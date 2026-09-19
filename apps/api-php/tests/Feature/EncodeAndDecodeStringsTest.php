<?php

declare(strict_types=1);

namespace Tests\Feature;

use NeetCode\Core\ArraysAndHashing\EncodeAndDecodeStrings;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use Tests\Support\ContractCases;
use Tests\TestCase;

/** `POST /problems/encode-and-decode-strings`, driven by the shared JSON contract. */
final class EncodeAndDecodeStringsTest extends TestCase
{
    private const URL = '/problems/encode-and-decode-strings';

    #[Test]
    #[DataProvider('solveCases')]
    public function it_solves_every_contract_case(string $approach, array $input, mixed $expected): void
    {
        $this->postJson(self::URL.'?approach='.$approach, $input)
            ->assertOk()
            ->assertJsonPath('result', $expected);
    }

    #[Test]
    #[DataProvider('validationCases')]
    public function it_422s_invalid_input(array $input, int $status): void
    {
        $this->postJson(self::URL, $input)
            ->assertStatus($status)
            ->assertJsonPath('error.type', 'validation_error');
    }

    /** @return iterable<string, array{string, array<string, mixed>, mixed}> */
    public static function solveCases(): iterable
    {
        return ContractCases::perApproach(EncodeAndDecodeStrings::SLUG, array_keys(EncodeAndDecodeStrings::solutions()));
    }

    /** @return iterable<string, array{array<string, mixed>, int}> */
    public static function validationCases(): iterable
    {
        return ContractCases::plain(EncodeAndDecodeStrings::SLUG, 'validationCases');
    }
}
