from kgce.schema.semantic.neo4jclasses import Neo4jNode, Neo4jRelation, Neo4jGraph

class Country(Neo4jNode):
    
    def __init__(self,name, iso2, country_wikipedia_link):
        super().__init__(name)
        self.iso2 = iso2
        self.country_wikipedia_link = country_wikipedia_link

    def _neostring(self):
        dict_params = {
            'name' : self.name,
            'iso2' : self.iso2,
            'country_wikipedia_link' : self.country_wikipedia_link
        }
        listofkeys = list(dict_params.keys())
        for key in listofkeys:
            if dict_params[key] is None:
                dict_params.pop(key)
        return super()._neostring("Country", dict_params)

class City(Neo4jNode):
    def __init__(self, name, country):
        super().__init__(name)
        self.country = country
    
    def _neostring(self):
        return super()._neostring("City", {'name' : self.name, 'country':self.country})

class Airport(Neo4jNode):
    def __init__(self, name, city, country, iata, icao):
        super().__init__(name)
        self.city = city
        self.country = country
        self.iata = iata
        self.icao = icao
    
    def _neostring(self):
        return super()._neostring("Airport", {'name' : self.name, 'city': self.city,
        "country": self.country, "iata":self.iata, "icao":self.icao})


class TransportGraph(Neo4jGraph):

    def __init__(self, graph_name, nodes):
        super().__init__(graph_name, nodes)


class PlaceGraph(Neo4jGraph):

    def __init__(self, graph_name, nodes):
        super().__init__(graph_name, nodes)


class AirportGraph(Neo4jGraph):

    def __init__(self, graph_name, nodes):
        super().__init__(graph_name, nodes)

class FlightGraph(Neo4jGraph):

    def __init__(self, graph_name, nodes):
        super().__init__(graph_name, nodes)

class Flight(Neo4jRelation):
    def __init__(self, name):
        super().__init__(name)
    
    def _neostring(self):
        return super()._neostring("FLIGHT", {'name' : self.name})


class CityOf(Neo4jRelation):

    def __init__(self, name):
        super().__init__(name)
    def _neostring(self):
        return super()._neostring("CITY_OF",  {'name' : self.name})

class AirportOf(Neo4jRelation):

    def __init__(self, name):
        super().__init__(name)
    def _neostring(self):
        return super()._neostring("AIRPORT_OF",  {'name' : self.name})

class Flight(Neo4jRelation):

    def __init__(self, name, callsign, number, icao24,
    registration, typecode, firstseen, lastseen, day, latitude_1, longitude_1,
    altitude_1, latitude_2, longitude_2, altitude_2):
        super().__init__(name)
        self.callsign = callsign
        self.number = number
        self.icao24 = icao24
        self.registration = registration
        self.typecode = typecode
        self.firstseen = firstseen
        self.lastseen = lastseen
        self.day = day
        self.latitude_1 = latitude_1
        self.longitude_1 = longitude_1
        self.altitude_1 = altitude_1
        self.latitude_2 = latitude_2
        self.longitude_2 = longitude_2
        self.altitude_2 = altitude_2

    def _neostring(self):
        return super()._neostring("FLIGHT",  {'name' : self.name,
        'callsign' : self.callsign,
        'number' : self.number,
        'icao24' : self.icao24,
        'registration' : self.registration,
        'typecode' : self.typecode,
        'firstseen' : self.firstseen,
        'lastseen' : self.lastseen,
        'day' : self.day,
        'latitude_1' : self.latitude_1,
        'longitude_1' : self.longitude_1,
        'altitude_1' : self.altitude_1,
        'latitude_2' : self.latitude_2,
        'longitude_2' : self.longitude_2,
        'altitude_2' : self.altitude_2
        })

