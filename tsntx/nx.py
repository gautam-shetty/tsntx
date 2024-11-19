from networkx import MultiDiGraph
from networkx import readwrite
from networkx.drawing.nx_agraph import write_dot
import os
import json

def export_as_json(G: MultiDiGraph, output_path: str):
    base_folder = os.path.dirname(output_path)
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    graph_data = readwrite.json_graph.node_link_data(G, edges="edges")
    with open(output_path, 'w') as f:
        json.dump(graph_data, f, indent=2)
        
def export_as_dot(G: MultiDiGraph, output_path: str):
    base_folder = os.path.dirname(output_path)
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    
    write_dot(G, output_path)
