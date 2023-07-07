from os import getenv

from dotenv import load_dotenv


class SingletonMeta(type):
    """
    Singleton class for instantiate only one time the configs.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    load_dotenv()
    TOKEN = getenv("TOKEN")
    CHANNEL_ID = getenv("CHANNEL_ID")
    ROLE_NAME = getenv("ROLE_NAME")
    ENVIRONMENT = getenv("ENVIRONMENT")
    INTERVAL_MINUTES = getenv("INTERVAL_MINUTES")
