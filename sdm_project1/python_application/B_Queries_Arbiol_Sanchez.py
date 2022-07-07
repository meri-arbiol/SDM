def three_most_cited_conference(conn):
    query = "MATCH (p2:Paper)-[r1:IS_PUBLISHED_IN]->(c:Conference)" \
            " WITH p2, r1, c, size(()-[:CITED_BY]->(p2)) AS counter" \
            " WITH c, p2.paper_ID, counter ORDER BY counter DESC" \
            " RETURN c, collect(p2.paper_ID)[0..3]"
    return conn.query(query)


def conference_community(conn):
    query = "match (a:Person)<-[au:AUTHORED_BY]-(paper:Paper)-[p:IS_PUBLISHED_IN]->(c:Conference) WITH a.author AS " \
            "author,c.conference as conference,count(DISTINCT c.edition) as edition Where edition>1 with author, " \
            "conference, edition ORDER BY edition return conference, collect(author) "
    return conn.query(query)


def h_index(conn):
    query = "match (a:Person)<-[au:AUTHORED_BY]-(p1:Paper)-[p:CITED_BY]->(p2:Paper) with a.author as author," \
            "p1.title as " \
            "paper,count(p2) as counter ORDER BY counter with author, collect(counter) as f with author, [x in range(1," \
            "size(f)) where f[x-1]>=x] as a UNWIND a as b return author,max(b) "
    return conn.query(query)


def impact_factor(conn):
    query = "match (p1:Paper)-[c:CITED_BY]->(p2:Paper)-[pu:IS_PUBLISHED_IN]->(v:Volume)-[i:IN]->(y:Year) " \
            "CALL{with v match (j:Journal)-[h:HAS]-(v1:Volume{volume_ID:v.volume_ID}) return j,v1} " \
            "with j.journal as journal, y.year as year, count(p1) as citations " \
            "match (p3:Paper)-[pu1:IS_PUBLISHED_IN]->(v2:Volume)-[i1:IN]->(y1:Year{year:toString(toInteger(year)-1)}) " \
            "CALL{with v2,journal match (j:Journal{journal:journal})-[h:HAS]-(v3:Volume{volume_ID:v2.volume_ID}) " \
            "return j,v3} " \
            "with citations,y1.year as year1, count(p3) as publications1, journal, year " \
            "match (p4:Paper)-[pu2:IS_PUBLISHED_IN]->(v4:Volume)-[i2:IN]->(y2:Year{year:toString(toInteger(year1)-1)}) " \
            "CALL{with v4,journal match (j:Journal{journal:journal})-[h:HAS]-(v5:Volume{volume_ID:v4.volume_ID}) " \
            "return j,v5} " \
            "return journal,year, toFloat(citations)/toFloat(publications1+count(p4)) as impactfactor"
    return conn.query(query)
