from typing import Any


class Query:
    def __init__(self, query: str, parameters: dict[str, Any]) -> None:
        """
        A schema for passing neo4j query

        Parameters
        ------------
        query : str
            the actual query to pass to neo4j driver
        parameters : dict[str, Any]
            the neo4j parameters for the query itself
        """
        self.query = query
        self.parameters = parameters
