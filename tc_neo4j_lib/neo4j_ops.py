import logging
from typing import Optional

from graphdatascience import GraphDataScience
from neo4j import GraphDatabase, Transaction
from neo4j.exceptions import ClientError, DatabaseError, TransientError


class Neo4jOps:
    def __init__(self) -> None:
        """
        neo4j utility functions
        """
        ## Neo4J credentials
        self.neo4j_dbName = None
        self.neo4j_url = None
        self.neo4j_auth = (None, None)
        self.neo4j_driver = None

    def set_neo4j_db_info(
        self,
        neo4j_db_name: Optional[str],
        neo4j_url: Optional[str],
        neo4j_user: Optional[str],
        neo4j_password: Optional[str],
    ) -> None:
        """
        Neo4j Database information setter

        Parameters:
        -------------
        neo4j_db_ame : str
            the database name to save the results in it
        neo4j_url : str
            the string of neo4j url
        neo4j_user : str
            neo4j username to connect
        neo4j_password : str
            neo4j database password
        """
        neo4j_auth = (neo4j_user, neo4j_password)

        self.neo4j_url = neo4j_url
        self.neo4j_auth = neo4j_auth
        self.neo4j_dbName = neo4j_db_name

    def neo4j_database_connect(self) -> None:
        """
        connect to neo4j database and set the database driver it the class
        """
        with GraphDatabase.driver(self.neo4j_url, auth=self.neo4j_auth) as driver:
            driver.verify_connectivity()

        self.neo4j_driver = driver
        self.gds = self.setup_gds()

    def setup_gds(self):
        gds = GraphDataScience(self.neo4j_url, self.neo4j_auth)

        return gds

    def _run_query(self, tx: Transaction, query: str) -> None:
        """
        handle neo4j queries in a transaction

        Parameters:
        -------------
        tx : neo4j.Transaction
            the transaction instance for neo4j python driver
        query : str
            the query to run for neo4j
        """
        try:
            tx.run(query)
        except TransientError as err:
            logging.error("Neo4j transient error!")
            logging.error(f"Code: {err.code}, message: {err.message}")
        except DatabaseError as err:
            logging.error("Neo4J database error")
            logging.error(f"Code: {err.code}, message: {err.message}")
        except ClientError as err:
            logging.error("Neo4j Client Error!")
            logging.error(f"Code: {err.code}, message: {err.message}")

    def store_data_neo4j(
        self, query_list: list[str], message: str = "", session_batch: int = 30000
    ) -> None:
        """
        store data into neo4j using the given query list

        Parameters:
        ------------
        query_list : list[str]
            list of strings to add data into neo4j
            min length is 1
        message : str
            the message to be printed out
            default is nothing
        session_batch : int
            the number of queries to run in one session
            default is 30K transactions
        """
        try:
            ## splitting the transactions
            queries_idx = list(range(len(query_list)))[::session_batch]
            if len(queries_idx) > 1:
                logging.info(
                    f"{message} huge query count, doing operations in multi-session"
                )
            for session_number, index in enumerate(queries_idx):
                queries = query_list[index : index + session_batch]
                with self.neo4j_driver.session(database=self.neo4j_dbName) as session:
                    with session.begin_transaction() as tx:
                        query_count = len(queries)
                        for idx, query in enumerate(queries):
                            msg_title = "Neo4J Transaction session "
                            msg_title += f"{session_number + 1}/{len(queries_idx)}"
                            logging.info(
                                f"{message} {msg_title}: Batch {idx + 1}/{query_count}"
                            )
                            # session.execute_write(self._run_query, query=query)
                            self._run_query(tx, query)
        except Exception as e:
            logging.error(f"Couldn't execute  Neo4J DB transaction, exception: {e}")
