<?php

declare(strict_types=1);

namespace App\Problems\TwoSum;

use Illuminate\Foundation\Http\FormRequest;

/**
 * Request validation for `POST /problems/two-sum`.
 *
 * A FormRequest is Laravel's counterpart to a Pydantic model and to a `class-validator` DTO.
 * The mechanism differs in a way worth knowing: rules are *strings evaluated at runtime*
 * against the raw input, not type annotations. That buys enormous flexibility — `bail`,
 * `sometimes`, cross-field rules, database-aware rules — and costs you compile-time safety
 * and editor autocompletion, which the other two get for free.
 *
 * `integer` is notably lax: it accepts the numeric string `"7"`. That would make this
 * endpoint disagree with the NestJS one, where `@IsInt()` rejects it, so the rule set below
 * is tightened with an explicit `is_int` closure.
 */
final class TwoSumRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    /** @return array<string, mixed> */
    public function rules(): array
    {
        return [
            'nums' => ['required', 'array', 'min:2'],
            'nums.*' => ['required', $this->strictInteger('nums.*')],
            'target' => ['required', $this->strictInteger('target')],
        ];
    }

    /** @return array<string, string> */
    public function messages(): array
    {
        return [
            'nums.min' => 'nums must contain at least 2 elements.',
            'nums.required' => 'nums is required.',
            'target.required' => 'target is required.',
        ];
    }

    /**
     * Reject anything that is not a real JSON integer.
     *
     * Laravel's built-in `integer` rule passes for `"7"` and for `7.0`. The Python app uses
     * Pydantic's `StrictInt` and the Node app uses `@IsInt()`; both refuse those. This closure
     * keeps the three in agreement.
     */
    private function strictInteger(string $label): callable
    {
        return static function (string $attribute, mixed $value, callable $fail) use ($label): void {
            if (! is_int($value)) {
                $fail("{$label} must be an integer.");
            }
        };
    }

    /**
     * Reject unexpected fields.
     *
     * Laravel has no `forbidNonWhitelisted` switch the way `ValidationPipe` does, and no
     * `extra="forbid"` the way Pydantic does — `validated()` simply drops what it does not
     * know. A typo'd field name is a bug, so this closes the gap explicitly.
     */
    protected function prepareForValidation(): void
    {
        // `$this->all()` merges the query string into the body, so `?approach=hash-map`
        // would look like an unexpected field. Only the decoded JSON body is the payload.
        $unexpected = array_diff(array_keys($this->json()->all()), ['nums', 'target']);

        if ($unexpected !== []) {
            abort(422, 'Unexpected fields: '.implode(', ', $unexpected));
        }
    }
}
