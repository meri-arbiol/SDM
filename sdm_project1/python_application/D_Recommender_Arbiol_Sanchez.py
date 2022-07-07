def define_database_community(conn):
    community = "CREATE (:Community{name:'Database community'})"
    relation = "match (t:Topic), (c:Community) " \
               "where t.topic in ['Data Managment', 'Indexing', 'Data Modelling', 'Big Data'," \
               "'Data Processing', 'Data Storage', 'Data Queryng'] and c.name='Database community' with t, c " \
               "CREATE (t)-[:is_in]->(c) return t,c"
    conn.query(community)
    conn.query(relation)


def conference_to_community(conn):
    query = "match (co:Conference)<-[pu:IS_PUBLISHED_IN]-(p:Paper) with  co as conference, toFloat(count(p)) as " \
            "papers_published " \
            "match (co1:Conference)<-[pu1:IS_PUBLISHED_IN]-(p1:Paper)-[r1:RELATED_TO]->(t1:Topic)-[i1:is_in]->(" \
            "c1:Community) " \
            "where co1.conference_ID=conference.conference_ID " \
            "with c1, co1, toFloat(count(p1)) as papers_comm, papers_published where papers_comm/papers_published>0.9 " \
            "CREATE (co1)-[B:BELONGS_TO]->(c1)"

    query2 = "match (j:Journal)-[h:HAS]->(v:Volume)<-[pu:IS_PUBLISHED_IN]-(p:Paper) with  j as journal, " \
             "toFloat(count(p)) as papers_published " \
             "match (j1:Journal)-[h1:HAS]->(v1:Volume)<-[pu1:IS_PUBLISHED_IN]-(p1:Paper)-[r1:RELATED_TO]->(" \
             "t1:Topic)-[i1:is_in]->(c1:Community) " \
             "where j1.journal_ID=journal.journal_ID with c1, j1, toFloat(count(p1)) as papers_comm, papers_published " \
             "where " \
             "papers_comm/papers_published>0.9 " \
             "CREATE (j1)-[b:BELONGS_TO]->(c1) return j1,b,c1"
    conn.query(query)
    conn.query(query2)


def top_papers(conn):
    papers = "CALL gds.graph.create.cypher('pagerank_sectionD','MATCH(p:Paper)-[:RELATED_TO]->(t:Topic)-[:is_in]->(" \
             "c:Community) WHERE c.name = 'Database community' RETURN distinct id(p) AS id', 'MATCH(c1:Community)<-[" \
             ":is_in]-(t1:Topic)<-[:RELATED_TO]-(p1:Paper)-[:CITED_BY]->(p2:Paper)-[:RELATED_TO]->(t2:Topic)-[" \
             ":is_in]->(c2:Community) WHERE c1.name = 'Database community' AND c2.name = 'Database community' RETURN " \
             "id(p1) AS source, id(p2) AS target') CALL gds.pageRank.stream('pagerank_sectionD') YIELD nodeId, " \
             "score RETURN gds.util.asNode(nodeId).title AS name, score ORDER BY score DESC limit 100 "
    return conn.query(conn)


def gururs(conn):
    guru = "CALL gds.pageRank.stream('pagerank_sectionD') YIELD nodeId, score WITH gds.util.asNode(nodeId).paper_ID AS " \
           "paperid_list, score ORDER BY score DESC limit 100 WITH collect(paperid_list) as list MATCH (a:Person)<-[" \
           ":AUTHORED_BY]-(p:Paper) MATCH (a:Person)<-[:AUTHORED_BY]-(p1:Paper) WHERE (p.paper_ID IN list) AND (" \
           "p1.paper_ID IN list) AND (p.paper_ID<>p1.paper_ID) RETURN distinct a.author as gurus_name "
    return conn.query(guru)
