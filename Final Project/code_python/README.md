## INSTRUCTIONS BEFORE RUNNING THE NOTEBOOK

- Put the two CSV files stored in our "data" folder inside the Neo4j input folder.
- Enter into a project in Neo4j and put the correct credentials of user, pass and uri when creating the connection from the notebook, for example:
```
  conn = Neo4jConnection(uri='bolt://localhost:7687', user="neo4j", pwd='sdm')
```
