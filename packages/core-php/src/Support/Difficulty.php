<?php

declare(strict_types=1);

namespace NeetCode\Core\Support;

/**
 * Backed enum — PHP's closest equivalent to Python's StrEnum and TypeScript's string-literal
 * union. Unlike the TypeScript version this exists at runtime, so `Difficulty::from()` gives
 * you real validation for free; unlike the Python version it cannot be compared to a bare
 * string without `->value`.
 */
enum Difficulty: string
{
    case Easy = 'easy';
    case Medium = 'medium';
    case Hard = 'hard';
}
