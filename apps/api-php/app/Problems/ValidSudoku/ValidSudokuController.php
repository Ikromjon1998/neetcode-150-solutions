<?php

declare(strict_types=1);

namespace App\Problems\ValidSudoku;

use App\Http\Controllers\Controller;
use App\Support\SolveResponse;
use App\Support\Timing;
use Illuminate\Http\JsonResponse;
use NeetCode\Core\ArraysAndHashing\ValidSudoku;
use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Registry\ProblemRegistry;

/** HTTP surface for problem 36. */
final class ValidSudokuController extends Controller
{
    public function __construct(private readonly ProblemRegistry $registry) {}

    public function __invoke(ValidSudokuRequest $request): JsonResponse
    {
        $approach = $this->resolveApproach($request->query('approach'));
        $input = $request->validated();

        $solve = $this->registry->solution(ValidSudoku::SLUG, $approach);
        [$result, $elapsedMicros] = Timing::measure(static fn (): mixed => $solve($input['board']));

        return SolveResponse::make(
            ValidSudoku::SLUG,
            $this->registry->meta(ValidSudoku::SLUG)->approach($approach),
            // Explicit: validated() key order follows rule evaluation, not declaration.
            ['board' => $input['board']],
            $result,
            $elapsedMicros,
        );
    }

    private function resolveApproach(mixed $requested): string
    {
        $available = $this->registry->approaches(ValidSudoku::SLUG);
        $approach = is_string($requested) && $requested !== ''
            ? $requested
            : $this->registry->meta(ValidSudoku::SLUG)->defaultApproach()->key;

        if (! in_array($approach, $available, true)) {
            throw new UnknownApproachException(ValidSudoku::SLUG, $approach, $available);
        }

        return $approach;
    }
}
