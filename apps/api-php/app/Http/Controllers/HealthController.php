<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use Illuminate\Http\JsonResponse;
use NeetCode\Core\Registry\ProblemRegistry;

/**
 * Liveness endpoint. Mirrors FastAPI's `/health` and the NestJS `HealthController`.
 *
 * Laravel also ships its own `/up` (configured in `bootstrap/app.php`); this one exists so
 * all three apps answer the same path with the same body.
 *
 * Note the constructor: nothing registers `ProblemRegistry` as a controller dependency
 * anywhere. Laravel's container reads the type hint and resolves the singleton the service
 * provider bound. FastAPI needs an explicit `Depends(...)`, NestJS needs the provider listed
 * in a module.
 */
final class HealthController extends Controller
{
    public function __construct(private readonly ProblemRegistry $registry) {}

    public function __invoke(): JsonResponse
    {
        return new JsonResponse([
            'status' => 'ok',
            'runtime' => 'php/laravel',
            'version' => (string) config('app.version', '1.0.0'),
            'problemsRegistered' => count($this->registry->slugs()),
        ]);
    }
}
