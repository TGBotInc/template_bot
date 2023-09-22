from dataclasses import dataclass
from environs import Env


@dataclass
class VerificationBot:
    token: str


@dataclass
class DataBasePath:
    path: str


@dataclass
class Config:
    bot: VerificationBot
    db: DataBasePath


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)

    return Config(
        bot=VerificationBot(
            token=env('BOT_TOKEN')
        ),
        db=DataBasePath(
            path=env('PATH_DB')
        )
    )
