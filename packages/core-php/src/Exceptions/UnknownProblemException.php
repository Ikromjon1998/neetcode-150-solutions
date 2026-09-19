<?php

declare(strict_types=1);

namespace NeetCode\Core\Exceptions;

/** No problem is registered under that slug. */
final class UnknownProblemException extends NeetCodeException
{
    public function __construct(public readonly string $slug)
    {
        parent::__construct("Unknown problem: '{$slug}'");
    }
}
