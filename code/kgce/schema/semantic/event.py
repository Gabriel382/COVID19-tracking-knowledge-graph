from types import new_class
from kgce.schema.semantic.neo4jclasses import Neo4jNode, Neo4jRelation, Neo4jGraph

class Event(Neo4jNode):
    def __init__(self, name, date, isocountry, newcases, cumulativecases, newdeaths, cumulativedeaths):
        super().__init__(name)
        self.date = date
        self.isocountry = isocountry
        self.newcases = newcases
        self.cumulativecases = cumulativecases
        self.newdeaths = newdeaths
        self.cumulativedeaths = cumulativedeaths
    
    def _neostring(self):
        return super()._neostring(
            "Event", {'name' : self.name,
             'isocountry': self.isocountry,
             'newcases': self.newcases,
             'cumulativecases': self.cumulativecases,
             'newdeaths': self.newdeaths,
             'cumulativedeaths': self.cumulativedeaths})

class EventOf(Neo4jRelation):
    def __init__(self, name, date):
        super().__init__(name)
        self.date = date
    
    def _neostring(self):
        return super()._neostring("EVENT_OF", {'name' : self.name, "date" : self.date})

class EventGraph(Neo4jGraph):

    def __init__(self, graph_name, nodes):
        super().__init__(graph_name, nodes)
