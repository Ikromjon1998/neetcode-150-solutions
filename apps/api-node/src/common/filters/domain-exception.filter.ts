/**
 * One place where domain errors become HTTP status codes.
 *
 * `@neetcode/core` throws `NoSolutionError`; it has no idea that 404 exists. The translation
 * happens here and only here, which is why the same algorithms can sit behind a CLI, a queue
 * worker or these three web apps without modification.
 *
 * Status codes are pinned to match the FastAPI and Laravel apps exactly:
 *
 * | Situation                     | Status | `error.type`       |
 * |-------------------------------|--------|--------------------|
 * | Body fails validation         | 422    | `validation_error` |
 * | Unknown `?approach=`          | 422    | `unknown_approach` |
 * | Unknown problem slug          | 404    | `unknown_problem`  |
 * | Valid input, no answer exists | 404    | `no_solution`      |
 * | Approach not implemented yet  | 501    | `not_implemented`  |
 *
 * NestJS returns **400** for validation out of the box; FastAPI returns 422. Rather than
 * loosen the Python app, the `ValidationPipe` in `main.ts` is configured with
 * `errorHttpStatusCode: 422` and this filter reshapes the body to match.
 */

import {
  ArgumentsHost,
  Catch,
  ExceptionFilter,
  HttpException,
  HttpStatus,
  Logger,
} from "@nestjs/common";
import type { Response } from "express";
import {
  NoSolutionError,
  UnknownApproachError,
  UnknownProblemError,
  UnsolvedError,
} from "@neetcode/core";

interface ErrorBody {
  error: {
    type: string;
    message: string;
    problem?: string;
    details?: Array<Record<string, unknown>>;
  };
}

const UNPROCESSABLE_CONTENT = 422;

@Catch()
export class DomainExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(DomainExceptionFilter.name);

  catch(exception: unknown, host: ArgumentsHost): void {
    const response = host.switchToHttp().getResponse<Response>();
    const { status, body } = this.translate(exception);
    if (status >= 500) this.logger.error(exception);
    response.status(status).json(body);
  }

  private translate(exception: unknown): { status: number; body: ErrorBody } {
    // A stub was hit. This is the expected state of an unsolved exercise, not a bug.
    if (exception instanceof UnsolvedError) {
      return {
        status: HttpStatus.NOT_IMPLEMENTED,
        body: {
          error: {
            type: "not_implemented",
            message: `${exception.slug} / ${exception.approach} is an exercise you have not solved yet.`,
            problem: exception.slug,
            details: [
              { field: "approach", message: `Write your solution in ${exception.path}` },
            ],
          },
        },
      };
    }

    if (exception instanceof NoSolutionError) {
      return {
        status: HttpStatus.NOT_FOUND,
        body: { error: { type: "no_solution", message: exception.detail, problem: exception.slug } },
      };
    }

    if (exception instanceof UnknownProblemError) {
      return {
        status: HttpStatus.NOT_FOUND,
        body: {
          error: { type: "unknown_problem", message: exception.message, problem: exception.slug },
        },
      };
    }

    if (exception instanceof UnknownApproachError) {
      return {
        status: UNPROCESSABLE_CONTENT,
        body: {
          error: {
            type: "unknown_approach",
            message: exception.message,
            problem: exception.slug,
            details: [
              { field: "approach", message: `Available: ${exception.available.join(", ")}` },
            ],
          },
        },
      };
    }

    if (exception instanceof HttpException) {
      return this.fromHttpException(exception);
    }

    return {
      status: HttpStatus.INTERNAL_SERVER_ERROR,
      body: { error: { type: "internal_error", message: "Unexpected server error." } },
    };
  }

  /**
   * Reshape Nest's own exceptions into the shared envelope.
   *
   * `ValidationPipe` throws with a payload of `{ statusCode, message: string[], error }`.
   * The `message` array is what `class-validator` produced, one human-readable string per
   * failed constraint — we lift it into `error.details` so the shape matches FastAPI's
   * `{ field, message }` list as closely as the two libraries allow.
   */
  private fromHttpException(exception: HttpException): { status: number; body: ErrorBody } {
    const status = exception.getStatus();
    const payload = exception.getResponse();
    const isValidation = status === UNPROCESSABLE_CONTENT;

    if (typeof payload === "object" && payload !== null && "message" in payload) {
      const raw = (payload as { message: unknown }).message;
      const messages = Array.isArray(raw) ? raw.map(String) : [String(raw)];
      return {
        status,
        body: {
          error: {
            type: isValidation ? "validation_error" : "http_error",
            message: isValidation ? "The request body failed validation." : messages.join("; "),
            details: messages.map((message) => ({ field: fieldOf(message), message })),
          },
        },
      };
    }

    return {
      status,
      body: { error: { type: "http_error", message: exception.message } },
    };
  }
}

/**
 * `class-validator` messages start with the property name ("nums must contain at least 2
 * elements"), so the first word is a good-enough field hint. FastAPI reports the field
 * separately and does not need this; it is the price of the two libraries disagreeing.
 */
function fieldOf(message: string): string {
  return message.split(" ")[0] ?? "body";
}
