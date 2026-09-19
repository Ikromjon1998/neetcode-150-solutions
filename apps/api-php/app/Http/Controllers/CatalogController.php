<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use Illuminate\Http\JsonResponse;
use NeetCode\Core\Registry\ProblemRegistry;
use NeetCode\Core\Support\ProblemMeta;

/**
 * Catalog endpoints — the same two routes exist in all three apps.
 *
 * Everything here is derived from the registry, so a newly added problem appears in the
 * catalog without anyone editing this file.
 */
final class CatalogController extends Controller
{
    public function __construct(private readonly ProblemRegistry $registry) {}

    public function index(): JsonResponse
    {
        return new JsonResponse(array_map($this->summarise(...), $this->registry->all()));
    }

    /** Throws `UnknownProblemException`, which `bootstrap/app.php` renders as 404. */
    public function show(string $slug): JsonResponse
    {
        return new JsonResponse($this->summarise($this->registry->meta($slug)));
    }

    /** @return array<string, mixed> */
    private function summarise(ProblemMeta $meta): array
    {
        return [...$meta->toArray(), 'endpoint' => "/problems/{$meta->slug}"];
    }
}
