class Token:
    def __init__(self, symbol: str, token_type: str) -> None:
        self.__symbol = symbol
        self.__token_type = token_type
        self.__occurrences = 1

    def get_symbol(self) -> str:
        return self.__symbol
    
    def get_token_type(self) -> str:
        return self.__token_type
    
    def get_occurrences(self) -> int:
        return self.__occurrences
    
    def increment_occurrences(self) -> None:
        self.__occurrences += 1