import re
from tqdm import tqdm

class Neo4jNode:
    def __init__(self,name):
        self.name = name
        
    def _neostring(self, class_name, dict_param):
        return ":" + class_name + " { " + ", ".join([str(x) + ": " + (str(float(y)) if type(y)==str and y.replace('.','',1).replace(',','',1).isdigit() else '"' + str(y).replace("'","").replace('"','') + 
        '"' ) for x,y in list(dict_param.items())]) + "}"


class Neo4jGraph:

    def __init__(self, graph_name, nodes):
        self.edges_dict = {}
        self.graph_name = graph_name
        self.nodes = nodes
    
    def add_bidirectional_edge(self,starting_node, ending_node, relation):
        self.add_unidirectional_edge(starting_node, ending_node, relation)
        self.add_unidirectional_edge(ending_node, starting_node, relation)

    def add_unidirectional_edge(self,starting_node, ending_node, relation):
        assert starting_node in self.nodes or starting_node is None
        assert ending_node in self.nodes or ending_node is None
        last_push = []
        if (starting_node,ending_node) in self.edges_dict:
            last_push = self.edges_dict[(starting_node,ending_node)]
        self.edges_dict[(starting_node,ending_node)] = last_push + [relation]
    
    def _neo_EdgeCreateCQL(self, relation, starting_node, ending_node):
        
        if starting_node is not None and ending_node is not None:
            return "MATCH (a" + starting_node._neostring()+"), (b"+ending_node._neostring()+") CREATE (a)-[r"+relation._neostring()+"]->(b) RETURN a.name,b.name,r.name"
        elif ending_node is not None:
            return "MATCH (b"+ending_node._neostring()+") CREATE ()-[r"+relation._neostring()+"]->(b) RETURN b.name,r.name"
        elif starting_node is not None:
            return "MATCH (a" + starting_node._neostring()+") CREATE (a)-[r"+relation._neostring()+"]->() RETURN a.name,r.name"
        else:
            return "CREATE ()-[r"+relation._neostring()+"]->() RETURN r.name"

    def _neo_NodeListCreationCQL(self, list_of_nodes):
        list_of_commands = []
        for node in list_of_nodes:
            node_name = re.sub('[^a-zA-Z]+', '', node.name.replace("'","").lower().replace(" ",""))
            node_name = node_name if len(node_name) > 0 else "n"
            list_of_commands.append("MERGE (" + node_name +""+node._neostring() + ") RETURN "+node_name)
        return list_of_commands

    def _neo_CreateGraphCQL(self):
        list_of_nodes = []
        list_of_edges = []
        for (starting_node,ending_node) in tqdm(self.edges_dict):
            # Starting Node
            if starting_node is not None:
                starting_node_string = starting_node._neostring()
                if starting_node_string not in list_of_nodes:
                    list_of_nodes.append(starting_node)
            # Ending Node
            if ending_node is not None:
                ending_node_string = ending_node._neostring()
                if ending_node_string not in list_of_nodes:
                    list_of_nodes.append(ending_node)
            # Relations
            list_of_relations = self.edges_dict[(starting_node,ending_node)]
            for r in list_of_relations:
                list_of_edges.append(self._neo_EdgeCreateCQL(r,starting_node, ending_node))
        return self._neo_NodeListCreationCQL(list_of_nodes),list_of_edges

class Neo4jRelation:

    def __init__(self, name):
        self.name = name
    
    def _neostring(self, class_name, dict_param):
        return ":" + class_name + " { " +  ", ".join([str(x) + ": " + (str(float(y)) if type(y)==str and y.replace('.','',1).replace(',','',1).isdigit() else '"' + y + 
        '"') for x,y in list(dict_param.items())]) + " }"

