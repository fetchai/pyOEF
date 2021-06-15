import fastapi
import uvicorn

from views import register

app = fastapi.FastAPI()


def main():
    configure()
    uvicorn.run(app, host="127.0.0.1", port=8000)


def configure_routes():
    app.include_router(register.router)
    # app.include_router(book.router)


def configure():
    configure_routes()


if __name__ == '__main__':
    main()
else:
    configure()