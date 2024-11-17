import networkx as nx
import ts
from models import Node as TSNTXNode

class AbstractSyntaxTree:
    def __init__(self):
        self.tree_graph = nx.MultiDiGraph()
    
    def add_tree_data(self, tree: ts.Tree):
        if not isinstance(tree, ts.Tree):
            raise TypeError("tree must be of type tree_sitter.Tree")
        
        # Function to traverse the Tree-sitter tree and add nodes/edges to the graph
        def traverse_tree(node: ts.Node, parent=None):
            nodes, edges = [], []
            tsntx_node = TSNTXNode(node)
            
            nodes.append(tsntx_node)

            if parent is not None:
                # self.tree_graph.add_edge(parent_id, node_id, "AST")
                edges.append((parent, tsntx_node, "AST"))
            
            # Traverse child nodes recursively
            for child in node.children:
                child_nodes, child_edges = traverse_tree(child, tsntx_node)
                
                # Accumulate nodes and edges from the child
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
    ast = AbstractSyntaxTree()
    ast.add_tree_data(ts_tree)
    print(ast.tree_graph.nodes(data=True))
    print('\n')
    print(ast.tree_graph.edges(keys=True))