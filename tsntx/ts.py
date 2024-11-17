from tree_sitter import Language, Parser, Tree, Node

class TSParser:
    def __init__(self, TSLanguage: Language):
        if not isinstance(TSLanguage, Language):
            raise TypeError("TSLanguage must be of type tree_sitter.Language")
        
        self.language = TSLanguage
        self.parser = Parser(TSLanguage)
        
    def generate_tree(self, code: str, encoding: str = 'utf8') -> Tree:
        tree: Tree = self.parser.parse(bytes(code, encoding), encoding=encoding)
        
        return tree