<?php

declare(strict_types=1);

namespace App\Support;

/**
 * A stopwatch scoped to the algorithm call only.
 *
 * `hrtime(true)` returns nanoseconds from a monotonic clock. `microtime(true)` would be a
 * float of wall-clock seconds — subject to NTP adjustment and only microsecond-ish precision,
 * which is not enough when an O(n) pass over six elements finishes in a few hundred
 * nanoseconds.
 */
final class Timing
{
    /**
     * @template T
     *
     * @param  callable(): T  $callback
     * @return array{0: T, 1: int} [result, elapsed microseconds]
     */
    public static function measure(callable $callback): array
    {
        $start = hrtime(true);
        $result = $callback();

        return [$result, intdiv(hrtime(true) - $start, 1_000)];
    }
}
