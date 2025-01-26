import ply.yacc as yacc
from LexicalAnalyser import LexicalAnalyser


class SyntacticAnalyser:
    RESERVED_WORDS = LexicalAnalyser.RESERVED_WORDS
    tokens = LexicalAnalyser.tokens

    
    start = "ontology"

    def p_ontology(self, p):
        """ontology : primitive_class_header
                    | primitive_class_header ontology"""


    # Primitive    
    def p_primitive_class_header(self, p):
        """primitive_class_header : CLASS CLASS_NAME SUBCLASS subclass_header primitive_class_expression
                                  | CLASS CLASS_NAME SUBCLASS primitive_class_expression subclass_header"""
        self.classes_table[p[2]] = "Class"

    def p_primitive_class_expression(self, p):
        """primitive_class_expression : DISJOINT disjoint_expression primitive_class_expression
                                      | INDIVIDUALS individuals_expression primitive_class_expression
                                      | DISJOINT disjoint_expression
                                      | INDIVIDUALS individuals_expression"""


    def p_subclass_header(self, p):
        """subclass_header : CLASS_NAME
                           | CLASS_NAME COMMA subclass_expression"""
        self.classes_table[p[1]] = "SUPCLASS"
        
    def p_subclass_expression(self, p):
        """subclass_expression : PROPRIETY SOME CLASS_NAME
                               | PROPRIETY ONLY CLASS_NAME
                               | subclass_expression LOGICAL subclass_expression
                               | PROPRIETY QUANTIFIER NUMBER CLASS_NAME
                               | LPAR subclass_expression RPAR
                               | subclass_expression COMMA subclass_expression"""
        
    
    def p_disjoint_expression(self, p):
        """disjoint_expression : CLASS_NAME
                               | disjoint_expression COMMA disjoint_expression"""
        self.classes_table[p[1]] = "DISJOINT"


    def p_individuals_expression(self, p):
        """individuals_expression : INDIVIDUAL_NAME"""
        self.classes_table[p[1]] = "INDIVIDUALS"


    # Errors
    def p_error(self, p):
        print(f"Syntax error at {p.value}")
        print("Syntax Analysis Failed!")


    def __init__(self, file_path):
        self.parser = yacc.yacc(module=self)
        self.classes_table = {}
        self.file_path = file_path


    def analyse_file(self) -> None:
        with open(self.file_path, "r") as file:
            data = file.read()
            self.parser.parse(data)
        
        # log classes
        with open("classes.txt", "w") as file:
            for class_name, class_type in reversed(self.classes_table.items()):
                if class_type != "Class":
                    file.write(f" -> {class_name} - {class_type}\n")
                else:
                    file.write(f"{class_name} - {class_type}\n")
