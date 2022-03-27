import uvicorn

from streaming.settings import Settings


class ServerRunner:
    def __init__(self, settings=None):
        if not settings:
            self.settings = Settings()

    def run(self):
        uvicorn.run(
            "streaming.app:app",
            host=str(self.settings.HOST),
            port=self.settings.PORT,
            reload=self.settings.RELOAD,
        )


def run_server(settings=None):
    ServerRunner(settings).run()


if __name__ == "__main__":
    ServerRunner().run()
