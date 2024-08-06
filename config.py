import json

from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict


class Auth(BaseSettings):
    secret_key: str = ""
    algorithm: str = ""
    login: str = ""
    password: str = ""


def read_json(file_path: str = "t1_company/practice.json") -> list[dict[str, str]]:
    with open(file_path, "r") as f:
        json_data = json.load(f)
    return json_data


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      env_nested_delimiter='__',
                                      extra='ignore')
    auth: Auth
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    practices: list[dict[str, str]] = read_json()


settings: Settings = Settings()
