<?php

declare(strict_types=1);

namespace NeetCode\Core\Exceptions;

/** The problem exists but has no implementation registered under that approach key. */
final class UnknownApproachException extends NeetCodeException
{
    /** @param list<string> $available */
    public function __construct(
        public readonly string $slug,
        public readonly string $approach,
        public readonly array $available = [],
    ) {
        $hint = $available === [] ? '' : ' Available: '.implode(', ', $available).'.';
        parent::__construct("Unknown approach '{$approach}' for problem '{$slug}'.{$hint}");
    }
}
