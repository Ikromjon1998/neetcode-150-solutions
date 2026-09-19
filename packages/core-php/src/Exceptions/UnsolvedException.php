<?php

declare(strict_types=1);

namespace NeetCode\Core\Exceptions;

/**
 * This approach has not been implemented yet — it is still an exercise.
 *
 * Thrown by every stub. Distinct from a crash: it is the expected state of a freshly cloned
 * repository, and it carries the path of the file you are meant to edit. The app renders it as
 * `501 Not Implemented` rather than a 500, so hitting the endpoint tells you where to go.
 */
final class UnsolvedException extends NeetCodeException
{
    public function __construct(
        public readonly string $slug,
        public readonly string $approach,
        public readonly string $path,
    ) {
        parent::__construct("{$slug} / {$approach} is not implemented yet. Write it in {$path}");
    }
}
