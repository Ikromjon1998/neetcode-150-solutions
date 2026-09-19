<?php

declare(strict_types=1);

namespace NeetCode\Core\Contracts;

use JsonException;
use NeetCode\Core\Exceptions\UnknownProblemException;
use NeetCode\Core\Support\ProblemMeta;
use RuntimeException;

/**
 * Loader for the shared JSON contracts in `packages/contracts/`.
 *
 * One JSON file per problem is the single source of truth for metadata and test cases, and
 * all three languages read it. Adding a case to the JSON immediately tightens the Python,
 * TypeScript and PHP suites at once — there is no way for them to drift apart.
 *
 * In the Laravel app this is bound as a singleton, so the files are read once per process
 * rather than once per request.
 */
final class ContractRepository
{
    private const ENV_VAR = 'NEETCODE_CONTRACTS_DIR';

    /** @var array<string, array<string, mixed>>|null */
    private ?array $contracts = null;

    /** @var array<string, ProblemMeta> */
    private array $metaCache = [];

    public function __construct(private readonly ?string $directory = null)
    {
    }

    /**
     * Locate `packages/contracts/problems`.
     *
     * Checks an explicit constructor argument, then $NEETCODE_CONTRACTS_DIR, then walks up
     * from this file, then from the working directory. The last fallback matters because
     * Composer installs this package as a symlink into `vendor/`, and `__DIR__` may resolve
     * either side of that link depending on how PHP was invoked.
     */
    public function directory(): string
    {
        if ($this->directory !== null) {
            return $this->directory;
        }

        $override = getenv(self::ENV_VAR);
        if (is_string($override) && $override !== '') {
            $path = realpath($override);
            if ($path === false || ! is_dir($path)) {
                throw new RuntimeException(
                    sprintf('$%s points at %s, which is not a directory.', self::ENV_VAR, $override)
                );
            }

            return $path;
        }

        foreach ([__DIR__, getcwd() ?: __DIR__] as $start) {
            $found = self::walkUp((string) $start);
            if ($found !== null) {
                return $found;
            }
        }

        throw new RuntimeException(sprintf(
            'Could not find packages/contracts/problems by walking up from %s or %s. Set $%s explicitly.',
            __DIR__,
            (string) getcwd(),
            self::ENV_VAR,
        ));
    }

    private static function walkUp(string $start): ?string
    {
        $current = realpath($start) ?: $start;

        while (true) {
            $candidate = $current.'/packages/contracts/problems';
            if (is_dir($candidate)) {
                return $candidate;
            }

            $parent = dirname($current);
            if ($parent === $current) {
                return null;
            }

            $current = $parent;
        }
    }

    /** @return array<string, array<string, mixed>> */
    private function all(): array
    {
        if ($this->contracts !== null) {
            return $this->contracts;
        }

        $contracts = [];
        $files = glob($this->directory().'/*.json') ?: [];
        sort($files);

        foreach ($files as $file) {
            $raw = file_get_contents($file);
            if ($raw === false) {
                throw new RuntimeException("Could not read contract file: {$file}");
            }

            try {
                /** @var array<string, mixed> $data */
                $data = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
            } catch (JsonException $e) {
                throw new RuntimeException("Invalid JSON in {$file}: {$e->getMessage()}", 0, $e);
            }

            $slug = (string) $data['slug'];
            if (isset($contracts[$slug])) {
                throw new RuntimeException("Duplicate contract slug '{$slug}' in {$file}");
            }

            $contracts[$slug] = $data;
        }

        return $this->contracts = $contracts;
    }

    /**
     * The decoded JSON for one problem, exactly as written on disk.
     *
     * @return array<string, mixed>
     */
    public function raw(string $slug): array
    {
        $contracts = $this->all();

        return $contracts[$slug] ?? throw new UnknownProblemException($slug);
    }

    /** @return list<string> */
    public function slugs(): array
    {
        return array_keys($this->all());
    }

    /** Parse one contract into the typed `ProblemMeta` the rest of the code uses. */
    public function meta(string $slug): ProblemMeta
    {
        return $this->metaCache[$slug] ??= ProblemMeta::fromArray($this->raw($slug));
    }

    /**
     * Test cases from a contract. `$section` is one of the *Cases keys in the schema.
     *
     * @return list<array<string, mixed>>
     */
    public function cases(string $slug, string $section = 'cases'): array
    {
        /** @var list<array<string, mixed>> $cases */
        $cases = $this->raw($slug)[$section] ?? [];

        return $cases;
    }
}
