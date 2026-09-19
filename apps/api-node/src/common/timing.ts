/**
 * A stopwatch scoped to the algorithm call only.
 *
 * `process.hrtime.bigint()` rather than `Date.now()`: it is monotonic and nanosecond-
 * resolution, which matters because an O(n) solution over six elements finishes in well
 * under a millisecond — `Date.now()` would report a flat 0 for every request.
 */
export function timed<T>(fn: () => T): { result: T; elapsedMicros: number } {
  const start = process.hrtime.bigint();
  const result = fn();
  return { result, elapsedMicros: Number((process.hrtime.bigint() - start) / 1000n) };
}
