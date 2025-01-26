import SymbolTable as ST

import os
import ply.lex as lex

from ply.lex import TOKEN


class LexicalAnalyser:
    RESERVED_WORDS = {
        "some": "SOME", "all": "ALL", "only": "ONLY", "value": "QUANTIFIER", "min": "QUANTIFIER", "max": "QUANTIFIER", "exactly": "QUANTIFIER", 
        "that": "LOGICAL", "not": "LOGICAL", "and": "LOGICAL", "or": "LOGICAL", 
        "Class:": "CLASS", "EquivalentTo:": "EQUIVALENT", "Individuals:": "INDIVIDUALS", "SubClassOf:": "SUBCLASS", "DisjointClasses:": "DISJOINT", "DisjointWith:": "DISJOINT"
    }

    tokens = [
        "NUMBER", "LPAR", "RPAR", "LCURLY", "RCURLY", "LBRACKET", "RBRACKET", "COMMA", "BIG", "LESS", "BEQ", "LEQ", "ID",
        "CLASS_NAME", "PROPRIETY", "INDIVIDUAL_NAME", "NAMESPACE"
    ] + list(set(RESERVED_WORDS.values()))
    

    # Simple tokens
    reserved_regex =  '|'.join(RESERVED_WORDS.keys())
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


    @TOKEN(reserved_regex)
    def t_ID(self, t: lex.LexToken) -> lex.LexToken:
        t.type = self.RESERVED_WORDS[t.value]
        return t
    
    def t_newline(self, t: lex.LexToken) -> lex.LexToken:
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_NUMBER(self, t: lex.LexToken) -> lex.LexToken:
        r"[\d]+"
        t.value = int(t.value)
        return t
    
    def t_NAMESPACE(self, t: lex.LexToken) -> lex.LexToken:
        r"[a-z]+:[a-z]+"
        return t

    def t_INDIVIDUAL_NAME(self, t: lex.LexToken) -> lex.LexToken:
        r"[[A-Z][a-zA-Z_]*[0-9]+"
        return t

    def t_CLASS_NAME(self, t: lex.LexToken) -> lex.LexToken:
        r"[A-Z][a-zA-Z_]*"
        return t
    
    def t_PROPRIETY(self, t: lex.LexToken) -> lex.LexToken:
        r"[a-z][a-zA-Z0-9_]*"
        return t
    
    
    def t_error(self, t: lex.LexToken) -> None:
        print(f"Lexical Error: '{t.value}' on line {t.lineno}")
        t.lexer.skip(1)


    def __init__(self, file_path: str) -> None:
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

        with open(f"../reports/log_lex_{self.file_name}.log", "w") as file:
            file.write("Line - Token - Classification\n")
            for line in log:
                file.write(f"{line}\n")
        
        return symbol_table
