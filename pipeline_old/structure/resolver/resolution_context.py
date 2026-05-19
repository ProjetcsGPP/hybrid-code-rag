# pipeline/structure/resolver/resolution_context.py


class ResolutionContext:

    def __init__(self, symbol, index):
        self.symbol = symbol
        self.index = index

        self.module = symbol.module_name
        self.class_name = symbol.parent_symbol_id