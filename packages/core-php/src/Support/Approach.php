<?php

declare(strict_types=1);

namespace NeetCode\Core\Support;

/**
 * One implemented way of solving a problem, with its cost.
 *
 * `readonly class` (PHP 8.2) makes every property immutable in one word — the equivalent of
 * Python's `@dataclass(frozen=True)` and of TypeScript's `readonly` members, except that PHP
 * enforces it at runtime rather than only at compile time.
 */
final readonly class Approach
{
    public function __construct(
        public string $key,
        public string $name,
        /** Big-O time, e.g. "O(n log n)". */
        public string $time,
        /** Big-O auxiliary space. */
        public string $space,
        public ?string $note = null,
        /** Exactly one approach per problem sets this; used when no key is given. */
        public bool $isDefault = false,
    ) {
    }

    /** @param array<string, mixed> $data */
    public static function fromArray(array $data): self
    {
        return new self(
            key: (string) $data['key'],
            name: (string) $data['name'],
            time: (string) $data['time'],
            space: (string) $data['space'],
            note: isset($data['note']) ? (string) $data['note'] : null,
            isDefault: (bool) ($data['default'] ?? false),
        );
    }

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return [
            'key' => $this->key,
            'name' => $this->name,
            'time' => $this->time,
            'space' => $this->space,
            'note' => $this->note,
            'default' => $this->isDefault,
        ];
    }
}
