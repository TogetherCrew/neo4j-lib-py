from unittest import TestCase

from tc_neo4j_lib import Neo4jOps


class TestNeo4jConnect(TestCase):
    def test_neo4j_connect(self):
        neo4j = Neo4jOps()
        neo4j.neo4j_database_connect()
