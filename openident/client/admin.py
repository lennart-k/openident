import asyncio
import json
from typing import Optional
from uuid import UUID

from aiohttp import web
import voluptuous as vol

from openident.http.error_handler import error_handler
from openident.http.validation import (validate_body, validate_match,
                                       validate_query, validation_middleware)

from .store import ClientStore

__all__ = ["AdminAPI"]


class AdminAPI:
    def __init__(
        self, store: ClientStore, loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        self._store = store
        self._loop = loop or asyncio.get_event_loop()

        self.app = web.Application(
            loop=loop, middlewares=[error_handler, validation_middleware]
        )
        self.app.router.add_route("POST", "", self.handle_post_client)
        self.app.router.add_route("GET", "", self.handle_get_clients)
        self.app.router.add_route("GET", "/{id}", self.handle_get_client)
        self.app.router.add_route("PATCH", "/{id}", self.handle_update_client)
        self.app.router.add_route("DELETE", "/{id}", self.handle_delete_client)

    @validate_body(
        vol.Schema(
            {
                "name": str,
                vol.Optional("scope", default=list): [str],
                vol.Optional("redirect_uris", default=list): [str],
            }
        )
    )
    async def handle_post_client(self, req: web.Request) -> web.Response:
        client = await self._store.create_client(**req["body"])

        return web.Response(
            body=client.to_json(), content_type="application/json", status=201
        )

    @validate_body(
        vol.Schema(
            {
                vol.Optional("name"): str,
                vol.Optional("scope"): [str],
                vol.Optional("redirect_uris"): [str],
            }
        )
    )
    @validate_match(vol.Schema({"id": vol.Coerce(UUID)}))
    async def handle_update_client(self, req: web.Request) -> web.Response:
        client = await self._store.update_client(req["match"]["id"], **req["body"])
        return web.Response(
            body=json.dumps(client.as_dict(), indent=4, sort_keys=True),
            content_type="application/json",
        )

    @validate_match(vol.Schema({"id": vol.Coerce(UUID)}))
    async def handle_delete_client(self, req: web.Request) -> web.Response:
        client_id = req["match"]["id"]
        await self._store.delete_client(client_id)
        return web.Response(status=204)

    @validate_query(
        vol.Schema(
            {
                vol.Optional("limit", default=None): vol.Any(
                    None, vol.All(vol.Coerce(int), vol.Clamp(min=0))
                ),
                vol.Optional("offset", default=None): vol.Any(
                    None, vol.All(vol.Coerce(int), vol.Clamp(min=0))
                ),
            }
        )
    )
    async def handle_get_clients(self, req: web.Request) -> web.Response:
        clients = await self._store.get_clients(**req["query"])
        out = [client.as_dict() for client in clients]
        return web.Response(
            body=json.dumps(out, indent=4, sort_keys=True),
            content_type="application/json",
        )

    async def handle_get_client(self, req: web.Request) -> web.Response:
        client_id = UUID(req.match_info["id"])
        client = await self._store.get_client(client_id)
        return web.Response(
            body=json.dumps(client.as_dict(), indent=4, sort_keys=True),
            content_type="application/json",
        )
