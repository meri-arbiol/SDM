def create_articles(conn):
    articles = "LOAD CSV WITH HEADERS FROM 'file:///articles.csv' AS row WITH row " \
               "CREATE (:Paper {paper_ID: row['article_ID'], title: row['title'], author: row['author'], coauthor: row[" \
               "'coauthor'], abstract: row['abstract']}) "
    conn.query(articles)


def create_authors(conn):
    authors = "LOAD CSV WITH HEADERS FROM 'file:///authors.csv' AS row WITH row CREATE (:Person {author: row[" \
              "'author'], " \
              "author_ID: row['author_ID']}) "

    conn.query(authors)


def create_coauthors(conn):
    coauthors = "LOAD CSV WITH HEADERS FROM 'file:///co_authors.csv' AS row WITH row CREATE (:Person {author: row[" \
                "'coauthor'], author_ID: row['coauthor_ID']}) "
    conn.query(coauthors)


def create_journals(conn):
    journals = "LOAD CSV WITH HEADERS FROM 'file:///journals.csv' AS row WITH row CREATE (:Journal {journal: row[" \
               "'Journals'], journal_ID: row['Journals_ID']})"
    conn.query(journals)


def create_conferences(conn):
    conferences = "LOAD CSV WITH HEADERS FROM 'file:///conferences.csv' AS row WITH row CREATE (:Conference {" \
                  "conference: row['conference'], conference_ID: row['conference_ID'], city: row['city'], " \
                  "year: row['year'], edition: row['edition']}) "
    conn.query(conferences)


def create_years(conn):
    years = "LOAD CSV WITH HEADERS FROM 'file:///years.csv' AS row WITH row CREATE (:Year {year: row['year']})"
    conn.query(years)


def create_volumes(conn):
    volumes = "LOAD CSV WITH HEADERS FROM 'file:///volumes.csv' AS row WITH row CREATE (:Volume {volume: row[" \
              "'volume'], volume_ID: row['Volume_ID']}) "
    conn.query(volumes)


def create_cited_by(conn):
    cited = "LOAD CSV WITH HEADERS FROM 'file:///cited_by.csv' as row MERGE(p1:Paper{paper_ID:row.article_ID1}) MERGE(" \
            "p2:Paper{paper_ID:row.article_ID2}) CREATE (p1)-[:CITED_BY]->(p2) "
    conn.query(cited)


def create_authored_by(conn):
    authored = "LOAD CSV WITH HEADERS FROM 'file:///cited_by.csv' as row MERGE(p1:Paper{paper_ID:row.article_ID1}) " \
               "MERGE(p2:Paper{paper_ID:row.article_ID2}) CREATE (p1)-[:CITED_BY]->(p2) "
    co_authored = "LOAD CSV WITH HEADERS FROM 'file:///co_authored_by.csv' as row MERGE(p: Paper{paper_ID: " \
                  "row.ARTICLES_ID}) MERGE(a: Person{author_ID: row.COAUTHOR_ID}) CREATE(p) - [: COAUTHORED_BY]->(a) "
    conn.query(authored)
    conn.query(co_authored)


def create_reviewed_by(conn):
    reviewed = "LOAD CSV WITH HEADERS FROM 'file:///reviewers.csv' as row " \
               "MERGE(a:Person{author_ID:row.Reviewer}) " \
               "MERGE(p:Paper{paper_ID:row.Article}) " \
               "CREATE (p)-[:REVIEWED_BY]->(a)"
    conn.query(reviewed)


def create_published_in(conn):
    published = "LOAD CSV WITH HEADERS FROM 'file:///conferences_relationship.csv' as row " \
                "MERGE(p: Paper{paper_ID: row.article_ID}) " \
                "MERGE(c: Conference{conference_ID: row.conference_ID}) " \
                "CREATE(p) - [: IS_PUBLISHED_IN]->(c)"
    published2 = "LOAD CSV WITH HEADERS FROM 'file:///articles_volume_relation.csv' as row " \
                 "FIELDTERMINATOR ';' " \
                 "MERGE(p:Paper{paper_ID:row.article_ID}) " \
                 "MERGE(v:Volume{volume_ID:row.Volume_ID}) " \
                 "CREATE (p)-[:IS_PUBLISHED_IN]->(v)"

    conn.query(published2)
    conn.query(published)


def create_has_in(conn):
    has = "LOAD CSV WITH HEADERS FROM 'file:///volum_journal_relation.csv' as row " \
          "FIELDTERMINATOR ';' " \
          "MERGE(j: Journal{journal_ID: row.Journals_ID}) " \
          "MERGE(v: Volume{volume_ID: row.Volume_ID}) " \
          "CREATE(j) - [: HAS]->(v)"
    in_ = "LOAD CSV WITH HEADERS FROM 'file:///year_volum_relation.csv' as row FIELDTERMINATOR ';' " \
          "MERGE(v: Volume{volume_ID: row.Volume_ID}) " \
          "MERGE(y: Year{year: row.year}) " \
          "CREATE(v) - [: IN]->(y)"
    conn.query(has)
    conn.query(in_)


def create_topics(conn):
    communities = "LOAD CSV WITH HEADERS FROM 'file:///topics.csv' AS row WITH row CREATE (:Topic {topic: row[" \
                  "'Topics'], topic_ID: row['Topics_ID']}) "
    links = "LOAD CSV WITH HEADERS FROM 'file:///relations_topics_articles.csv' as row " \
            "MERGE(t:Topic{topic_ID:row.Topic_ID}) " \
            "MERGE(p:Paper{paper_ID:row.Article_ID}) " \
            "CREATE (p)-[:RELATED_TO]->(t) "
    conn.query(communities)
    conn.query(links)
