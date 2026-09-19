/**
 * Validates the `?approach=` query parameter for one specific problem.
 *
 * Instantiated per route with the slug baked in — `@Query("approach", new ApproachPipe(SLUG))`
 * — which is how a Nest pipe carries configuration. The FastAPI equivalent is a dependency
 * factory returning a closure; Laravel does it with a route-model-binding-style check in a
 * FormRequest. Three spellings of "validate this against a per-route whitelist".
 */

import { Injectable, PipeTransform } from "@nestjs/common";
import { approachesFor, defaultApproach, UnknownApproachError } from "@neetcode/core";

@Injectable()
export class ApproachPipe implements PipeTransform<string | undefined, string> {
  private readonly available: string[];
  private readonly fallback: string;

  constructor(private readonly slug: string) {
    this.available = approachesFor(slug);
    this.fallback = defaultApproach(slug).key;
  }

  transform(value: string | undefined): string {
    const approach = value ?? this.fallback;
    if (!this.available.includes(approach)) {
      throw new UnknownApproachError(this.slug, approach, this.available);
    }
    return approach;
  }
}
