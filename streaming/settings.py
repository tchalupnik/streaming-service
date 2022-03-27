from typing import Union

from pydantic import AnyUrl, BaseSettings, IPvAnyAddress


class Settings(BaseSettings):
    HOST: Union[AnyUrl, IPvAnyAddress] = "0.0.0.0"
    PORT: int = 8080
    RELOAD: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
