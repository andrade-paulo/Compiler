import SymbolTable as ST

import os
import ply.lex as lex
from ply.lex import TOKEN


class LexicalAnalyser:
    RESERVED_WORDS = {
        "some": "QUANTIFIER", "all": "QUANTIFIER", "value": "QUANTIFIER", "min": "QUANTIFIER", "max": "QUANTIFIER", "exactly": "QUANTIFIER", 
        "that": "LOGICAL", "not": "LOGICAL", "and": "LOGICAL", "or": "LOGICAL", 
        "Class:": "CLASS", "EquivalentTo:": "EQUIVALENT", "Individuals:": "INDIVIDUALS", "SubClassOf:": "SUBCLASS", "DisjointClasses:": "DISJOINT_CLASS"
    }

    tokens = (
        "NUMBER", "LPAR", "RPAR", "LCURLY", "RCURLY", "LBRACKET", "RBRACKET", "COMMA", "BIG", "LESS", "BEQ", "LEQ", "ID",
        "CLASS_NAME", "PROPRIETY", "INDIVIDUAL_NAME", "NAMESPACE", 
        "QUANTIFIER", "LOGICAL", "CLASS", "EQUIVALENT", "INDIVIDUALS", "SUBCLASS", "DISJOINT_CLASS"
    )

    # Simple tokens
    t_ignore = ' \t'
    t_LPAR = r'\('
    t_RPAR = r'\)'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','
    t_BIG = r'>'
    t_LESS = r'<'
    t_BEQ = r'>='
    t_LEQ = r'<='

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_NUMBER(self, t):
        r"[\d]+"
        t.value = int(t.value)
        return t
    
    def t_ID(self, t):
        r'some|all|value|min|max|exactly|that|not|and|or|Class:|EquivalentTo:|Individuals:|SubClassOf:|DisjointClasses:'
        t.type = self.RESERVED_WORDS[t.value]
        return t
    
    def t_NAMESPACE(self, t):
        r"[a-z]+:[a-z]+"
        return t
    
    def t_CLASS_NAME(self, t):
        r"[A-Z][a-zA-Z_]*"
        return t
    
    def t_PROPRIETY(self, t):
        r"[a-z][a-zA-Z0-9_]*"
        return t

    def t_INDIVIDUAL_NAME(self, t):
        r"[A-Z][a-zA-Z_]*[\d]+"
        return t
    
    def t_error(self, t):
        print(f"Lexical Error: '{t.value}' on line {t.lineno}")
        t.lexer.skip(1)

    def __init__(self, file_path: str):
        self.lexer = lex.lex(module=self)

        if not os.path.exists(file_path):
            raise FileNotFoundError
        
        self.file_path = file_path
        self.file_name = file_path.split("/")[-1]

    def analyse_file(self, symbol_table: ST.SymbolTable) -> ST.SymbolTable:
        with open(self.file_path, "r") as file:
            self.lexer.input(file.read())

        log = []
        for token in self.lexer:
            symbol_table.add_symbol(token.value, token.type)
            log.append(f"{token.lineno} - {token.value} - {token.type}")

        with open(f"../reports/log_{self.file_name}.log", "w") as file:
            file.write("Line - Token - Classification\n")
            for line in log:
                file.write(f"{line}\n")
        
        return symbol_table
