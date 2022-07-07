from neo4j import GraphDatabase
from A2_Load_Arbiol_Sanchez import *
from D_Recommender_Arbiol_Sanchez import *
from A3_Transformation_Arbiol_Sanchez import *

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query))
        except Exception as e:
            print(query)
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

    def delete_all(self):
        self.query("MATCH (n) DETACH DELETE n")

    def delete_nodes(self, node):
        self.query("MATCH (n:"+node+") delete n")

    def delete_edges(self, edge):
        self.query("MATCH ()-[e:"+edge+"]-() delete e")

    def create_graphdatabase(self):
        create_authors(self)
        create_articles(self)
        create_years(self)
        create_volumes(self)
        create_coauthors(self)
        create_conferences(self)
        create_journals(self)
        create_authored_by(self)
        create_cited_by(self)
        create_published_in(self)
        create_reviewed_by(self)
        create_has_in(self)
        create_topics(self)

    def transform(self):
        add_reviews(self)
        add_affiliations(self)

    def recommender(self):
        define_database_community(self)
        conference_to_community(self)
        return top_papers(self), gururs(self)