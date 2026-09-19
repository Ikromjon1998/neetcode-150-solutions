<?php

declare(strict_types=1);

namespace NeetCode\Core\Tests\ArraysAndHashing;

use NeetCode\Core\ArraysAndHashing\TwoSum;
use NeetCode\Core\Contracts\ContractRepository;
use NeetCode\Core\Exceptions\NoSolutionException;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

/**
 * 1. Two Sum — driven entirely by packages/contracts/problems/0001-two-sum.json.
 *
 * Note what is *not* here: no hand-written input/expected pairs. Add a case to the JSON and
 * it lands in this file, in the Python suite and in the TypeScript suite at the same time.
 */
final class TwoSumTest extends TestCase
{
    #[Test]
    #[DataProvider('contractCases')]
    public function it_solves_every_contract_case(string $approach, array $input, array $expected): void
    {
        $solve = TwoSum::solutions()[$approach];

        $this->assertSame($expected, $solve($input['nums'], $input['target']));
    }

    #[Test]
    #[DataProvider('noSolutionCases')]
    public function it_throws_when_no_pair_exists(string $approach, array $input): void
    {
        $this->expectException(NoSolutionException::class);

        $solve = TwoSum::solutions()[$approach];
        $solve($input['nums'], $input['target']);
    }

    /**
     * Differential test: every approach must return the identical answer.
     *
     * This is the test that makes adding a new approach cheap and safe — it is automatically
     * compared against the ones already trusted.
     */
    #[Test]
    #[DataProvider('inputsOnly')]
    public function all_approaches_agree(array $input): void
    {
        $results = array_map(
            static fn (callable $solve): array => $solve($input['nums'], $input['target']),
            TwoSum::solutions(),
        );

        $this->assertCount(1, array_unique(array_map(serialize(...), $results)));
    }

    /** @return iterable<string, array{string, array<string, mixed>, list<int>}> */
    public static function contractCases(): iterable
    {
        $contracts = new ContractRepository();

        foreach (array_keys(TwoSum::solutions()) as $approach) {
            foreach ($contracts->cases(TwoSum::SLUG) as $case) {
                yield "{$case['name']} ({$approach})" => [$approach, $case['input'], $case['expected']];
            }
        }
    }

    /** @return iterable<string, array{string, array<string, mixed>}> */
    public static function noSolutionCases(): iterable
    {
        $contracts = new ContractRepository();

        foreach (array_keys(TwoSum::solutions()) as $approach) {
            foreach ($contracts->cases(TwoSum::SLUG, 'notFoundCases') as $case) {
                yield "{$case['name']} ({$approach})" => [$approach, $case['input']];
            }
        }
    }

    /** @return iterable<string, array{array<string, mixed>}> */
    public static function inputsOnly(): iterable
    {
        foreach ((new ContractRepository())->cases(TwoSum::SLUG) as $case) {
            yield $case['name'] => [$case['input']];
        }
    }
}
