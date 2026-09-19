<?php

declare(strict_types=1);

namespace App\Problems\ProductOfArrayExceptSelf;

use Illuminate\Foundation\Http\FormRequest;

/**
 * Request validation for `POST /problems/product-of-array-except-self`.
 *
 * Laravel's built-in `integer` rule accepts the numeric string "7"; Pydantic's StrictInt and
 * class-validator's @IsInt() both refuse it. `strictType()` keeps the three apps in agreement.
 */
final class ProductOfArrayExceptSelfRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    /** @return array<string, mixed> */
    public function rules(): array
    {
        return [
            'nums' => ['present', 'array'],
            'nums.*' => ['present', $this->strictType('is_int', 'nums.*')],
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
        $unexpected = array_diff(array_keys($this->json()->all()), ['nums']);

        if ($unexpected !== []) {
            abort(422, 'Unexpected fields: '.implode(', ', $unexpected));
        }
    }
}
