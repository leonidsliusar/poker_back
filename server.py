"""server."""
import uvicorn
from dependency_injector.wiring import Provide
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket

from application import ApplicationContainer
from core.state.abstract.state import AbstractState

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/test")
async def websocket_endpoint(
        websocket: WebSocket,
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text("2")


def main() -> None:
    """."""
    uvicorn.run(
        "server:app",
        host="localhost",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
