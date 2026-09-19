<?php

declare(strict_types=1);

use App\Http\Controllers\CatalogController;
use App\Http\Controllers\HealthController;
use App\Problems\ContainsDuplicate\ContainsDuplicateController;
use App\Problems\EncodeAndDecodeStrings\EncodeAndDecodeStringsController;
use App\Problems\GroupAnagrams\GroupAnagramsController;
use App\Problems\LongestConsecutiveSequence\LongestConsecutiveSequenceController;
use App\Problems\ProductOfArrayExceptSelf\ProductOfArrayExceptSelfController;
use App\Problems\TopKFrequentElements\TopKFrequentElementsController;
use App\Problems\TwoSum\TwoSumController;
use App\Problems\ValidAnagram\ValidAnagramController;
use App\Problems\ValidSudoku\ValidSudokuController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API routes
|--------------------------------------------------------------------------
|
| Registered with an empty prefix (see bootstrap/app.php) so the paths match the FastAPI and
| NestJS apps exactly — `/problems/two-sum`, not `/api/problems/two-sum`. That is the whole
| point of this repo: the same request against three runtimes.
|
| Order matters. The concrete problem routes are declared before `/problems/{slug}` so the
| catch-all never swallows one.
|
| ADD NEW PROBLEM ROUTES in the group below. `make new-problem` inserts the line.
|
*/

Route::get('/health', HealthController::class);

Route::prefix('problems')->group(function (): void {
    // --- problem endpoints (one line per problem) ---
    Route::post('/encode-and-decode-strings', EncodeAndDecodeStringsController::class);
    Route::post('/valid-sudoku', ValidSudokuController::class);
    Route::post('/group-anagrams', GroupAnagramsController::class);
    Route::post('/top-k-frequent-elements', TopKFrequentElementsController::class);
    Route::post('/longest-consecutive-sequence', LongestConsecutiveSequenceController::class);
    Route::post('/product-of-array-except-self', ProductOfArrayExceptSelfController::class);
    Route::post('/contains-duplicate', ContainsDuplicateController::class);
    Route::post('/valid-anagram', ValidAnagramController::class);
    Route::post('/two-sum', TwoSumController::class);

    // --- catalog (must stay last: {slug} matches anything) ---
    Route::get('/', [CatalogController::class, 'index']);
    Route::get('/{slug}', [CatalogController::class, 'show']);
});
