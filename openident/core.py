import asyncio
import logging

from aiohttp import web

from openident.client.admin import AdminAPI as ClientAdmin
from openident.persistence.memory import MemoryClientStore

logging.getLogger().setLevel(logging.DEBUG)


def run() -> None:
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    # address = "postgresql://openident:openident@localhost/openident"
    # app.add_subapp("/clients", AdminAPI(loop=loop,
    #                store=SQLPersister(address)).app)
    app.add_subapp("/clients", ClientAdmin(loop=loop, store=MemoryClientStore()).app)
    # app.add_subapp("/users", AdminAPI(loop=loop, store=MemoryClientStore()).app)
    web.run_app(app)
