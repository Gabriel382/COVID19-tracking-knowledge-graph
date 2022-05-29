from kgce.neo4j.handler import Neo4jWrapper
from traffic.data import airports
from kgce.schema.semantic.handler import getPlaceAirportGraphFromTable


neoServer = Neo4jWrapper(uri="bolt://localhost:7687",userName="neo4j",password="neo4j")
logpath = 'data/Log/openskylog.txt'
# ================== GET COUNTRIES, CITIES AND AIRPORTS ==================
# DKAP
print("DKAP for countries, cities and airports...")
cities_countries = airports.data.rename(columns=dict(municipality="city")).drop_duplicates().reset_index(drop=True)
# KGCE
print("Getting country-city and airport graphs...")
placeGraph, airportGraph = getPlaceAirportGraphFromTable(cities_countries)


# ================== GET FLIGHTS ==================
# DKAP
print("DKAP for flights...")
from dkap.opensky import getOpenSkyData
from utils.loghelper import is_log_written, print_file_in_log


flights_dict = getOpenSkyData("data/OpenSky/", logpath, is_log_written)

# KGCE LOOP
print("KGCE for flights - LOOP Starts")
from kgce.schema.semantic.handler import getFlightsFromTable

for flightmonth in flights_dict.keys():
    if not is_log_written(logpath,flightmonth):
        print("================ Current Month : " + str(flightmonth) + " ======================")
        # Getting graph
        print("Getting graph...")
        flightgraph = getFlightsFromTable(flights_dict[flightmonth], airportGraph)

        # CQL command for Flight Graph
        print("Getting queries...")
        cql_command_nodes, cql_command_edges = flightgraph._neo_CreateGraphCQL()

        # Send Flights to Neo4J
        print("Sending queries to Neo4j...")
        result = neoServer.sendQuery(cql_command_edges)

        # If done, then save in log
        print("Saving in log...")
        print_file_in_log(logpath, flightmonth)
        print("Done for the month of " + str(flightmonth))
    else:
        print("==========================================")
        print("=========== Month already in log : " + str(flightmonth) + " ==================")
        print("==========================================")

print("Done!")
neoServer.closeConnection()