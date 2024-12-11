import Token

class SymbolTable:
    def __init__(self, previous_table=None):
        self.__symbol_table = {}  # "Symbol": Token
        self.__previous_table = previous_table  # parent SymbolTable


    def add_symbol(self, symbol: str, value: str) -> None:
        if symbol in self.__symbol_table:
            self.__symbol_table[symbol].increment_occurrences()
        else:
            self.__symbol_table[symbol] = Token.Token(symbol, value)


    def get_symbol(self, symbol: Token.Token) -> Token.Token:
        if symbol in self.__symbol_table:
            return self.__symbol_table[symbol]
        elif self.__previous_table is not None:
            return self.__previous_table.get_symbol(symbol)
        
        return f"{symbol} IS NOT DEFINED"
    

    def get_table(self) -> dict:
        return self.__symbol_table