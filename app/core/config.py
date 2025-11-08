import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    db_name: str = os.getenv("db_name", "mydatabase")
    db_user_name: str = os.getenv("db_user_name", "postgres")
    db_password: str = os.getenv("db_password", "password")
    db_host: str = os.getenv("db_host", "localhost")
    db_port: int = int(os.getenv("db_port", 5432))

    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg2://{self.db_user_name}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


config = Config()
