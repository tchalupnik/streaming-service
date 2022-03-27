from typing import Optional, Dict, Any

from pydantic import AnyUrl, BaseSettings, SecretStr, validator
from yarl import URL


def get_connection_string(
    uri: str,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    port: Optional[int] = None,
):
    url = URL(uri).with_user(username).with_password(password)
    if port is not None:
        url = url.with_port(port)

    return url.human_repr()


class AmqpDsn(AnyUrl):
    allowed_schemes = {"amqp", "amqps"}
    user_required = True


class MQSettings(BaseSettings):
    MQ_URL: AnyUrl
    MQ_USERNAME: str
    MQ_PASSWORD: SecretStr

    AMQP_URI: Optional[AmqpDsn] = None
    DEFAULT_EXCHANGE_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("AMQP_URI", pre=True, allow_reuse=True)
    def assemble_amqp_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        rv = get_connection_string(
            values["MQ_URL"],
            username=values["MQ_USERNAME"],
            password=values["MQ_PASSWORD"].get_secret_value(),
        )
        return rv
