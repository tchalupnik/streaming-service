from .settings import MQSettings


class MQBase:
    def __init__(self, settings: MQSettings = None):
        if not settings:
            settings = MQSettings()
        self.settings = settings
