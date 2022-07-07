def node_similarity(conn):
    query = "MATCH(p1: Person {author: 'Douglas Walton'})<-[r1:AUTHORED_BY]-(p:Paper)-[r2:RELATED_TO]->(t1: Topic) " \
            "WITH " \
            "p1, collect(id(t1)) as point1 MATCH(p2: Person)<-[r3:AUTHORED_BY]-(p:Paper)-[r4:RELATED_TO]->(t2: Topic) " \
            "WHERE p1 <> p2 WITH p1, p2, point1, collect(id(t2)) as point2 RETURN p1.author AS from, p2.author as to, " \
            "gds.alpha.similarity.jaccard(point1, point2) as jaccard ORDER BY jaccard DESC LIMIT 20; "
    return conn.query(query)


def page_rank(conn):
    query = "CALL gds.graph.create('pagerank', 'Paper', 'CITED_BY') CALL gds.pageRank.stream('pagerank') YIELD nodeId, " \
            "score RETURN gds.util.asNode(nodeId).title AS name, score ORDER BY score DESC, name ASC limit 10 "

    return conn.query(query)
