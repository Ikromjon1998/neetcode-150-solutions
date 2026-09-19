<?php

declare(strict_types=1);

namespace App\Problems\LongestConsecutiveSequence;

use App\Http\Controllers\Controller;
use App\Support\SolveResponse;
use App\Support\Timing;
use Illuminate\Http\JsonResponse;
use NeetCode\Core\ArraysAndHashing\LongestConsecutiveSequence;
use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Registry\ProblemRegistry;

/** HTTP surface for problem 128. */
final class LongestConsecutiveSequenceController extends Controller
{
    public function __construct(private readonly ProblemRegistry $registry) {}

    public function __invoke(LongestConsecutiveSequenceRequest $request): JsonResponse
    {
        $approach = $this->resolveApproach($request->query('approach'));
        $input = $request->validated();

        $solve = $this->registry->solution(LongestConsecutiveSequence::SLUG, $approach);
        [$result, $elapsedMicros] = Timing::measure(static fn (): mixed => $solve($input['nums']));

        return SolveResponse::make(
            LongestConsecutiveSequence::SLUG,
            $this->registry->meta(LongestConsecutiveSequence::SLUG)->approach($approach),
            // Explicit: validated() key order follows rule evaluation, not declaration.
            ['nums' => $input['nums']],
            $result,
            $elapsedMicros,
        );
    }

    private function resolveApproach(mixed $requested): string
    {
        $available = $this->registry->approaches(LongestConsecutiveSequence::SLUG);
        $approach = is_string($requested) && $requested !== ''
            ? $requested
            : $this->registry->meta(LongestConsecutiveSequence::SLUG)->defaultApproach()->key;

        if (! in_array($approach, $available, true)) {
            throw new UnknownApproachException(LongestConsecutiveSequence::SLUG, $approach, $available);
        }

        return $approach;
    }
}
