<?php

declare(strict_types=1);

namespace Tests\Feature;

use NeetCode\Core\ArraysAndHashing\TwoSum;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use Tests\Support\ContractCases;
use Tests\TestCase;

/**
 * `POST /problems/two-sum`, driven by the shared JSON contract.
 *
 * The identical case list is asserted by `apps/api-python/tests/test_two_sum.py` and by
 * `apps/api-node/test/two-sum.e2e.spec.ts`. If the three apps ever disagree about a payload,
 * one of the three suites goes red.
 */
final class TwoSumTest extends TestCase
{
    private const URL = '/problems/two-sum';

    #[Test]
    #[DataProvider('solveCases')]
    public function it_solves_every_contract_case(string $approach, array $input, array $expected): void
    {
        $this->postJson(self::URL.'?approach='.$approach, $input)
            ->assertOk()
            ->assertJsonPath('result', $expected)
            ->assertJsonPath('problem', TwoSum::SLUG)
            ->assertJsonPath('approach.key', $approach)
            ->assertJsonPath('input', $input)
            ->assertJson(fn ($json) => $json->has('elapsedMicros')->etc());
    }

    #[Test]
    #[DataProvider('inputsOnly')]
    public function it_uses_the_default_approach_when_the_query_is_omitted(array $input): void
    {
        $this->postJson(self::URL, $input)
            ->assertOk()
            ->assertJsonPath('approach.key', 'hash-map');
    }

    #[Test]
    #[DataProvider('validationCases')]
    public function it_422s_invalid_input(array $input, int $status): void
    {
        $this->postJson(self::URL, $input)
            ->assertStatus($status)
            ->assertJsonPath('error.type', 'validation_error')
            ->assertJson(fn ($json) => $json->has('error.details')->etc());
    }

    #[Test]
    #[DataProvider('noSolutionCases')]
    public function it_404s_when_no_pair_exists(array $input): void
    {
        $this->postJson(self::URL, $input)
            ->assertNotFound()
            ->assertJsonPath('error.type', 'no_solution');
    }

    #[Test]
    public function it_422s_an_unknown_approach(): void
    {
        $this->postJson(self::URL.'?approach=nope', ['nums' => [2, 7], 'target' => 9])
            ->assertStatus(422)
            ->assertJsonPath('error.type', 'unknown_approach');
    }

    #[Test]
    public function it_rejects_an_unexpected_field(): void
    {
        $this->postJson(self::URL, ['nums' => [2, 7], 'target' => 9, 'targett' => 9])
            ->assertStatus(422);
    }

    /** @return iterable<string, array{string, array<string, mixed>, list<int>}> */
    public static function solveCases(): iterable
    {
        return ContractCases::perApproach(TwoSum::SLUG, array_keys(TwoSum::solutions()));
    }

    /** @return iterable<string, array{array<string, mixed>, mixed}> */
    public static function inputsOnly(): iterable
    {
        foreach (ContractCases::plain(TwoSum::SLUG) as $name => [$input, $_]) {
            yield $name => [$input];
        }
    }

    /** @return iterable<string, array{array<string, mixed>, int}> */
    public static function validationCases(): iterable
    {
        return ContractCases::plain(TwoSum::SLUG, 'validationCases');
    }

    /** @return iterable<string, array{array<string, mixed>}> */
    public static function noSolutionCases(): iterable
    {
        foreach (ContractCases::plain(TwoSum::SLUG, 'notFoundCases') as $name => [$input, $_]) {
            yield $name => [$input];
        }
    }
}
