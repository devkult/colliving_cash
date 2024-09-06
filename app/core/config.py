from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    dialect: str
    driver: str
    username: str
    password: str
    host: str
    port: str
    database: str

    @property
    def url(self) -> str:
        return f"{self.dialect}+{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__", case_sensitive=False, extra="ignore"
    )

    db: DatabaseConfig


settings = Config()
