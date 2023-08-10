import os

from dotenv import load_dotenv
from tc_neo4j_lib import Neo4jOps


def test_neo4j_env_variables():
    """
    test if the environment variables are loaded correctly
    """
    load_dotenv()

    protocol = os.getenv("NEO4J_PROTOCOL")
    host = os.getenv("NEO4J_HOST")
    port = os.getenv("NEO4J_PORT")
    db_name = os.getenv("NEO4J_DB")

    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    assert protocol is not None
    assert host is not None
    assert port is not None
    assert db_name is not None
    assert protocol is not None
    assert user is not None
    assert password is not None


def test_neo4j_connection():
    load_dotenv()

    protocol = os.getenv("NEO4J_PROTOCOL")
    host = os.getenv("NEO4J_HOST")
    port = os.getenv("NEO4J_PORT")

    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    db_name = os.getenv("NEO4J_DB")

    neo4j_ops = Neo4jOps()

    neo4j_ops.set_neo4j_db_info(
        neo4j_db_name=db_name,
        neo4j_protocol=protocol,
        neo4j_host=host,
        neo4j_port=port,
        neo4j_user=user,
        neo4j_password=password,
    )

    neo4j_ops.neo4j_database_connect()


def test_neo4j_data_insertion():
    load_dotenv()

    protocol = os.getenv("NEO4J_PROTOCOL")
    host = os.getenv("NEO4J_HOST")
    port = os.getenv("NEO4J_PORT")

    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    db_name = os.getenv("NEO4J_DB")

    neo4j_ops = Neo4jOps()

    neo4j_ops.set_neo4j_db_info(
        neo4j_db_name=db_name,
        neo4j_protocol=protocol,
        neo4j_host=host,
        neo4j_port=port,
        neo4j_user=user,
        neo4j_password=password,
    )

    neo4j_ops.neo4j_database_connect()

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    insertion_query = """
        CREATE (a:Account {userId: "acc1"})
            -[r:INTERACTED]->(b: Account {userId: "acc2"})
        """
    neo4j_ops.store_data_neo4j([insertion_query], message="SAMPLE INSERTION: ")

    # using the gds driver to retreive the data
    result = neo4j_ops.gds.run_cypher(
        """
        MATCH (a: Account) RETURN a.userId as userId
        """
    )

    print(result)
    assert all(["acc1", "acc2"] == result["userId"].values)
