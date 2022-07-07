from Neo4jconnect import *
from B_Queries_Arbiol_Sanchez import *
from C_Graph_algorithms_Arbiol_Sanchez import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #Connection to Neo4j
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="1234")
    #A2 load
    conn.create_graphdatabase()
    #A3 Evolve
    conn.transform()
    #B Queries
    most_cited_papers=three_most_cited_conference(conn)
    community=conference_community(conn)
    h=h_index(conn)
    factor=impact_factor(conn)
    #C Algorithms
    similarity=node_similarity(conn)
    rank=page_rank(conn)
    #D Recommender
    top, guru = conn.recommender()
    conn.close()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
