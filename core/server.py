import asyncio
import uvloop
import websockets

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def handler(websocket):
    while True:
        message = await websocket.recv()
        if message:
            print(f"from port{websocket.port}: {message}")


class Server:
    _host: str = "localhost"
    _port: int = 8000

    async def run(self):
        async with websockets.serve(handler, self._host, self._port):
            await asyncio.Future()


server = Server()


async def main():
    try:
        await server.run()
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down servers...")
