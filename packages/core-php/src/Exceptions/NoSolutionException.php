<?php

declare(strict_types=1);

namespace NeetCode\Core\Exceptions;

/**
 * Input was well formed but no answer exists.
 *
 * Distinct from invalid input: `[1, 2, 3]` with target `100` is a perfectly legal request
 * that simply has no answer. The app renders this as 404, not 422.
 */
final class NoSolutionException extends NeetCodeException
{
    public function __construct(
        public readonly string $slug,
        public readonly string $detail = 'No solution exists for the given input.',
    ) {
        parent::__construct("{$slug}: {$detail}");
    }
}
