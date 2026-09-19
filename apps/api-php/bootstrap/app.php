<?php

declare(strict_types=1);

use App\Support\ApiError;
use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
use Illuminate\Foundation\Http\Middleware\TrimStrings;
use Illuminate\Validation\ValidationException;
use NeetCode\Core\Exceptions\NoSolutionException;
use NeetCode\Core\Exceptions\UnknownApproachException;
use NeetCode\Core\Exceptions\UnknownProblemException;
use NeetCode\Core\Exceptions\UnsolvedException;
use Symfony\Component\HttpKernel\Exception\HttpExceptionInterface;

/**
 * One place where domain errors become HTTP status codes.
 *
 * `neetcode/core` throws `NoSolutionException`; it has no idea that 404 exists. The
 * translation happens here and only here, which is why the same algorithms can sit behind a
 * CLI, a queue worker or these three web apps without modification.
 *
 * Status codes are pinned to match the FastAPI and NestJS apps exactly:
 *
 * | Situation                     | Status | error.type         |
 * |-------------------------------|--------|--------------------|
 * | Body fails validation         | 422    | validation_error   |
 * | Unknown ?approach=            | 422    | unknown_approach   |
 * | Unknown problem slug          | 404    | unknown_problem    |
 * | Valid input, no answer exists | 404    | no_solution        |
 * | Approach not implemented yet  | 501    | not_implemented    |
 */

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        // Empty prefix: the paths must match the other two apps byte for byte.
        api: __DIR__.'/../routes/api.php',
        apiPrefix: '',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware): void {
        /*
         * Laravel applies TrimStrings and ConvertEmptyStringsToNull to every request by
         * default. Both were designed for HTML form posts, where a blank text input and an
         * absent one mean the same thing. In a JSON API they do not: ConvertEmptyStringsToNull
         * turns `{"s": ""}` into `{"s": null}`, so a perfectly valid empty-string payload
         * fails an `is_string` check and 422s — while the FastAPI and NestJS apps answer 200.
         *
         * Neither Pydantic nor class-validator has any equivalent behaviour. Removing them is
         * the only way the three apps can agree.
         */
        $middleware->remove([
            ConvertEmptyStringsToNull::class,
            TrimStrings::class,
        ]);
    })
    ->withExceptions(function (Exceptions $exceptions): void {
        // API-only app: never render an HTML error page, regardless of the Accept header.
        $exceptions->shouldRenderJsonWhen(static fn (): bool => true);

        // A stub was hit. This is the expected state of an unsolved exercise, not a bug.
        $exceptions->render(static fn (UnsolvedException $e) => ApiError::make(
            501,
            'not_implemented',
            "{$e->slug} / {$e->approach} is an exercise you have not solved yet.",
            problem: $e->slug,
            details: [['field' => 'approach', 'message' => "Write your solution in {$e->path}"]],
        ));

        $exceptions->render(static fn (NoSolutionException $e) => ApiError::make(
            404,
            'no_solution',
            $e->detail,
            problem: $e->slug,
        ));

        $exceptions->render(static fn (UnknownProblemException $e) => ApiError::make(
            404,
            'unknown_problem',
            $e->getMessage(),
            problem: $e->slug,
        ));

        $exceptions->render(static fn (UnknownApproachException $e) => ApiError::make(
            ApiError::UNPROCESSABLE_CONTENT,
            'unknown_approach',
            $e->getMessage(),
            problem: $e->slug,
            details: [['field' => 'approach', 'message' => 'Available: '.implode(', ', $e->available)]],
        ));

        /*
         * Reshape Laravel's own validation response.
         *
         * Out of the box it is `{"message": "...", "errors": {"field": ["..."]}}`. FastAPI
         * and NestJS both produce `{"error": {"type", "message", "details"}}`, so the errors
         * bag is flattened into the shared `details` list here.
         */
        $exceptions->render(static function (ValidationException $e) {
            $details = [];

            foreach ($e->errors() as $field => $messages) {
                foreach ($messages as $message) {
                    $details[] = ['field' => $field, 'message' => $message];
                }
            }

            return ApiError::make(
                ApiError::UNPROCESSABLE_CONTENT,
                'validation_error',
                'The request body failed validation.',
                details: $details,
            );
        });

        /*
         * `abort(422, ...)` from TwoSumRequest::prepareForValidation() arrives here as an
         * HttpException, not a ValidationException, so it needs its own shaping to keep the
         * envelope consistent.
         */
        $exceptions->render(static function (HttpExceptionInterface $e) {
            $status = $e->getStatusCode();

            return ApiError::make(
                $status,
                $status === ApiError::UNPROCESSABLE_CONTENT ? 'validation_error' : 'http_error',
                $status === ApiError::UNPROCESSABLE_CONTENT ? 'The request body failed validation.' : $e->getMessage(),
                details: $status === ApiError::UNPROCESSABLE_CONTENT
                    ? [['field' => 'body', 'message' => $e->getMessage()]]
                    : null,
            );
        });
    })->create();
