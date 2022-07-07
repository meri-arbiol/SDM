from rdflib import Graph , Literal , BNode , Namespace , RDF , RDFS , OWL , URIRef, FOAF
import csv
import os


def abox_generation(g, NS):
    VOCAB = Namespace( "http://localhost:7200/publications/" )
    g.bind( 'onto',VOCAB)
    file = os.path.join(os.getcwd(), 'CamilaAndMeritxell-SECTIONb.2_b.3-Perez_Arbiol.csv')

    with open(file, newline='', encoding='utf-8-sig') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            ## parser
            paper = row['IDpaper'].replace(' ', '_').replace('(', '').replace(')', '')
            titlepaper = Literal(row['Title_paper'].replace(' ', '_').replace('(', '').replace(')', ''))
            typepaper = Literal(row['type_paper'].replace(' ', '_'))
            abstractpaper = Literal(row['Abstract_paper'].replace(' ', '_').replace('(', '').replace(')', ''))
            author = row['IDauthor'].replace(' ', '_')
            author_name = Literal(row['Author'].replace(' ', '_'))
            reviewer = row['IDreviewer'].replace(' ', '_')
            reviewer_name = Literal(row['Reviewer'].replace(' ', '_'))
            review = row['IDreview'].replace(' ', '_')
            review_decision = Literal(row['Decision'].replace(' ', '_'))
            review_comment = Literal(row['Review'].replace(' ', '_').replace('(', '').replace(')', ''))
            topic = row['IDtopic'].replace(' ', '_')
            topic_name = Literal(row['Topic'].replace(' ', '_'))

            g.add((VOCAB[paper], RDF.type , NS[typepaper] ) )

            ## classes relations
            g.add( ( VOCAB[paper] , NS["writtenBy"] , VOCAB[author] ) )
            g.add( ( VOCAB[paper] , NS["reviewedBy"] , VOCAB[reviewer] ) )
            g.add( ( VOCAB[reviewer] , NS["writes"] , VOCAB[review] ) )
            g.add( ( VOCAB[paper] , NS["relatedTo"] , VOCAB[topic] ) )


            ## attributes relations
            g.add ((VOCAB[author], NS["personhasaName"], VOCAB[author_name]))
            g.add ((VOCAB[reviewer], NS["personhasaName"], VOCAB[author_name]))
            g.add((VOCAB[paper], NS["hasaName"], VOCAB[titlepaper]))
            g.add((VOCAB[paper], NS["abstractIs"], VOCAB[abstractpaper]))
            g.add((VOCAB[review], NS["hasaDecision"], VOCAB[review_decision]))
            g.add((VOCAB[review], NS["rtextIs"], VOCAB[review_comment]))
            g.add((VOCAB[topic], NS["thasName"], VOCAB[topic_name]))


            if row['IDconference'] != '':
                ## parser
                conference = row['IDconference'].replace(' ', '_').replace('(', '').replace(')', '')
                typeconference = Literal(row['type_conference'].replace(' ', '_').replace('(', '').replace(')', ''))
                conference_name = Literal(row['Name'].replace(' ', '_').replace('(', '').replace(')', ''))
                edition = row['IDedition'].replace(' ', '_').replace('(', '').replace(')', '')
                edition_name = Literal(row['Edition'].replace(' ', '_').replace('(', '').replace(')', ''))
                edition_city = Literal(row['City'].replace(' ', '_').replace('(', '').replace(')', ''))
                edition_year = Literal(row['Year_edition'].replace(' ', '_').replace('(', '').replace(')', ''))
                chair = row['Chairs'].replace(' ', '_').replace('(', '').replace(')', '')
                chair_name = row['Name_chair'].replace(' ', '_').replace('(', '').replace(')', '')


                g.add((VOCAB[conference], RDF.type , NS[typeconference] ) )

                ##classes relations
                g.add( ( VOCAB[edition] , NS["eispartOf"] , VOCAB[conference] ) )
                g.add( ( VOCAB[conference] , NS["cishandleBy"] , VOCAB[chair] ) )
                g.add( ( VOCAB[paper] , NS["PublishenOnE"] , VOCAB[edition] ) )
                g.add( ( VOCAB[conference] , NS["crelatedTo"] , VOCAB[topic] ) )
                g.add( ( VOCAB[chair] , NS["cassign"] , VOCAB[reviewer] ) )

                ## attributes relations
                g.add( ( VOCAB[conference] , NS["hasconferenceName"] , VOCAB[conference_name] ) )
                g.add( ( VOCAB[edition] , NS["ehasaName"] , VOCAB[edition_name] ) )
                g.add( ( VOCAB[edition] , NS["ehasaCity"] , VOCAB[edition_city] ) )
                g.add( ( VOCAB[edition] , NS["ehasaYear"] , VOCAB[edition_year] ) )
                g.add ((VOCAB[chair], NS["personhasaName"], VOCAB[chair_name]))

            if row['IDjournal'] != '':
                ## parser
                journal = row['IDjournal'].replace(' ', '_').replace('(', '').replace(')', '')
                journal_title = row['title'].replace(' ', '_').replace('(', '').replace(')', '')
                volume = row['volume'].replace(' ', '_').replace('(', '').replace(')', '')
                volume_year = row['Year_volume'].replace(' ', '_').replace('(', '').replace(')', '')
                editor = row['editor'].replace(' ', '_').replace('(', '').replace(')', '')
                editor_name = row['name_editor'].replace(' ', '_').replace('(', '').replace(')', '')

                ## classes relations
                g.add( ( VOCAB[paper] , NS["publishedOnV"] , VOCAB[volume] ) )
                g.add( ( VOCAB[volume] , NS["vispartOf"] , VOCAB[journal] ) )
                g.add( ( VOCAB[journal] , NS["jishandleby"] , VOCAB[editor] ) )
                g.add( ( VOCAB[journal] , NS["jrelatedTo"] , VOCAB[topic] ) )
                g.add( ( VOCAB[editor] , NS["eassign"] , VOCAB[reviewer] ) )

                ## attributes relations
                g.add( ( VOCAB[journal] , NS["hasjournalName"] , VOCAB[journal_title] ) )
                g.add( ( VOCAB[volume] , NS["vhasaYear"] , VOCAB[volume_year] ) )
                g.add ((VOCAB[editor], NS["personhasaName"], VOCAB[editor_name]))

    return g


if __name__ == '__main__':

    g = Graph()
    g.parse("CamilaAndMeritxell-SECTIONb.1-Perez_Arbiol.ttl")
    NS = Namespace( "http://localhost:7200/publications/" )

    g = abox_generation(g, NS)

    g.serialize( destination = "CamilaAndMeritxell-SECTIONb.2_b.3-Perez_Arbiol.ttl" , format = "ttl" )

    print( "Created CamilaAndMeritxell-SECTIONb.2_b.3-Perez_Arbiol.ttl in folder:" )
    print( str( os.getcwd() ) )
