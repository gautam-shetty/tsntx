import ts
from hashlib import md5
from pathlib import Path

class Node:
    def __init__(self, file_path: Path, ts_node: ts.Node):
        self.id = ts_node.id
        self.type = ts_node.type
        self.start_point = ts_node.start_point
        self.end_point = ts_node.end_point
        self.start_byte = ts_node.start_byte
        self.end_byte = ts_node.end_byte
        self.is_named = ts_node.is_named
        self.tsntx_id = self.get_tsntx_id(file_path)
        
    def get_tsntx_id(self, file_path: Path):
        return hash(md5(f"{file_path}-{self.id}".encode()).hexdigest())
    
    def get_ts_node_data(self):
        return {key: value for key, value in self.__dict__.items() if key != 'tsntx_id'}