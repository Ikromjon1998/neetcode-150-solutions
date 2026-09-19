<?php

declare(strict_types=1);

namespace App\Support;

use Illuminate\Http\JsonResponse;

/** Builds the error envelope. Every non-2xx response in all three apps has this shape. */
final class ApiError
{
    /**
     * 422. Referenced from bootstrap/app.php, which is evaluated once per application
     * instance — and PHPUnit builds a fresh one per test. A top-level `const` there would be
     * redefined on the second test and raise a warning; a class constant is defined once.
     */
    public const UNPROCESSABLE_CONTENT = 422;

    /** @param list<array<string, mixed>>|null $details */
    public static function make(
        int $status,
        string $type,
        string $message,
        ?string $problem = null,
        ?array $details = null,
    ): JsonResponse {
        $error = ['type' => $type, 'message' => $message];

        if ($problem !== null) {
            $error['problem'] = $problem;
        }

        if ($details !== null) {
            $error['details'] = $details;
        }

        return new JsonResponse(['error' => $error], $status);
    }
}
