<?php

declare(strict_types=1);

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web routes
|--------------------------------------------------------------------------
|
| This app is an API; there are no views. The root route just points a browser at the
| interesting parts.
|
*/

Route::get('/', fn (): array => [
    'name' => 'NeetCode API (PHP / Laravel)',
    'catalog' => url('/problems'),
    'health' => url('/health'),
]);
