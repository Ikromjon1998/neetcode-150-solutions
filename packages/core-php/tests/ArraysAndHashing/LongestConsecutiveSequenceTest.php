<?php

declare(strict_types=1);

namespace NeetCode\Core\Tests\ArraysAndHashing;

use NeetCode\Core\ArraysAndHashing\LongestConsecutiveSequence;
use NeetCode\Core\Contracts\ContractRepository;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

/**
 * 128. Longest Consecutive Sequence — driven by packages/contracts/problems/0128-longest-consecutive-sequence.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the TypeScript suite at the same time.
 */
final class LongestConsecutiveSequenceTest extends TestCase
{
    #[Test]
    #[DataProvider('contractCases')]
    public function it_solves_every_contract_case(string $approach, array $input, mixed $expected): void
    {
        $solve = LongestConsecutiveSequence::solutions()[$approach];

        $this->assertSame($expected, $solve($input['nums']));
    }

    /** Differential test — every approach must return the identical answer. */
    #[Test]
    #[DataProvider('inputsOnly')]
    public function all_approaches_agree(array $input): void
    {
        $results = array_map(
            static fn (callable $solve): mixed => $solve($input['nums']),
            LongestConsecutiveSequence::solutions(),
        );

        $this->assertCount(1, array_unique(array_map(serialize(...), $results)));
    }

    /** @return iterable<string, array{string, array<string, mixed>, mixed}> */
    public static function contractCases(): iterable
    {
        $contracts = new ContractRepository();

        foreach (array_keys(LongestConsecutiveSequence::solutions()) as $approach) {
            foreach ($contracts->cases(LongestConsecutiveSequence::SLUG) as $case) {
                yield "{$case['name']} ({$approach})" => [$approach, $case['input'], $case['expected']];
            }
        }
    }

    /** @return iterable<string, array{array<string, mixed>}> */
    public static function inputsOnly(): iterable
    {
        foreach ((new ContractRepository())->cases(LongestConsecutiveSequence::SLUG) as $case) {
            yield $case['name'] => [$case['input']];
        }
    }
}
