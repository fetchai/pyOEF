import fastapi
import uvicorn
from fastapi_utils.tasks import repeat_every

from data import redis_session
from views import register, admin

app = fastapi.FastAPI()


def main():
    configure()
    uvicorn.run(app, host="127.0.0.1", port=8000)


def configure_redis():
    redis_session.global_init()


def configure_routes():
    app.include_router(register.router)
    app.include_router(admin.router)


def configure():
    configure_redis()
    configure_routes()


if __name__ == '__main__':
    main()
else:
    configure()