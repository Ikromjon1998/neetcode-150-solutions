<?php

declare(strict_types=1);

namespace App\Problems\TwoSum;

use App\Http\Controllers\Controller;
use App\Support\SolveResponse;
use App\Support\Timing;
use Illuminate\Http\JsonResponse;
use NeetCode\Core\ArraysAndHashing\TwoSum;
use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Registry\ProblemRegistry;

/**
 * HTTP surface for problem 1.
 *
 * Every problem module in this app looks exactly like this file: a FormRequest, an approach
 * check, a registry lookup, and the shared envelope. That regularity is the point — it makes
 * adding problem 2 a copy-paste-and-rename job, and it is mirrored one-for-one by the FastAPI
 * router and the NestJS controller.
 *
 * The class lives in `app/Problems/TwoSum/` rather than the default
 * `app/Http/Controllers/`. PSR-4 maps `App\` to `app/`, so this needs no extra configuration,
 * and it keeps a feature's controller and its request object in one folder — the same shape
 * as the NestJS module and the FastAPI package.
 */
final class TwoSumController extends Controller
{
    public function __construct(private readonly ProblemRegistry $registry) {}

    public function __invoke(TwoSumRequest $request): JsonResponse
    {
        $approach = $this->resolveApproach($request->query('approach'));

        /** @var array{nums: list<int>, target: int} $input */
        $input = $request->validated();

        $solve = $this->registry->solution(TwoSum::SLUG, $approach);
        [$result, $elapsedMicros] = Timing::measure(
            static fn (): array => $solve($input['nums'], $input['target'])
        );

        return SolveResponse::make(
            TwoSum::SLUG,
            $this->registry->meta(TwoSum::SLUG)->approach($approach),
            // Rebuilt explicitly rather than passing `$input` straight through: `validated()`
            // returns keys in the order the rules happened to evaluate, not the order they
            // were declared. The FastAPI and NestJS apps both echo `{nums, target}`, and an
            // API's key order should not depend on a validator's internals.
            ['nums' => $input['nums'], 'target' => $input['target']],
            $result,
            $elapsedMicros,
        );
    }

    /**
     * Validate `?approach=` against this problem's registered keys.
     *
     * Not in the FormRequest: that validates the body, and this is a query parameter whose
     * valid values come from the registry rather than from a static rule string.
     */
    private function resolveApproach(mixed $requested): string
    {
        $available = $this->registry->approaches(TwoSum::SLUG);
        $approach = is_string($requested) && $requested !== ''
            ? $requested
            : $this->registry->meta(TwoSum::SLUG)->defaultApproach()->key;

        if (! in_array($approach, $available, true)) {
            throw new UnknownApproachException(TwoSum::SLUG, $approach, $available);
        }

        return $approach;
    }
}
