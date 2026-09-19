<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;
use NeetCode\Core\Exceptions\UnsolvedException;

/**
 * 271. Encode and Decode Strings
 *
 * Design an encoding that flattens a list of arbitrary strings into one string, and a decoding
 * that recovers the list exactly. Unlike the other problems here this is a design exercise with
 * two halves, so the endpoint runs the full round trip: it encodes the input and returns what
 * decoding produces. A correct implementation therefore returns its input unchanged — and any
 * encoding that cannot survive delimiters, empty strings or digits will not.
 *
 * https://leetcode.com/problems/encode-and-decode-strings/
 *
 * Each method below is an exercise. Replace the `throw` with your implementation, then
 * run `make test-php`.
 *
 * Stuck? `make show SLUG=encode-and-decode-strings` prints a worked answer.
 */
final class EncodeAndDecodeStrings implements ProblemDefinition
{
    public const SLUG = 'encode-and-decode-strings';

    private const PATH = 'packages/core-php/src/ArraysAndHashing/EncodeAndDecodeStrings.php';

    public static function slug(): string
    {
        return self::SLUG;
    }

    /** @return array<string, callable> */
    public static function solutions(): array
    {
        return [
            'length-prefixed' => self::lengthPrefixed(...),
            'delimiter-escaped' => self::delimiterEscaped(...),
        ];
    }

    /**
     * Length prefix and sentinel — target: O(n) time, O(n) space.
     *
     * Write each string as `<length>#<string>`. The length is read before the payload, so the
     * payload is never scanned for a delimiter and may contain anything at all — including `#` and
     * digits. The standard answer, and the only one here that is unconditionally safe.
     */
    public static function lengthPrefixed(array $strs): array
    {
        throw new UnsolvedException(self::SLUG, 'length-prefixed', self::PATH);
    }

    /**
     * Escaped delimiter — target: O(n) time, O(n) space.
     *
     * Join on a delimiter, escaping any occurrence of it (and of the escape character) inside the
     * payloads. Correct, but every decode has to scan character by character — it exists here to
     * show what the length prefix buys you.
     */
    public static function delimiterEscaped(array $strs): array
    {
        throw new UnsolvedException(self::SLUG, 'delimiter-escaped', self::PATH);
    }
}
