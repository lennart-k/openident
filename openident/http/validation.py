from collections.abc import Awaitable
from typing import Callable

from aiohttp import web
import voluptuous as vol

# Will be replaced by aiohttp.typedefs.Handler in the near future
Handler = Callable[[web.Request], Awaitable[web.StreamResponse]]


def validate_body(schema: vol.Schema) -> Callable[[Callable], Callable]:
    def decorator(
        handle: Handler,
    ) -> Handler:
        setattr(handle, "_schema_body", schema)
        return handle

    return decorator


def validate_query(schema: vol.Schema) -> Callable[[Callable], Callable]:
    def decorator(
        handle: Handler,
    ) -> Handler:
        setattr(handle, "_schema_query", schema)
        return handle

    return decorator


def validate_match(schema: vol.Schema) -> Callable[[Callable], Callable]:
    def decorator(
        handle: Handler,
    ) -> Handler:
        setattr(handle, "_schema_match", schema)
        return handle

    return decorator


@web.middleware
async def validation_middleware(
    request: web.Request, handler: Handler
) -> web.StreamResponse:
    orig_handler = request.match_info.handler
    if schema := getattr(orig_handler, "_schema_body", None):
        request["body"] = schema(await request.json())
    if schema := getattr(orig_handler, "_schema_query", None):
        request["query"] = schema(dict(request.query))
    if schema := getattr(orig_handler, "_schema_match", None):
        request["match"] = schema(dict(request.match_info))
    return await handler(request)
