from datetime import datetime
import ply.yacc as yacc
from LexicalAnalyser import LexicalAnalyser
import ClassTable as CT


class SyntacticAnalyser:
    RESERVED_WORDS = LexicalAnalyser.RESERVED_WORDS
    tokens = LexicalAnalyser.tokens
    
    start = "ontology"


    def __init__(self, file_path: str):
        self.file_path = file_path
        self.classes_table = {}
        self.errors = []
        self.parser = yacc.yacc(module=self)


    def correct_line(self, lineno: int) -> int:
        return (lineno + 1) - self.file_lines_number


    def p_ontology(self, p):
        """ontology : primitive_class_header
                    | primitive_class_header ontology
                    | defined_class_header
                    | defined_class_header ontology"""

   
    def p_primitive_class_header(self, p):
        """primitive_class_header : CLASS CLASS_NAME SUBCLASS subclass_header 
                                  | CLASS CLASS_NAME SUBCLASS subclass_header class_expression"""
        
        # Swap the class name from "NEW_CLASS" to the correct one
        self.classes_table[p[2]] = self.classes_table["NEW_CLASS"]
        self.classes_table.pop("NEW_CLASS", None)

        # Set name and type
        self.classes_table[p[2]].set_name(p[2])
        self.classes_table[p[2]].set_primary_class_type("Primitive Class")


    def p_defined_class_header(self, p):
        """defined_class_header : CLASS CLASS_NAME EQUIVALENT equivalent_expression
                                | CLASS CLASS_NAME EQUIVALENT equivalent_expression SUBCLASS subclass_header
                                | CLASS CLASS_NAME EQUIVALENT equivalent_expression class_expression
                                | CLASS CLASS_NAME EQUIVALENT equivalent_expression SUBCLASS subclass_header class_expression"""
        
        # Swap the class name from "NEW_CLASS" to the correct one
        self.classes_table[p[2]] = self.classes_table["NEW_CLASS"]
        self.classes_table.pop("NEW_CLASS", None)

        # Set name and type
        self.classes_table[p[2]].set_name(p[2])
        self.classes_table[p[2]].set_primary_class_type("Defined Class")


    def p_defined_class_header_error(self, p):
        """defined_class_header : CLASS CLASS_NAME SUBCLASS subclass_header EQUIVALENT equivalent_expression
                                | CLASS CLASS_NAME SUBCLASS subclass_header EQUIVALENT equivalent_expression class_expression"""
        self.errors.append(f"(Line {self.correct_line(p.lineno(3))}) Operator Precedence Error: EQUIVALENT and SUBCLASS must be declared respectively")


    def p_class_expression(self, p):
        """class_expression : DISJOINT disjoint_expression INDIVIDUALS individuals_expression"""

    def p_class_expression_error(self, p):
        """class_expression : DISJOINT disjoint_expression
                            | INDIVIDUALS individuals_expression"""
        self.errors.append(f"(Line {self.correct_line(p.lineno(1))}) Operator Precedence Error: DISJOINT and INDIVIDUALS must be declared respectively")


    def p_equivalent_expression(self, p):
        """equivalent_expression : CLASS_NAME
                                 | CLASS_NAME COMMA equivalent_expression"""
        
        if "NEW_CLASS" not in self.classes_table.keys():
            self.classes_table["NEW_CLASS"] = CT.OntologyClass()
        
        self.classes_table["NEW_CLASS"].equivalent_to.append(p[1])


    def p_subclass_header(self, p):
        """subclass_header : CLASS_NAME
                           | CLASS_NAME COMMA subclass_expression"""
        
        if "NEW_CLASS" not in self.classes_table.keys():
            self.classes_table["NEW_CLASS"] = CT.OntologyClass()

        self.classes_table["NEW_CLASS"].set_subclass_of(p[1])

        # Check closure
        if "Closure Class" in self.classes_table["NEW_CLASS"].secondary_types:
            # Search for the closure property
            for prop in self.classes_table["NEW_CLASS"].properties:
                if prop.operator_token == "only":
                    if not self.classes_table["NEW_CLASS"].check_closure(prop.name, prop.class_name.split(", ")):
                        self.errors.append(f"Closure Error: There's an inconsistency on the closure of {prop.name}")


    def p_subclass_expression(self, p):
        """subclass_expression : PROPRIETY SOME CLASS_NAME 
                               | PROPRIETY SOME CLASS_NAME COMMA subclass_expression
                               | LPAR PROPRIETY SOME CLASS_NAME RPAR
                               | LPAR PROPRIETY SOME CLASS_NAME RPAR LOGICAL subclass_expression

                               | PROPRIETY QUANTIFIER NUMBER CLASS_NAME
                               | PROPRIETY QUANTIFIER NUMBER CLASS_NAME COMMA subclass_expression
                               | LPAR PROPRIETY QUANTIFIER NUMBER CLASS_NAME RPAR
                               | LPAR PROPRIETY QUANTIFIER NUMBER CLASS_NAME RPAR LOGICAL subclass_expression
                               
                               | PROPRIETY ONLY CLASS_NAME
                               | PROPRIETY ONLY LPAR closure_classes RPAR"""

        if "NEW_CLASS" not in self.classes_table.keys():
            self.classes_table["NEW_CLASS"] = CT.OntologyClass()

        if p[1] not in ['(', None]:
            if p.slice[2].type == "QUANTIFIER":
                self.classes_table["NEW_CLASS"].add_property(p[1], p[2], p[3], p[4])
            else:
                if p[3] == '(':  # Skip (
                    p[3] = ", ".join(p[4])  # p[4] is a list of classes
                
                self.classes_table["NEW_CLASS"].add_property(p[1], p[2], None, p[3])
        
        if p[2] == "only":
            self.classes_table["NEW_CLASS"].add_secondary_type("Closure Class")
        

    def p_closure_classes(self, p):
        """closure_classes : CLASS_NAME
                           | CLASS_NAME LOGICAL closure_classes
                           | CLASS_NAME COMMA closure_classes"""
        p[0] = []

        for i in p[1:]:
            if i not in [',', 'or']:  # Ignore the comma and the logical operator
                if isinstance(i, list):  # Unpack the list
                    p[0] += i
                else:
                    p[0].append(i)

    
    def p_disjoint_expression(self, p):
        """disjoint_expression : CLASS_NAME
                               | CLASS_NAME COMMA disjoint_expression"""
        
        if "NEW_CLASS" not in self.classes_table.keys():
            self.classes_table["NEW_CLASS"] = CT.OntologyClass()
        
        self.classes_table["NEW_CLASS"].add_disjoint(p[1])


    def p_individuals_expression(self, p):
        """individuals_expression : INDIVIDUAL_NAME
                                  | INDIVIDUAL_NAME COMMA individuals_expression"""
        
        if p[1]:
            if "NEW_CLASS" not in self.classes_table.keys():
                self.classes_table["NEW_CLASS"] = CT.OntologyClass()
            
            self.classes_table["NEW_CLASS"].add_individual(p[1])


    # Errors
    def p_error(self, p):
        if p:
            self.errors.append(f"(Line {self.correct_line(p.lineno)}) Syntax error at \"{p.value}\"")
        else:
            self.errors.append("Syntax Analysis Failed!")


    def analyse_file(self) -> None:
        with open(self.file_path, "r") as file: 
            data = file.read()
            self.file_lines_number = len(data.split("\n"))
            self.parser.parse(data)
        
        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # log classes
        with open("classes.txt", "w") as file:
            file.write(f"Log ({date_time})\n")
            file.write(f"{len(self.classes_table.keys())} Valid Classes\n\n")

            for class_name, class_data in self.classes_table.items():
                file.write(f"{class_data}\n\n")

        # log errors
        if self.errors:
            with open("errors.txt", "w") as file:
                file.write(f"Log ({date_time})\n\n")
                for error in self.errors:
                    file.write(f"{error}\n")
