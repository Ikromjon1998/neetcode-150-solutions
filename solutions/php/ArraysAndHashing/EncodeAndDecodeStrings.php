<?php

declare(strict_types=1);

namespace NeetCode\Core\ArraysAndHashing;

use NeetCode\Core\Contracts\ProblemDefinition;

/**
 * 271. Encode and Decode Strings — https://leetcode.com/problems/encode-and-decode-strings/
 *
 * Flatten a list of arbitrary strings into one string, and recover the list exactly.
 *
 * A design exercise with two halves, so the registered function runs the full round trip: it
 * encodes the input and returns what decoding produces. A correct implementation therefore
 * returns its input unchanged — and any encoding that cannot survive delimiters, empty strings
 * or leading digits will not.
 */
final class EncodeAndDecodeStrings implements ProblemDefinition
{
    public const SLUG = 'encode-and-decode-strings';

    private const SENTINEL = '#';

    private const DELIMITER = ':';

    private const ESCAPE = '\\';

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
     * `<length>#<payload>` for each string, concatenated.
     *
     * The length is measured in **bytes** with `strlen`, deliberately, because the decoder
     * slices with `substr`, which also counts bytes. Mixing `mb_strlen` with `substr` — or
     * `strlen` with `mb_substr` — produces a decoder that works perfectly on ASCII and silently
     * corrupts anything else. Elsewhere in this repo `mb_*` is always the right answer; here the
     * rule is narrower and sharper: **the measure and the slice must agree**.
     *
     * @param  list<string>  $strs
     */
    private static function encodeLengthPrefixed(array $strs): string
    {
        $encoded = '';

        foreach ($strs as $word) {
            $encoded .= strlen($word).self::SENTINEL.$word;
        }

        return $encoded;
    }

    /**
     * Read a length, skip the sentinel, take exactly that many bytes, repeat.
     *
     * @return list<string>
     */
    private static function decodeLengthPrefixed(string $encoded): array
    {
        $result = [];
        $cursor = 0;
        $total = strlen($encoded);

        while ($cursor < $total) {
            $sentinel = strpos($encoded, self::SENTINEL, $cursor);
            $length = (int) substr($encoded, $cursor, $sentinel - $cursor);
            $start = $sentinel + 1;
            $result[] = substr($encoded, $start, $length);
            $cursor = $start + $length;
        }

        return $result;
    }

    /**
     * Round trip through the length-prefixed encoding. Time O(n), space O(n).
     *
     * The length is read before the payload, so the payload is never scanned and may contain
     * anything at all — `#`, digits, `4#test`. That is why this is the standard answer: it makes
     * the payload opaque instead of trying to escape it.
     *
     * @param  list<string>  $strs
     * @return list<string>
     */
    public static function lengthPrefixed(array $strs): array
    {
        return self::decodeLengthPrefixed(self::encodeLengthPrefixed($strs));
    }

    /**
     * Join on `:`, escaping `\` first and then `:` inside each payload.
     *
     * Order matters: escape the escape character before the delimiter, or decoding cannot tell
     * an escaped delimiter from a backslash followed by a real one.
     *
     * @param  list<string>  $strs
     */
    private static function encodeDelimiterEscaped(array $strs): string
    {
        $escaped = array_map(
            static fn (string $word): string => str_replace(
                [self::ESCAPE, self::DELIMITER],
                [self::ESCAPE.self::ESCAPE, self::ESCAPE.self::DELIMITER],
                $word,
            ),
            $strs,
        );

        return implode(self::DELIMITER, $escaped);
    }

    /**
     * Scan byte by byte, honouring the escape.
     *
     * Byte-wise is safe here only because both the delimiter and the escape are ASCII, and no
     * byte of a UTF-8 multi-byte sequence can collide with an ASCII byte. That property is what
     * UTF-8 was designed for, and it is the reason this decoder does not need `mb_*`.
     *
     * @return list<string>
     */
    private static function decodeDelimiterEscaped(string $encoded): array
    {
        $result = [];
        $current = '';
        $index = 0;
        $total = strlen($encoded);

        while ($index < $total) {
            $char = $encoded[$index];

            if ($char === self::ESCAPE && $index + 1 < $total) {
                $current .= $encoded[$index + 1];
                $index += 2;
            } elseif ($char === self::DELIMITER) {
                $result[] = $current;
                $current = '';
                $index++;
            } else {
                $current .= $char;
                $index++;
            }
        }

        $result[] = $current;

        return $result;
    }

    /**
     * Round trip through the escaped-delimiter encoding. Time O(n), space O(n).
     *
     * Correct, but strictly more work: every character is examined twice and the decoder cannot
     * skip ahead. It exists to make the length prefix's advantage concrete rather than asserted.
     *
     * The empty list is the one case a delimiter format cannot represent — joining nothing
     * produces `''`, and splitting `''` produces `['']`, not `[]`. The special case below is
     * itself the lesson.
     *
     * @param  list<string>  $strs
     * @return list<string>
     */
    public static function delimiterEscaped(array $strs): array
    {
        if ($strs === []) {
            return [];
        }

        return self::decodeDelimiterEscaped(self::encodeDelimiterEscaped($strs));
    }
}
