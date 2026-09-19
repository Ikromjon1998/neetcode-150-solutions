<?php

declare(strict_types=1);

namespace App\Providers;

use Illuminate\Contracts\Foundation\CachesConfiguration;
use Illuminate\Support\ServiceProvider;
use NeetCode\Core\Contracts\ContractRepository;
use NeetCode\Core\Registry\ProblemRegistry;

/**
 * Wires the framework-free core package into Laravel's service container.
 *
 * This provider is the entire integration surface. Everything else in `app/` type-hints
 * `ProblemRegistry` and lets the container do the rest — which is Laravel's answer to
 * FastAPI's `Depends()` and NestJS's constructor injection, and arguably the most automatic
 * of the three: no decorator, no module declaration, just a type hint.
 */
final class NeetCodeServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        // Singletons: the contract JSON is parsed once per process, not once per request.
        $this->app->singleton(
            ContractRepository::class,
            fn (): ContractRepository => new ContractRepository(config('neetcode.contracts_dir')),
        );

        $this->app->singleton(ProblemRegistry::class, fn ($app): ProblemRegistry => new ProblemRegistry(
            config('neetcode.problems', []),
            $app->make(ContractRepository::class),
        ));
    }

    public function boot(): void
    {
        if (! config('neetcode.verify_on_boot', true)) {
            return;
        }

        // Skip while `artisan config:cache` is running — the container is mid-rebuild and the
        // config it would read is the one being replaced.
        if ($this->app instanceof CachesConfiguration && $this->app->configurationIsCached() === false
            && $this->app->runningInConsole() && $this->isCachingCommand()) {
            return;
        }

        $this->app->make(ProblemRegistry::class)->verify();
    }

    private function isCachingCommand(): bool
    {
        $command = $_SERVER['argv'][1] ?? '';

        return in_array($command, ['config:cache', 'optimize', 'package:discover'], true);
    }
}
