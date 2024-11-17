import ts

class Node:
    def __init__(self, node: ts.Node):
        self.id = id(node)
        self.node = node
        
    def __repr__(self):
        return f"Node({self.id}) - {self.node})"