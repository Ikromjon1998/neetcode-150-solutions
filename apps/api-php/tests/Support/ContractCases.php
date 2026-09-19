<?php

declare(strict_types=1);

namespace Tests\Support;

use NeetCode\Core\Contracts\ContractRepository;

/**
 * Turns the shared JSON contract into PHPUnit data providers.
 *
 * Every case written in `packages/contracts/problems/*.json` becomes a named, individually
 * reported test here — and simultaneously in the Python and TypeScript suites, which read the
 * same file.
 *
 * Note that this is static and does not use the container: PHPUnit calls data providers
 * before the Laravel application is booted, so `app(ContractRepository::class)` is not
 * available yet. The core package being framework-free is what makes this possible at all.
 */
final class ContractCases
{
    private static ?ContractRepository $contracts = null;

    private static function contracts(): ContractRepository
    {
        return self::$contracts ??= new ContractRepository;
    }

    /**
     * Each case once per approach.
     *
     * @return iterable<string, array{string, array<string, mixed>, mixed}>
     */
    public static function perApproach(string $slug, array $approaches, string $section = 'cases'): iterable
    {
        foreach ($approaches as $approach) {
            foreach (self::contracts()->cases($slug, $section) as $case) {
                yield "{$case['name']} ({$approach})" => [
                    $approach,
                    $case['input'],
                    $case['expected'] ?? null,
                ];
            }
        }
    }

    /** @return iterable<string, array{array<string, mixed>, mixed}> */
    public static function plain(string $slug, string $section = 'cases'): iterable
    {
        foreach (self::contracts()->cases($slug, $section) as $case) {
            yield $case['name'] => [$case['input'], $case['expected'] ?? $case['status'] ?? null];
        }
    }
}
