<?php

declare(strict_types=1);

namespace Tests\Feature;

use NeetCode\Core\Registry\ProblemRegistry;
use PHPUnit\Framework\Attributes\Test;
use Tests\TestCase;

/** Endpoints that exist regardless of which problems are solved. */
final class HealthAndCatalogTest extends TestCase
{
    #[Test]
    public function it_reports_health(): void
    {
        $registry = $this->app->make(ProblemRegistry::class);

        $this->getJson('/health')
            ->assertOk()
            ->assertJsonPath('status', 'ok')
            ->assertJsonPath('runtime', 'php/laravel')
            ->assertJsonPath('problemsRegistered', count($registry->slugs()));
    }

    #[Test]
    public function it_lists_every_registered_problem(): void
    {
        $registry = $this->app->make(ProblemRegistry::class);
        $response = $this->getJson('/problems')->assertOk();

        $slugs = array_column($response->json(), 'slug');
        sort($slugs);
        $expected = $registry->slugs();
        sort($expected);

        $this->assertSame($expected, $slugs);

        foreach ($response->json() as $item) {
            $this->assertSame("/problems/{$item['slug']}", $item['endpoint']);
            $this->assertNotEmpty($item['approaches']);
        }
    }

    #[Test]
    public function it_returns_catalog_metadata_matching_the_contract(): void
    {
        $response = $this->getJson('/problems/two-sum')->assertOk();

        $response->assertJsonPath('id', 1)
            ->assertJsonPath('title', 'Two Sum')
            ->assertJsonPath('difficulty', 'easy')
            ->assertJsonPath('topic', 'arrays-and-hashing');

        $keys = array_column($response->json('approaches'), 'key');
        sort($keys);
        $this->assertSame(['brute-force', 'hash-map'], $keys);
    }

    #[Test]
    public function it_404s_an_unknown_problem(): void
    {
        $this->getJson('/problems/not-a-real-problem')
            ->assertNotFound()
            ->assertJsonPath('error.type', 'unknown_problem');
    }
}
