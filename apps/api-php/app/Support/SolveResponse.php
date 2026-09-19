<?php

declare(strict_types=1);

namespace App\Support;

use Illuminate\Http\JsonResponse;
use NeetCode\Core\Support\Approach;

/**
 * Builds the response envelope shared by every problem endpoint.
 *
 * The envelope is byte-for-byte identical in the FastAPI and NestJS apps. That is what makes
 * the three implementations comparable: you can point the same HTTP client at port 8000, 3000
 * or 8080 and diff the JSON.
 *
 * Laravel would normally reach for an API Resource here. A Resource earns its keep when it is
 * shaping an Eloquent model; this envelope wraps a plain array and has no relations to load,
 * so a small factory is the more honest tool.
 */
final class SolveResponse
{
    /** @param array<string, mixed> $input */
    public static function make(string $slug, Approach $approach, array $input, mixed $result, int $elapsedMicros): JsonResponse
    {
        return new JsonResponse([
            'problem' => $slug,
            'approach' => $approach->toArray(),
            'input' => $input,
            'result' => $result,
            'elapsedMicros' => $elapsedMicros,
        ]);
    }
}
