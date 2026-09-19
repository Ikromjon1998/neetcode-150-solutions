<?php

declare(strict_types=1);

namespace App\Problems\TopKFrequentElements;

use App\Http\Controllers\Controller;
use App\Support\SolveResponse;
use App\Support\Timing;
use Illuminate\Http\JsonResponse;
use NeetCode\Core\ArraysAndHashing\TopKFrequentElements;
use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Registry\ProblemRegistry;

/** HTTP surface for problem 347. */
final class TopKFrequentElementsController extends Controller
{
    public function __construct(private readonly ProblemRegistry $registry) {}

    public function __invoke(TopKFrequentElementsRequest $request): JsonResponse
    {
        $approach = $this->resolveApproach($request->query('approach'));
        $input = $request->validated();

        $solve = $this->registry->solution(TopKFrequentElements::SLUG, $approach);
        [$result, $elapsedMicros] = Timing::measure(static fn (): mixed => $solve($input['nums'], $input['k']));

        return SolveResponse::make(
            TopKFrequentElements::SLUG,
            $this->registry->meta(TopKFrequentElements::SLUG)->approach($approach),
            // Explicit: validated() key order follows rule evaluation, not declaration.
            ['nums' => $input['nums'], 'k' => $input['k']],
            $result,
            $elapsedMicros,
        );
    }

    private function resolveApproach(mixed $requested): string
    {
        $available = $this->registry->approaches(TopKFrequentElements::SLUG);
        $approach = is_string($requested) && $requested !== ''
            ? $requested
            : $this->registry->meta(TopKFrequentElements::SLUG)->defaultApproach()->key;

        if (! in_array($approach, $available, true)) {
            throw new UnknownApproachException(TopKFrequentElements::SLUG, $approach, $available);
        }

        return $approach;
    }
}
