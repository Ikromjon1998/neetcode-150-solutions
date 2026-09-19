<?php

declare(strict_types=1);

namespace App\Problems\ValidAnagram;

use Illuminate\Foundation\Http\FormRequest;

/**
 * Request validation for `POST /problems/valid-anagram`.
 *
 * Two Laravel defaults would make this endpoint disagree with its Python and Node twins, and
 * both are worked around below:
 *
 * 1. The `integer` rule accepts the numeric string "7". Pydantic's `StrictInt` and
 *    class-validator's `@IsInt()` both refuse it, so `strictType()` does the check by hand.
 * 2. The `required` rule rejects the empty string, the empty array and `"0"` — so
 *    `{"s": "", "t": ""}` would 422 here while returning 200 everywhere else. `present` is
 *    the rule that means what you actually want: the key must be in the payload.
 */
final class ValidAnagramRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    /** @return array<string, mixed> */
    public function rules(): array
    {
        return [
            's' => ['present', $this->strictType('is_string', 's')],
            't' => ['present', $this->strictType('is_string', 't')],
        ];
    }

    private function strictType(string $check, string $label): callable
    {
        return static function (string $attribute, mixed $value, callable $fail) use ($check, $label): void {
            if (! $check($value)) {
                $fail("{$label} has the wrong type.");
            }
        };
    }

    /** Laravel silently drops unknown fields; a typo'd field name is a bug. */
    protected function prepareForValidation(): void
    {
        $unexpected = array_diff(array_keys($this->json()->all()), ['s', 't']);

        if ($unexpected !== []) {
            abort(422, 'Unexpected fields: '.implode(', ', $unexpected));
        }
    }
}
