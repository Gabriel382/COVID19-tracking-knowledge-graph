from kgce.schema.semantic.map import Country, City, CityOf, Flight, PlaceGraph, AirportGraph, Airport, AirportOf, FlightGraph
from kgce.schema.semantic.event import Event, EventGraph, EventOf
import numpy as np
import pandas as pd
import pycountry
from tqdm import tqdm
from datetime import date, datetime

def getPlaceAirportGraphFromTable(df_table):
    '''
    Must have country, iso_country, country_wikipedia_link and city columns
    '''
    country_dict = {}
    city_dict = {}
    airport_dict = {}
    placeGraph = PlaceGraph(graph_name="World Graph",nodes=[])
    airportGraph = AirportGraph(graph_name="Airport Graph", nodes=[])

    # For each (city,country) pair
    for i in tqdm(range(df_table.shape[0])):
        country_name = df_table.loc[i]['country']
        city_name = df_table.loc[i]['city']
        city_key_name = str(city_name) + country_name
        airpot_name = df_table.loc[i]['name']
        airport_key_name = str(airpot_name) + city_key_name
        if not pd.isna(country_name) and not pd.isna(city_name):
            # Check countries
            if country_name not in country_dict.keys():
                # If we dont find isocode on table
                isocode = df_table.loc[i]['iso_country'] if not pd.isna(df_table.loc[i]['iso_country']) else pycountry.countries.get(name=country_name).alpha_2
                # Then create country instance
                country = Country(country_name, isocode, df_table.loc[i]['country_wikipedia_link'])
                country_dict[country_name] = country
                placeGraph.nodes.append(country)
            else:
                country = country_dict[country_name]
            # Check cities
            if city_key_name not in city_dict.keys():
                city = City(city_name, country_name)
                city_dict[city_key_name] = city 
                placeGraph.nodes.append(city)
                airportGraph.nodes.append(city)
            else:
                city = city_dict[city_key_name]
            # Check airports
            if airport_key_name not in airport_dict.keys():
                airport = Airport(airpot_name, city_name, country_name, df_table.loc[i]['iata'], df_table.loc[i]['icao'])
                airport_dict[airport_key_name] = airport
                airportGraph.nodes.append(airport)
            else:
                airport = airport_dict[airport_key_name]
            # Make City relationships
            if (city, country) not in placeGraph.edges_dict.keys():
                try:
                    relation = CityOf("city of")
                    placeGraph.add_unidirectional_edge(city, country, relation)
                except Exception as e:
                    tqdm.write(city.name + " " + country.name)
                    tqdm.write(e)
            # Make Airport relationships
            if (airport, city) not in airportGraph.edges_dict.keys():
                try:
                    relation = AirportOf("airport of")
                    airportGraph.add_unidirectional_edge(airport, city, relation)
                except Exception as e:
                    tqdm.write(airport.name + " " + city.name)
                    tqdm.write(e)

    return placeGraph, airportGraph


def getEventGraphFromTable(df_table, countrynodes):
    # Setup country dict
    dict_countries = {}
    eventGraph = EventGraph("Event Graph", nodes=[])
    for country in countrynodes:
        dict_countries[country.iso2] = country
        eventGraph.nodes.append(country)

    # For each (day, country) event
    for i in tqdm(range(df_table.shape[0])):
        # Get event
        eventline = df_table.loc[i]
        event = Event(name=str(eventline["Date_reported"])+str(eventline["Country_code"]),
         date=str(datetime.fromisoformat(str(eventline["Date_reported"])).timestamp()),
         isocountry=eventline["Country_code"], newcases=eventline["New_cases"],
         cumulativecases=eventline["Cumulative_cases"], newdeaths=eventline["New_deaths"],
         cumulativedeaths=eventline["Cumulative_deaths"])
        eventGraph.nodes.append(event)
        # Get country of event
        if event.isocountry in dict_countries.keys():
            country = dict_countries[event.isocountry]
            relation = EventOf(name="Event Of", date=event.date)
            eventGraph.add_unidirectional_edge(event, country, relation)
            
    return eventGraph

def getFlightsFromTable(df_table, airportgraph):
    airports = [x for x in airportgraph.nodes if type(x)==Airport]
    airportdict = dict(zip( [x.icao for x in airports] ,airports))
    
    flightGraph = FlightGraph('Flight Graph', airports)

    for i in tqdm(range(df_table.shape[0])):
        # Get line
        line = df_table.loc[i]
        # Check if we have both airports have nodes
        origin_airport = airportdict[line['origin']] if (not pd.isna(line['origin']) and line['origin'] in airportdict.keys()) else None
        destination_airport = airportdict[line['destination']] if (not pd.isna(line['destination']) and line['destination'] in airportdict.keys()) else None
        if origin_airport != destination_airport or (origin_airport is None and destination_airport is None):
            flight  = Flight("Flight", str(line['callsign']), str(line['number']), str(line['icao24']), str(line['registration']),
                str(line['typecode']), str(line['firstseen'].timestamp()), str(line['lastseen'].timestamp()), str(line['day'].timestamp()), str(line['latitude_1']),
                str(line['longitude_1']), str(line['altitude_1']), str(line['latitude_2']), str(line['longitude_2']), str(line['altitude_2']))
            flightGraph.add_unidirectional_edge(origin_airport, destination_airport, flight)
    return flightGraph