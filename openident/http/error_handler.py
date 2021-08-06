import asyncio
from collections.abc import Awaitable, Callable
import json
from traceback import print_exc

from aiohttp import web

# Will be replaced by aiohttp.typedefs.Handler in the near future
Handler = Callable[[web.Request], Awaitable[web.StreamResponse]]


@web.middleware
async def error_handler(request: web.Request, handler: Handler) -> web.StreamResponse:
    try:
        return await handler(request)
    except web.HTTPException:  # pylint: disable=try-except-raise
        raise
    except asyncio.CancelledError:  # pylint: disable=try-except-raise
        raise
    except Exception as e:  # pylint: disable=broad-except
        print_exc()

        return web.Response(
            body=json.dumps(
                {
                    "error": type(e).__name__,
                    "message": str(e),
                }
            ),
            status=500,
            content_type="application/json",
        )
