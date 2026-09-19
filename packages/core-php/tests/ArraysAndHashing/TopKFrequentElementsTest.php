<?php

declare(strict_types=1);

namespace NeetCode\Core\Tests\ArraysAndHashing;

use NeetCode\Core\ArraysAndHashing\TopKFrequentElements;
use NeetCode\Core\Contracts\ContractRepository;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

/**
 * 347. Top K Frequent Elements — driven by packages/contracts/problems/0347-top-k-frequent-elements.json.
 *
 * No hand-written fixtures: add a case to the JSON and it lands here, in the Python suite and
 * in the TypeScript suite at the same time.
 */
final class TopKFrequentElementsTest extends TestCase
{
    #[Test]
    #[DataProvider('contractCases')]
    public function it_solves_every_contract_case(string $approach, array $input, mixed $expected): void
    {
        $solve = TopKFrequentElements::solutions()[$approach];

        $this->assertSame($expected, $solve($input['nums'], $input['k']));
    }

    /** Differential test — every approach must return the identical answer. */
    #[Test]
    #[DataProvider('inputsOnly')]
    public function all_approaches_agree(array $input): void
    {
        $results = array_map(
            static fn (callable $solve): mixed => $solve($input['nums'], $input['k']),
            TopKFrequentElements::solutions(),
        );

        $this->assertCount(1, array_unique(array_map(serialize(...), $results)));
    }

    /** @return iterable<string, array{string, array<string, mixed>, mixed}> */
    public static function contractCases(): iterable
    {
        $contracts = new ContractRepository();

        foreach (array_keys(TopKFrequentElements::solutions()) as $approach) {
            foreach ($contracts->cases(TopKFrequentElements::SLUG) as $case) {
                yield "{$case['name']} ({$approach})" => [$approach, $case['input'], $case['expected']];
            }
        }
    }

    /** @return iterable<string, array{array<string, mixed>}> */
    public static function inputsOnly(): iterable
    {
        foreach ((new ContractRepository())->cases(TopKFrequentElements::SLUG) as $case) {
            yield $case['name'] => [$case['input']];
        }
    }
}
