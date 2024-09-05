import logging
import threading
from typing import Any

from graphdatascience import GraphDataScience
from neo4j import GraphDatabase, Transaction
from neo4j.exceptions import ClientError, DatabaseError, TransientError

from .credentials import load_neo4j_credentials
from .schema import Query


class Neo4jOps:
    __instance = None

    def __init__(self) -> None:
        """
        neo4j utility functions
        """
        if Neo4jOps.__instance is not None:
            raise Exception("Singletone class! use `get_instance` method always.")
        else:
            self._neo4j_database_connect()
            Neo4jOps.__instance = self

    @staticmethod
    def get_instance():
        if Neo4jOps.__instance is None:
            with threading.Lock():
                if Neo4jOps.__instance is None:  # Double-checked locking
                    Neo4jOps()
        return Neo4jOps.__instance

    def _neo4j_database_connect(self) -> None:
        """
        connect to neo4j database and set the database driver it the class
        """
        creds = load_neo4j_credentials()

        url = creds["url"]
        auth = creds["auth"]
        self.db_name = creds["db_name"]

        self.neo4j_driver = GraphDatabase.driver(url, auth=auth, database=self.db_name)
        self.neo4j_driver.verify_connectivity()

        self.gds = GraphDataScience(url, auth)

    def _run_query(self, tx: Transaction, query: str, **kwargs) -> None:
        """
        handle neo4j queries in a transaction

        Parameters:
        -------------
        tx : neo4j.Transaction
            the transaction instance for neo4j python driver
        query : str
            the query to run for neo4j
        **kwargs : dict[str, Any]
            the parameters for the neo4j query
        """
        try:
            tx.run(query, kwargs)
        except TransientError as err:
            logging.error("Neo4j transient error!")
            logging.error(f"Code: {err.code}, message: {err.message}")
        except DatabaseError as err:
            logging.error("Neo4J database error")
            logging.error(f"Code: {err.code}, message: {err.message}")
        except ClientError as err:
            logging.error("Neo4j Client Error!")
            logging.error(f"Code: {err.code}, message: {err.message}")

    def run_queries_in_batch(
        self, queries: list[Query], message: str = "", session_batch: int = 30000
    ) -> None:
        """
        store data into neo4j using the given query list

        Parameters:
        ------------
        queries : list[neo4j_lib_py.schema.Query]
            list of tuples with lenght of 2. the first index is the neo4j query
            and the second index is the neo4j query parameters
            min length is 1
        message : str
            the message to be printed out
            default is nothing
        session_batch : int
            the number of queries to run in one session
            default is 30K transactions
        """
        try:
            # splitting the transactions
            queries_idx = list(range(len(queries)))[::session_batch]
            if len(queries_idx) > 1:
                logging.info(
                    f"{message} huge query count, doing operations in multi-session"
                )
            for session_number, index in enumerate(queries_idx):
                batch_queries = queries[index : index + session_batch]
                with self.neo4j_driver.session(database=self.db_name) as session:
                    with session.begin_transaction() as tx:
                        apoc_run_queries: str = ""
                        apoc_query_params: dict[str, Any] = {}
                        logging.info(
                            f"Neo4J Transaction session {message}"
                            f" {session_number + 1}/{len(queries_idx)}"
                        )

                        for query_idx, query_item in enumerate(batch_queries):
                            query = query_item.query
                            query_parameters = query_item.parameters

                            new_query = query
                            # updating the parameters to be unique
                            for param_idx, (key, value) in enumerate(
                                query_parameters.items()
                            ):
                                # creating a unique key for query parameter
                                # as we're going to merge all queries together
                                unique_key = f"{key}_{query_idx}_{param_idx}"
                                new_query = new_query.replace(
                                    f"${key}", "$" + unique_key
                                )

                                apoc_query_params[unique_key] = value

                            apoc_run_queries += f"{new_query}\n"

                        nested_param_dict: dict[str, Any] = {}

                        for key in apoc_query_params:
                            nested_param_dict[key.replace("$", "")] = f"${key}"

                        self._run_query(
                            tx,
                            f"""CALL apoc.cypher.runMany("{apoc_run_queries}", """
                            + f"{nested_param_dict})".replace("'", ""),
                            **apoc_query_params,
                        )
        except Exception as e:
            logging.error(f"Couldn't execute  Neo4J DB transaction, exception: {e}")
