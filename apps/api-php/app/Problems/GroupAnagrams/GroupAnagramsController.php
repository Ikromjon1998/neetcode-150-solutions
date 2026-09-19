<?php

declare(strict_types=1);

namespace App\Problems\GroupAnagrams;

use App\Http\Controllers\Controller;
use App\Support\SolveResponse;
use App\Support\Timing;
use Illuminate\Http\JsonResponse;
use NeetCode\Core\ArraysAndHashing\GroupAnagrams;
use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Registry\ProblemRegistry;

/** HTTP surface for problem 49. */
final class GroupAnagramsController extends Controller
{
    public function __construct(private readonly ProblemRegistry $registry) {}

    public function __invoke(GroupAnagramsRequest $request): JsonResponse
    {
        $approach = $this->resolveApproach($request->query('approach'));
        $input = $request->validated();

        $solve = $this->registry->solution(GroupAnagrams::SLUG, $approach);
        [$result, $elapsedMicros] = Timing::measure(static fn (): mixed => $solve($input['strs']));

        return SolveResponse::make(
            GroupAnagrams::SLUG,
            $this->registry->meta(GroupAnagrams::SLUG)->approach($approach),
            // Explicit: validated() key order follows rule evaluation, not declaration.
            ['strs' => $input['strs']],
            $result,
            $elapsedMicros,
        );
    }

    private function resolveApproach(mixed $requested): string
    {
        $available = $this->registry->approaches(GroupAnagrams::SLUG);
        $approach = is_string($requested) && $requested !== ''
            ? $requested
            : $this->registry->meta(GroupAnagrams::SLUG)->defaultApproach()->key;

        if (! in_array($approach, $available, true)) {
            throw new UnknownApproachException(GroupAnagrams::SLUG, $approach, $available);
        }

        return $approach;
    }
}
