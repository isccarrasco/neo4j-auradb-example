from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def find_requirements(self, person_name):
        with self.driver.session(database="neo4j") as session:
            result = session.read_transaction(self._find_and_return_requirement)
            for row in result:
                print("Found requirement: {row}".format(row=row))

    @staticmethod
    def _find_and_return_requirement(tx):
        query = (
            "MATCH (r:Requirements) "
            "RETURN r"
        )
        result = tx.run(query)
        return [row for row in result]


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    # uri = "neo4j+s://71388106.databases.neo4j.io"
    uri = "neo4j+s://15245744.databases.neo4j.io"
    user = "neo4j"
    password = "get_the_password"
    app = App(uri, user, password)
    app.find_requirements("Alice")
    app.close()
