/**
 * `@IsMatrix("int" | "string")` — validate a rectangular 2-D array of primitives.
 *
 * `class-validator`'s `each: true` descends exactly one level, so `@IsInt({ each: true })` on a
 * `number[][]` checks whether each *row* is an integer and fails every time. `@ValidateNested`
 * is the documented answer, but it needs a class per nested level, and a row of primitives has
 * no class to point at.
 *
 * Pydantic handles `list[list[StrictInt]]` natively, and Laravel handles it with a `field.*.*`
 * wildcard rule. This decorator is what the TypeScript side needs to reach parity — a small
 * but concrete example of the three validation libraries having genuinely different reach.
 */

import {
  buildMessage,
  registerDecorator,
  type ValidationArguments,
  type ValidationOptions,
} from "class-validator";

export type MatrixElement = "int" | "string";

const CHECKS: Record<MatrixElement, (value: unknown) => boolean> = {
  int: (value) => typeof value === "number" && Number.isInteger(value),
  string: (value) => typeof value === "string",
};

export function isMatrix(value: unknown, element: MatrixElement): boolean {
  if (!Array.isArray(value)) return false;
  const check = CHECKS[element];
  return value.every((row) => Array.isArray(row) && row.every(check));
}

export function IsMatrix(
  element: MatrixElement,
  options?: ValidationOptions,
): PropertyDecorator {
  return function decorate(target: object, propertyName: string | symbol): void {
    registerDecorator({
      name: "isMatrix",
      target: target.constructor,
      propertyName: propertyName as string,
      constraints: [element],
      options,
      validator: {
        validate: (value: unknown, args: ValidationArguments) =>
          isMatrix(value, args.constraints[0] as MatrixElement),
        defaultMessage: buildMessage(
          (prefix) => `${prefix}$property must be a 2-D array of ${element}`,
          options,
        ),
      },
    });
  };
}
