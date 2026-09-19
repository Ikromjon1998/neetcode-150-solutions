<?php

declare(strict_types=1);

namespace NeetCode\Core\Registry;

use NeetCode\Core\Contracts\ContractRepository;
use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Exceptions\UnknownProblemException;
use NeetCode\Core\Support\Approach;
use NeetCode\Core\Support\ProblemMeta;
use RuntimeException;

/**
 * Problem registry — built from an explicit, injectable list of classes.
 *
 * This is the PHP answer to "how does the app find the solutions?", and it is deliberately
 * different from how the Python and TypeScript sides do it:
 *
 * - **Python** — a decorator registers each function as an import side effect, and `pkgutil`
 *   walks the package. Drop in a file and it appears. No registration step at all.
 * - **TypeScript** — one `import` line in a barrel file, so the bundler can tree-shake and
 *   the type-checker can verify every entry.
 * - **PHP (here)** — a list of class-strings, injected. Nothing is instantiated until it is
 *   asked for, and the list itself is a plain array, which is what makes
 *   `php artisan config:cache` possible.
 *
 * `docs/06-language-comparison.md` covers why each ecosystem landed where it did.
 */
final class ProblemRegistry
{
    /** @var array<string, class-string<ProblemDefinition>> */
    private array $bySlug = [];

    /** @param iterable<class-string<ProblemDefinition>> $definitions */
    public function __construct(
        iterable $definitions,
        private readonly ContractRepository $contracts = new ContractRepository(),
    ) {
        foreach ($definitions as $definition) {
            if (! is_subclass_of($definition, ProblemDefinition::class)) {
                throw new RuntimeException(
                    sprintf('%s does not implement %s', $definition, ProblemDefinition::class)
                );
            }

            $this->bySlug[$definition::slug()] = $definition;
        }
    }

    /** A registry holding every problem shipped with the package. */
    public static function default(?ContractRepository $contracts = null): self
    {
        return new self(DefaultProblems::all(), $contracts ?? new ContractRepository());
    }

    public function contracts(): ContractRepository
    {
        return $this->contracts;
    }

    public function has(string $slug): bool
    {
        return isset($this->bySlug[$slug]);
    }

    /** @return list<string> Slugs ordered by LeetCode id. */
    public function slugs(): array
    {
        $slugs = array_keys($this->bySlug);
        usort($slugs, fn (string $a, string $b): int => $this->contracts->meta($a)->id <=> $this->contracts->meta($b)->id);

        return $slugs;
    }

    /** @return list<ProblemMeta> Metadata for every registered problem, ordered by id. */
    public function all(): array
    {
        return array_map($this->meta(...), $this->slugs());
    }

    public function meta(string $slug): ProblemMeta
    {
        $this->assertKnown($slug);

        return $this->contracts->meta($slug);
    }

    /** @return list<string> */
    public function approaches(string $slug): array
    {
        $this->assertKnown($slug);

        return array_keys($this->bySlug[$slug]::solutions());
    }

    /** Look up one implementation. Pass `null` to get the contract's default. */
    public function solution(string $slug, ?string $approach = null): callable
    {
        $this->assertKnown($slug);

        $solutions = $this->bySlug[$slug]::solutions();
        $key = $approach ?? $this->contracts->meta($slug)->defaultApproach()->key;

        return $solutions[$key]
            ?? throw new UnknownApproachException($slug, $key, array_keys($solutions));
    }

    /**
     * Fail loudly if code and contracts have drifted apart.
     *
     * Called by a test and by the Laravel app at boot. It catches the two mistakes that are
     * easy to make when adding a problem: implementing an approach you forgot to declare in
     * the JSON, or declaring one you forgot to implement.
     */
    public function verify(): void
    {
        $problems = [];

        foreach ($this->bySlug as $slug => $class) {
            $meta = $this->contracts->meta($slug);
            $declared = array_map(static fn (Approach $a): string => $a->key, $meta->approaches);
            $implemented = array_keys($class::solutions());

            $missing = array_diff($declared, $implemented);
            if ($missing !== []) {
                $problems[] = "{$slug}: declared in contract but not implemented: ".implode(', ', $missing);
            }

            $extra = array_diff($implemented, $declared);
            if ($extra !== []) {
                $problems[] = "{$slug}: implemented but not declared in contract: ".implode(', ', $extra);
            }

            $defaults = array_filter($meta->approaches, static fn (Approach $a): bool => $a->isDefault);
            if (count($defaults) > 1) {
                $problems[] = "{$slug}: more than one default approach";
            }
        }

        if ($problems !== []) {
            throw new RuntimeException("Registry does not match contracts:\n  - ".implode("\n  - ", $problems));
        }
    }

    private function assertKnown(string $slug): void
    {
        if (! isset($this->bySlug[$slug])) {
            throw new UnknownProblemException($slug);
        }
    }
}
