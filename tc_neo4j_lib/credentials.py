import os

from dotenv import load_dotenv


def load_neo4j_credentials() -> dict[str, tuple[str, str] | str]:
    """
    load neo4j credentials

    Parameters
    ------------
    creds : dict[str, str]
        the neo4j credentials to use
        the keys are representing what the values are
        keys are `auth` ,`url` ,`db_name`
    """
    load_dotenv()

    protocol = os.getenv("NEO4J_PROTOCOL")
    host = os.getenv("NEO4J_HOST")
    port = os.getenv("NEO4J_PORT")
    db_name = os.getenv("NEO4J_DB")

    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    if (
        protocol is None
        or host is None
        or port is None
        or db_name is None
        or user is None
        or password is None
    ):
        raise ValueError("At least one of the neo4j credentials is missing!")

    url = f"{protocol}://{host}:{port}"

    creds: dict[str, tuple[str, str] | str] = {
        "auth": (user, password),
        "url": url,
        "db_name": db_name,
    }

    return creds
