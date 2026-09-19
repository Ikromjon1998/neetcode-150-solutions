<?php

declare(strict_types=1);

namespace App\Problems\ValidAnagram;

use App\Http\Controllers\Controller;
use App\Support\SolveResponse;
use App\Support\Timing;
use Illuminate\Http\JsonResponse;
use NeetCode\Core\ArraysAndHashing\ValidAnagram;
use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Registry\ProblemRegistry;

/** HTTP surface for problem 242. */
final class ValidAnagramController extends Controller
{
    public function __construct(private readonly ProblemRegistry $registry) {}

    public function __invoke(ValidAnagramRequest $request): JsonResponse
    {
        $approach = $this->resolveApproach($request->query('approach'));
        $input = $request->validated();

        $solve = $this->registry->solution(ValidAnagram::SLUG, $approach);
        [$result, $elapsedMicros] = Timing::measure(static fn (): mixed => $solve($input['s'], $input['t']));

        return SolveResponse::make(
            ValidAnagram::SLUG,
            $this->registry->meta(ValidAnagram::SLUG)->approach($approach),
            // Explicit: validated() key order follows rule evaluation, not declaration.
            ['s' => $input['s'], 't' => $input['t']],
            $result,
            $elapsedMicros,
        );
    }

    private function resolveApproach(mixed $requested): string
    {
        $available = $this->registry->approaches(ValidAnagram::SLUG);
        $approach = is_string($requested) && $requested !== ''
            ? $requested
            : $this->registry->meta(ValidAnagram::SLUG)->defaultApproach()->key;

        if (! in_array($approach, $available, true)) {
            throw new UnknownApproachException(ValidAnagram::SLUG, $approach, $available);
        }

        return $approach;
    }
}
