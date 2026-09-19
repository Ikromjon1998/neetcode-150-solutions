<?php

declare(strict_types=1);

use NeetCode\Core\Registry\DefaultProblems;

return [

    /*
    |--------------------------------------------------------------------------
    | Registered problems
    |--------------------------------------------------------------------------
    |
    | Every class here must implement NeetCode\Core\Contracts\ProblemDefinition.
    | NeetCodeServiceProvider builds the ProblemRegistry singleton from this list.
    |
    | This is a plain array on purpose: `php artisan config:cache` compiles the whole file
    | into a single cached PHP array at deploy time, so a production request never scans a
    | directory or reflects over a class to find a solution. The FastAPI app does discover its
    | problems by walking the package — cheaper to write, but it cannot be frozen this way.
    |
    | ADD NEW PROBLEM CLASSES HERE (or in DefaultProblems, which this defers to).
    |
    */

    'problems' => DefaultProblems::all(),

    /*
    |--------------------------------------------------------------------------
    | Contracts directory
    |--------------------------------------------------------------------------
    |
    | Where packages/contracts/problems lives. Leave null to let ContractRepository find it by
    | walking up the tree; set NEETCODE_CONTRACTS_DIR in a container where the repo layout
    | does not survive the build.
    |
    */

    'contracts_dir' => env('NEETCODE_CONTRACTS_DIR'),

    /*
    |--------------------------------------------------------------------------
    | Verify registry on boot
    |--------------------------------------------------------------------------
    |
    | Fail the boot if a contract declares an approach nobody implemented. Disable it only if
    | you have a deliberate reason — a container that cannot serve correct answers should
    | never pass its readiness check.
    |
    */

    'verify_on_boot' => (bool) env('NEETCODE_VERIFY_ON_BOOT', true),

];
