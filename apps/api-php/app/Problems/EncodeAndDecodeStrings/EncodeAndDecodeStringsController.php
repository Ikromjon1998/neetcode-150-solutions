<?php

declare(strict_types=1);

namespace App\Problems\EncodeAndDecodeStrings;

use App\Http\Controllers\Controller;
use App\Support\SolveResponse;
use App\Support\Timing;
use Illuminate\Http\JsonResponse;
use NeetCode\Core\ArraysAndHashing\EncodeAndDecodeStrings;
use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Registry\ProblemRegistry;

/** HTTP surface for problem 271. */
final class EncodeAndDecodeStringsController extends Controller
{
    public function __construct(private readonly ProblemRegistry $registry) {}

    public function __invoke(EncodeAndDecodeStringsRequest $request): JsonResponse
    {
        $approach = $this->resolveApproach($request->query('approach'));
        $input = $request->validated();

        $solve = $this->registry->solution(EncodeAndDecodeStrings::SLUG, $approach);
        [$result, $elapsedMicros] = Timing::measure(static fn (): mixed => $solve($input['strs']));

        return SolveResponse::make(
            EncodeAndDecodeStrings::SLUG,
            $this->registry->meta(EncodeAndDecodeStrings::SLUG)->approach($approach),
            // Explicit: validated() key order follows rule evaluation, not declaration.
            ['strs' => $input['strs']],
            $result,
            $elapsedMicros,
        );
    }

    private function resolveApproach(mixed $requested): string
    {
        $available = $this->registry->approaches(EncodeAndDecodeStrings::SLUG);
        $approach = is_string($requested) && $requested !== ''
            ? $requested
            : $this->registry->meta(EncodeAndDecodeStrings::SLUG)->defaultApproach()->key;

        if (! in_array($approach, $available, true)) {
            throw new UnknownApproachException(EncodeAndDecodeStrings::SLUG, $approach, $available);
        }

        return $approach;
    }
}
