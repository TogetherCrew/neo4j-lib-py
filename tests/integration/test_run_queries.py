from unittest import TestCase

from tc_neo4j_lib import Neo4jOps, Query


class TestNeo4jRunQueries(TestCase):
    def test_no_connection_raise_error(self):
        neo4j = Neo4jOps()
        queries = []
        for idx in range(5):
            query = Query(
                query="MERGE (a: {id: $id})",
                parameters={"id": idx},
            )
            queries.append(query)

        with self.assertRaises(ConnectionError):
            neo4j.run_queries_in_batch(queries)

    def test_run_single_query(self):
        neo4j = Neo4jOps()
        # initializing the connection
        neo4j.neo4j_database_connect()
        neo4j.neo4j_driver.execute_query("MATCH (n) DETACH DELETE (n)")

        query_count = 1

        queries = []
        for idx in range(query_count):
            query = Query(
                query="MERGE (:Person {id: $id})",
                parameters={"id": idx},
            )
            queries.append(query)

        neo4j.run_queries_in_batch(queries)

        records, _, _ = neo4j.neo4j_driver.execute_query(
            "MATCH (p:Person) RETURN p.id as id"
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 0)

    def test_run_multiple_queries(self):
        neo4j = Neo4jOps()
        # initializing the connection
        neo4j.neo4j_database_connect()
        neo4j.neo4j_driver.execute_query("MATCH (n) DETACH DELETE (n)")

        query_count = 5

        queries = []
        for idx in range(query_count):
            query = Query(
                query="MERGE (:Person {id: $id})",
                parameters={"id": idx},
            )
            queries.append(query)

        neo4j.run_queries_in_batch(queries)

        records, _, _ = neo4j.neo4j_driver.execute_query(
            "MATCH (p:Person) RETURN p.id as id"
        )
        self.assertEqual(len(records), query_count)
        self.assertEqual(records[0]["id"], 0)
        self.assertEqual(records[1]["id"], 1)
        self.assertEqual(records[2]["id"], 2)
        self.assertEqual(records[3]["id"], 3)
        self.assertEqual(records[4]["id"], 4)