from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    db_dialect: str
    db_driver: str
    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_database: str

    model_config = SettingsConfigDict(
        env_file="path_to_.env"
    )
    # TODO: Поставить норм путь ;)


settings = Config()
