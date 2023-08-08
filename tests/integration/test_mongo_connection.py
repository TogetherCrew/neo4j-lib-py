import os

from dotenv import load_dotenv
from pymongo import MongoClient


def test_mongo_env_variables():
    """
    test if the environment variables are loaded correctly
    """
    load_dotenv()

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    assert host is not None
    assert port is not None
    assert user is not None
    assert password is not None
    assert db_name is not None


def test_mongo_connection():
    """
    test connecting to mongodb
    """
    load_dotenv()

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    mongodb_connection = f"mongodb://{user}:{password}@{host}:{port}/{db_name}"
    _ = MongoClient(host=mongodb_connection)
