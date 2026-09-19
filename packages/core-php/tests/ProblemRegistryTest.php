<?php

declare(strict_types=1);

namespace NeetCode\Core\Tests;

use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Exceptions\UnknownProblemException;
use NeetCode\Core\Registry\ProblemRegistry;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

/**
 * Registry-level guards.
 *
 * These run against every problem in the package, so they keep paying off as the repo grows:
 * problem 150 is checked by exactly the same tests as problem 1.
 */
final class ProblemRegistryTest extends TestCase
{
    private ProblemRegistry $registry;

    protected function setUp(): void
    {
        $this->registry = ProblemRegistry::default();
    }

    #[Test]
    public function it_agrees_with_the_json_contracts(): void
    {
        $this->registry->verify();
        $this->addToAssertionCount(1);
    }

    #[Test]
    public function it_registers_two_sum(): void
    {
        $this->assertContains('two-sum', $this->registry->slugs());
    }

    #[Test]
    public function it_orders_problems_by_leetcode_id(): void
    {
        $ids = array_map(static fn ($meta): int => $meta->id, $this->registry->all());
        $sorted = $ids;
        sort($sorted);

        $this->assertSame($sorted, $ids);
    }

    #[Test]
    #[DataProvider('slugProvider')]
    public function it_declares_at_most_one_default_approach(string $slug): void
    {
        $meta = ProblemRegistry::default()->meta($slug);
        $defaults = array_filter($meta->approaches, static fn ($a): bool => $a->isDefault);

        $this->assertLessThanOrEqual(1, count($defaults));
    }

    #[Test]
    #[DataProvider('slugProvider')]
    public function it_resolves_a_default_approach_without_an_explicit_key(string $slug): void
    {
        $this->assertIsCallable(ProblemRegistry::default()->solution($slug));
    }

    #[Test]
    public function it_throws_for_an_unregistered_slug(): void
    {
        $this->expectException(UnknownProblemException::class);
        $this->registry->solution('does-not-exist');
    }

    #[Test]
    public function it_lists_the_available_approaches_when_the_key_is_wrong(): void
    {
        try {
            $this->registry->solution('two-sum', 'quantum');
            $this->fail('Expected UnknownApproachException');
        } catch (UnknownApproachException $e) {
            $available = $e->available;
            $expected = $this->registry->approaches('two-sum');
            sort($available);
            sort($expected);

            $this->assertSame($expected, $available);
        }
    }

    /** @return iterable<string, array{string}> */
    public static function slugProvider(): iterable
    {
        foreach (ProblemRegistry::default()->slugs() as $slug) {
            yield $slug => [$slug];
        }
    }
}
