"""src.server."""
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.application import ApplicationContainer
from src.routes import router

app = FastAPI()
app.include_router(router)
container = ApplicationContainer()
app._state = container

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main() -> None:
    """."""
    uvicorn.run(
        f"{__name__}:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
