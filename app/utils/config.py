# -------------------------------------------------------------------------------------------------------------
# Copyright (c) UCARE.AI Pte Ltd. All rights reserved.
# -------------------------------------------------------------------------------------------------------------
import os
from enum import Enum

from pydantic import BaseSettings


class Settings(BaseSettings):
    CHROMADB_HOST: str
    CHROMADB_PORT: str
    CHROMADB_COL_NAME: str
    EMBEDDING_MODEL: str

    OPENAI_API_KEY: str


class ProductionConfig(Settings):
    # it means that, every entry for Settings must
    # come from environment variables
    pass


# class DevelopmentConfig(Settings):
#     class Config:
#         env_file = "./config/dev.env"


def find_which_config():
    # if os.getenv("ENV"):  # there is DOMAIN name provided
    #     config = ProductionConfig()
    # else:
    config = ProductionConfig()

    # def func() -> Settings:
    #     return config

    # return func()
    return config


# configurations = find_which_config()


if __name__ == "__main__":
    print(find_which_config())
