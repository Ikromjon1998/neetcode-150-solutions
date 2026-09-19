<?php

declare(strict_types=1);

namespace NeetCode\Core\Exceptions;

use RuntimeException;

/**
 * Base class, so the Laravel app can catch everything this package throws with one handler.
 *
 * Extends `RuntimeException` rather than `Exception` because every one of these describes a
 * condition only detectable at runtime, which is precisely the SPL distinction — and it keeps
 * these separate from Laravel's own `LogicException` hierarchy.
 */
abstract class NeetCodeException extends RuntimeException
{
}
