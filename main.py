import fastapi
import uvicorn

from data import redis_session
from views import register, admin, xml_oef, personality_pieces, search
from starlette.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    configure()
    uvicorn.run(app, host="127.0.0.1", port=8000)


def configure_redis():
    redis_session.global_init()


def configure_routes():
    app.include_router(xml_oef.router)
    app.include_router(personality_pieces.router)
    app.include_router(register.router)
    app.include_router(admin.router)
    app.include_router(search.router)


def configure():
    configure_redis()
    configure_routes()


if __name__ == '__main__':
    main()
else:
    configure()