"""Status codes this app pins by hand.

Starlette renamed `HTTP_422_UNPROCESSABLE_ENTITY` to `HTTP_422_UNPROCESSABLE_CONTENT` (RFC
9110 changed the reason phrase), and referencing either name ties the app to a Starlette
version range for no benefit. 422 is 422. Everything else still comes from `fastapi.status`.
"""

UNPROCESSABLE_CONTENT = 422
