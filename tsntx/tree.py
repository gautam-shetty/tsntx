import ts
import nx
from pathlib import Path
from models import Node, EdgeType

class AbstractSyntaxTree:
    def __init__(self, file_path: Path = None):
        self.tree_graph = nx.MultiDiGraph()
        self.file_path = file_path
        self.concrete_tree_mode: bool = False
    
    def __call__(self):
        return self.tree_graph
    
    def add_tree_data(self, tree: ts.Tree):
        if not isinstance(tree, ts.Tree):
            raise TypeError("tree must be of type tree_sitter.Tree")
        
        # Function to traverse the Tree-sitter tree and add nodes/edges to the graph
        def traverse_tree(ts_node: ts.Node, parent_node: Node = None):
            nodes, edges = [], []
            current_node = Node(self.file_path, ts_node)
            
            if self.concrete_tree_mode:
                nodes.append((current_node.tsntx_id, { "ts_node" : current_node.get_ts_node_data()}))
            else:
                if current_node.is_named:
                    nodes.append((current_node.tsntx_id, { "ts_node" : current_node.get_ts_node_data() }))
                

            if parent_node is not None:
                edges.append((parent_node.tsntx_id, current_node.tsntx_id, EdgeType.AST))
            
            # Traverse child nodes recursively
            for child in ts_node.children:
                child_nodes, child_edges = traverse_tree(child, current_node)
                
                nodes.extend(child_nodes)
                edges.extend(child_edges)
            
            return nodes, edges
        
        tree_nodes, tree_edges = traverse_tree(tree.root_node)
        self.tree_graph.add_nodes_from(tree_nodes)
        self.tree_graph.add_edges_from(tree_edges)
    
if __name__ == "__main__":
    import tree_sitter_python as tspython
    
    PY_LANGUGAGE = ts.Language(tspython.language())
    parser = ts.TSParser(PY_LANGUGAGE)
    
    sample_code = """
    def foo():
        if bar:
            baz()
    """
    ts_tree = parser.generate_tree(sample_code)
    
    ast = AbstractSyntaxTree(file_path="test.py")
    ast.add_tree_data(ts_tree)
    nx.export_as_json(ast.tree_graph, "tmp/ast.json")
    nx.export_as_dot(ast.tree_graph, "tmp/ast.dot")