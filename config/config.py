from environs import Env
from dataclasses import dataclass


@dataclass
class BotConfig:
    token: str
    admin_ids: list[int]


@dataclass
class DbConfig:
    db_path: str = "config/main.db"


@dataclass
class Config:
    bot: BotConfig
    db: DbConfig


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        bot=BotConfig(
            token=env.str("BOT_TOKEN"),
            admin_ids=env.list("ADMIN_IDS", subcast=int)
        ),
        db=DbConfig()
    )