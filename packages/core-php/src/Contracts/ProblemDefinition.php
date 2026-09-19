<?php

declare(strict_types=1);

namespace NeetCode\Core\Contracts;

/**
 * What a problem class must expose so the registry can pick it up.
 *
 * An interface, not a decorator (Python) and not a plain object literal (TypeScript). PHP has
 * had attributes since 8.0 and they could have played the decorator's role, but reading them
 * requires reflection over every candidate class — and reflection-based discovery is exactly
 * what `php artisan config:cache` exists to avoid. An explicit interface plus an explicit list
 * is both faster and easier to follow.
 */
interface ProblemDefinition
{
    /** kebab-case identifier, matching the JSON contract and the URL segment. */
    public static function slug(): string;

    /**
     * Approach key => callable implementation.
     *
     * @return array<string, callable>
     */
    public static function solutions(): array;
}
