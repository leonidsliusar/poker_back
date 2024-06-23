"""src.routes."""
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect
from src.application import ApplicationContainer
from src.core.models.models import RequestModel
from src.dispatcher import Dispatcher

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/holdem")
@inject
async def websocket_endpoint(
        websocket: WebSocket,
        dispatch: Dispatcher = Depends(Provide[ApplicationContainer.dispatcher_holdem]),
):
    await manager.connect(websocket)
    try:
        while True:
            request = await websocket.receive_json()
            request_obj = RequestModel.model_validate(request)
            result = dispatch.exec(request_obj)
            if result:
                await websocket.send_json(result.model_dump())
    except WebSocketDisconnect:
        manager.disconnect(websocket)
