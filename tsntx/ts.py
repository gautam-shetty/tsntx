from tree_sitter import Language, Parser, Tree

class TSParser:
    def __init__(self, TSLanguage: Language):
        if not isinstance(TSLanguage, Language):
            raise TypeError("TSLanguage must be of type tree_sitter.Language")
        
        self.language = TSLanguage
        self.parser = Parser(TSLanguage)
        
    def generate_tree(self, code: str, encoding: str = 'utf8', byte_offset: int = 0) -> Tree:
        
        def read_callable_byte_offset(byte_offset, point):
            return src[byte_offset : byte_offset + 1]
        
        src = bytes(code, encoding)
        tree: Tree = self.parser.parse(read_callable_byte_offset, encoding=encoding)
        
        return tree