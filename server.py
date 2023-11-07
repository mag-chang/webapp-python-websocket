#!/usr/bin/env python

import asyncio
from websockets.server import serve

async def echo(websocket):
    for i in range(10):
        await websocket.send(f"Hello Web socket! [{i}]")
        await asyncio.sleep(5.0)

async def main():
    async with serve(echo, "0.0.0.0", 8000):
        await asyncio.Future()  # run forever

asyncio.run(main())
