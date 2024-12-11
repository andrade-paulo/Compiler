import os
import re


class LexicalAnalyser:
    RESERVED_WORDS = {
        "some": "QUANTIFIER", "all": "QUANTIFIER", "value": "QUANTIFIER", "min": "QUANTIFIER", "max": "QUANTIFIER", "exactly": "QUANTIFIER", 
        "that": "LOGICAL", "not": "LOGICAL", "and": "LOGICAL", "or": "LOGICAL", 
        "Class:": "RESERVED_WORD", "EquivalentTo:": "RESERVED_WORD", "Individuals:": "RESERVED_WORD", "SubClassOf:": "RESERVED_WORD", "DisjointClasses:": "RESERVED_WORD"
    }

    SPECIAL_SYMBOLS = ["(", ")", "{", "}", "[", "]", ",", ">", "<", "="]

    REGEX_MAP = {
        "CLASS_NAME": r"[A-Z][a-zA-Z_]*",
        "PROPRIETY": r"[a-z][a-zA-Z0-9_]*",
        "INDIVIDUAL_NAME": r"[A-Z][a-zA-Z_]*[\d]+",
        "NAMESPACE": r"[a-z]+:[a-z]+",
        "NUMBER": r"[\d]+",
    }


    def __init__(self, input_file: str) -> None:
        if not os.path.exists(input_file):
            raise FileNotFoundError
        
        self.__input_file = input_file


    def analyse_file(self) -> list:
        tokens = []

        with open(self.__input_file, "r") as file:
            for line in file.readlines():
                line = line.strip()
                for word in line.split(" "):
                    token = ""
                    for char in word:
                        if char in self.SPECIAL_SYMBOLS:
                            if token != "":  # If the special symbol is not separated by a space
                                tokens.append(token)
                                token = ""
                            tokens.append(char)
                        else:   # If the character is not a special symbol it is part of the token
                            token += char
                    if token != "":
                        tokens.append(token.strip())
        return tokens


    def classify_token(self, token: str) -> str:
        if token in self.SPECIAL_SYMBOLS:
            return "SPECIAL_SYMBOL"
        
        if token in self.RESERVED_WORDS.keys():
            return self.RESERVED_WORDS[token]
        
        for key, value in self.REGEX_MAP.items():
            if re.fullmatch(value, token):
                return key
            
        return "UNMATCHED"


    