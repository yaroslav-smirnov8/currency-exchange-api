from aiohttp import web

from app import create_app


def main() -> None:
    app = create_app()
    web.run_app(app, port=8080)


if __name__ == "__main__":
    main()
