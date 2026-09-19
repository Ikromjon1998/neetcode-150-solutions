<?php

declare(strict_types=1);

namespace NeetCode\Core\Support;

use NeetCode\Core\Exceptions\UnknownApproachException;

/** Everything descriptive about a problem. Loaded from the shared JSON contract. */
final readonly class ProblemMeta
{
    /** @param list<Approach> $approaches */
    public function __construct(
        public int $id,
        public string $slug,
        public string $title,
        public Difficulty $difficulty,
        public Topic $topic,
        public string $summary,
        public array $approaches,
        public ?string $leetcodeUrl = null,
        public ?string $neetcodeUrl = null,
    ) {
    }

    /** @param array<string, mixed> $data */
    public static function fromArray(array $data): self
    {
        /** @var list<array<string, mixed>> $rawApproaches */
        $rawApproaches = $data['approaches'];

        return new self(
            id: (int) $data['id'],
            slug: (string) $data['slug'],
            title: (string) $data['title'],
            difficulty: Difficulty::from((string) $data['difficulty']),
            topic: Topic::from((string) $data['topic']),
            summary: (string) $data['summary'],
            approaches: array_map(Approach::fromArray(...), $rawApproaches),
            leetcodeUrl: isset($data['leetcodeUrl']) ? (string) $data['leetcodeUrl'] : null,
            neetcodeUrl: isset($data['neetcodeUrl']) ? (string) $data['neetcodeUrl'] : null,
        );
    }

    public function defaultApproach(): Approach
    {
        foreach ($this->approaches as $approach) {
            if ($approach->isDefault) {
                return $approach;
            }
        }

        return $this->approaches[0];
    }

    public function approach(string $key): Approach
    {
        foreach ($this->approaches as $approach) {
            if ($approach->key === $key) {
                return $approach;
            }
        }

        throw new UnknownApproachException(
            $this->slug,
            $key,
            array_map(static fn (Approach $a): string => $a->key, $this->approaches),
        );
    }

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        return [
            'id' => $this->id,
            'slug' => $this->slug,
            'title' => $this->title,
            'difficulty' => $this->difficulty->value,
            'topic' => $this->topic->value,
            'summary' => $this->summary,
            'approaches' => array_map(static fn (Approach $a): array => $a->toArray(), $this->approaches),
            'leetcodeUrl' => $this->leetcodeUrl,
            'neetcodeUrl' => $this->neetcodeUrl,
        ];
    }
}
