def add_reviews(conn):
    query1 = "LOAD CSV WITH HEADERS FROM 'file:///reviewers_with_review.csv' AS line FIELDTERMINATOR ',' with line MATCH " \
             "(p:Paper{paper_ID:line['Article']})-[e:REVIEWED_BY]->(a:Person{author_ID:line['Reviewer']}) SET " \
             "e.review=line['abstract'], e.decision=line['Decision'] return e.review, e.decision"
    return conn.query(query1)


def add_affiliations(conn):
    affiliations = "LOAD CSV WITH HEADERS FROM 'file:///affiliations.csv' AS line FIELDTERMINATOR ',' with line " \
                   "CREATE (:Affiliation{aff_ID:line['ID'], Name: line['name']}) "
    relations = "LOAD CSV WITH HEADERS FROM 'file:///affiliated_in.csv' AS line FIELDTERMINATOR ',' with line" \
                " MERGE(p:Person{author_ID:line.author_ID})" \
                " MERGE(a:Affiliation{aff_ID:line.AFFILIATION_ID})" \
                " CREATE (p)-[r:AFFILIATED_IN]->(a)"
    affi = conn.query(affiliations)
    affi_in = conn.query(relations)
    return affi, affi_in

def papers_published_in_affiliation(conn):
    query = "match (a:Affiliation)<-[af:AFFILIATED_IN]-(p:Person)<-[]-(pa:Paper) return a, count(pa)"
    return conn.query(query)
