from tc_neo4j_lib import Neo4jOps


def test_neo4j_creds_set():
    """
    test if the random copmutations results is not None
    """
    neo4j_ops = Neo4jOps()

    db_name = "db_name"
    protocol = "bolt"
    host = "localhost"
    port = "port"

    user = "username"
    password = "password"

    neo4j_ops.set_neo4j_db_info(
        neo4j_db_name=db_name,
        neo4j_protocol=protocol,
        neo4j_host=host,
        neo4j_port=port,
        neo4j_user=user,
        neo4j_password=password,
    )

    url = f"{protocol}://{host}:{port}"

    assert neo4j_ops.neo4j_db_name == db_name
    assert neo4j_ops.neo4j_url == url
    assert neo4j_ops.neo4j_auth == (user, password)
