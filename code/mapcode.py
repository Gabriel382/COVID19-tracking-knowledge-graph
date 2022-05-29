from kgce.neo4j.handler import Neo4jWrapper
from traffic.data import airports
from kgce.schema.semantic.handler import getPlaceAirportGraphFromTable


neoServer = Neo4jWrapper(uri="bolt://localhost:7687",userName="neo4j",password="neo4j")

# ================== GET COUNTRIES, CITIES AND AIRPORTS ==================
# DKAP
cities_countries = airports.data.rename(columns=dict(municipality="city")).drop_duplicates().reset_index(drop=True)
# KGCE
print("Getting countries, cities and airports...")
placeGraph, airportGraph = getPlaceAirportGraphFromTable(cities_countries)

# DKAP
import pandas as pd
from kgce.schema.semantic.map import Country
whodata = pd.read_csv("data/WHO/WHO-COVID-19-global-data.csv")
country_nodes = [x for x in placeGraph.nodes if type(x)==Country]
# KGCE
from kgce.schema.semantic.handler import getEventGraphFromTable
print("Getting event graph...")
eventGraph = getEventGraphFromTable(whodata,country_nodes)

# CQL command for Event Graph
print("Getting queries...")
cql_command_nodes, cql_command_edges = eventGraph._neo_CreateGraphCQL()
cql_command = cql_command_nodes + cql_command_edges
cql_command_filter = [x for x in cql_command if  not (x[0:5] == "MERGE" and ":Country {" in x)]

# Send Events to Neo4J
print("Deleting existing events...")
result = neoServer.sendQuery(["MATCH (n:Event) DETACH DELETE n"])
print("Sending queries to Neo4j")
result = neoServer.sendQuery(cql_command_filter)
print("DONE!")
neoServer.closeConnection()