from rdflib import Graph, Literal, RDF, URIRef

# create a Graph
g = Graph()
g.parse("bands_ontology_res.owl", format='turtle')


def result(message, query_in):
    res = g.query(query_in)
    print("\n" + message)
    for row in res:
        if (len(row) > 1):
            band = row[0].split('#')[1].replace("_", " ")
            genre = row[1].split('#')[1].replace("_", " ")
            print("{} - {}".format(band, genre))
        else:
            print(row[0].split('#')[1].replace("_", " "))


result('Bands formed after 2000:',
       """PREFIX : <http://www.semanticweb.org/alivanov/ontologies/2020/5/untitled-ontology-3#>
    SELECT ?artist
    WHERE {
        ?artist a :Artist;
            :formed ?formed .
        FILTER(?formed > 2000)
    }""")

result("Metalcore albums:",
       """PREFIX : <http://www.semanticweb.org/alivanov/ontologies/2020/5/untitled-ontology-3#>
       SELECT ?album
       WHERE {
           ?album a :Album;
           :hasGenreOf :Metalcore
       }""")

result("Progressive metal artists:",
       """PREFIX : <http://www.semanticweb.org/alivanov/ontologies/2020/5/untitled-ontology-3#>
       SELECT ?artist
       WHERE {
           ?artist a :Artist;
           :hasGenreOf :Progressive_Metal
       }""")

result("Deathcore tracks:",
       """PREFIX : <http://www.semanticweb.org/alivanov/ontologies/2020/5/untitled-ontology-3#>
       SELECT ?track
       WHERE {
           ?track a :Track;
           :fromAlbum ?album .
           {
               SELECT ?album
               WHERE {
                   ?album a :Album;
                   :hasGenreOf :Deathcore
               }
           }
       }""")

result('Groups in similar genres to Progressive Rock',
       """PREFIX : <http://www.semanticweb.org/alivanov/ontologies/2020/5/untitled-ontology-3#>
        SELECT ?band ?genre
        WHERE{
            ?band a :Artist;
            :hasGenreOf ?genre.
            {
                SELECT ?genre
                    WHERE{
                        ?genre a ?baseGen.
                        {SELECT ?baseGen
                            WHERE {
                                :Progressive_Rock a ?baseGen.
                                FILTER(?baseGen != owl:NamedIndividual)
                            }
                        }
                FILTER(?genre != :Progressive_Rock)
            }
        }
        }""")
