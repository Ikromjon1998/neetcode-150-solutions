<?php

declare(strict_types=1);

namespace App\Problems\ProductOfArrayExceptSelf;

use App\Http\Controllers\Controller;
use App\Support\SolveResponse;
use App\Support\Timing;
use Illuminate\Http\JsonResponse;
use NeetCode\Core\ArraysAndHashing\ProductOfArrayExceptSelf;
use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Registry\ProblemRegistry;

/** HTTP surface for problem 238. */
final class ProductOfArrayExceptSelfController extends Controller
{
    public function __construct(private readonly ProblemRegistry $registry) {}

    public function __invoke(ProductOfArrayExceptSelfRequest $request): JsonResponse
    {
        $approach = $this->resolveApproach($request->query('approach'));
        $input = $request->validated();

        $solve = $this->registry->solution(ProductOfArrayExceptSelf::SLUG, $approach);
        [$result, $elapsedMicros] = Timing::measure(static fn (): mixed => $solve($input['nums']));

        return SolveResponse::make(
            ProductOfArrayExceptSelf::SLUG,
            $this->registry->meta(ProductOfArrayExceptSelf::SLUG)->approach($approach),
            // Explicit: validated() key order follows rule evaluation, not declaration.
            ['nums' => $input['nums']],
            $result,
            $elapsedMicros,
        );
    }

    private function resolveApproach(mixed $requested): string
    {
        $available = $this->registry->approaches(ProductOfArrayExceptSelf::SLUG);
        $approach = is_string($requested) && $requested !== ''
            ? $requested
            : $this->registry->meta(ProductOfArrayExceptSelf::SLUG)->defaultApproach()->key;

        if (! in_array($approach, $available, true)) {
            throw new UnknownApproachException(ProductOfArrayExceptSelf::SLUG, $approach, $available);
        }

        return $approach;
    }
}
