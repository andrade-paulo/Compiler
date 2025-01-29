class OntologyProperty:
    def __init__(self, name: str, operator_token: str, cardinality: int, class_name: str):
        self.name = name
        self.operator_token = operator_token
        self.class_name = class_name
        self.cardinality = cardinality  # Will only be used if the operator's token == "QUANTIFIER"


    def add_class_name(self, class_name: str):
        self.class_name.append(class_name)


    def __str__(self) -> str:
        return f"    Property: {self.name}\n" \
               f"    Operator Token: {self.operator_token}\n" \
               f"    Cardinality: {self.cardinality}\n" \
               f"    Class Name: {self.class_name}\n"


class OntologyClass:
    def __init__(self):
        self.name = None
        self.primary_class_type = None
        self.secondary_types = []
        self.subclass_of = None
        self.equivalent_to = []
        self.disjoint_with = []
        self.individous = []
        self.properties = []


    def set_name(self, name: str):
        self.name = name


    def set_primary_class_type(self, primary_class_type: str):
        self.primary_class_type = primary_class_type


    def add_secondary_type(self, secondary_type: str):
        self.secondary_types.append(secondary_type)


    def set_subclass_of(self, subclass_of: str):
        self.subclass_of = subclass_of


    def add_individual(self, individual_name: str):
        self.individous.append(individual_name)


    def add_disjoint(self, class_name: str):
        self.disjoint_with.append(class_name)


    def add_property(self, propertie_name: str, operator_token: str, cardinality: int, class_name: str, ):
        self.properties.append(OntologyProperty(propertie_name, operator_token, cardinality, class_name))


    def check_closure(self, propertie: str, classes_names: list) -> bool:
        # Get all occourences of the propertie on self.properties
        associated_classes = [prop.class_name for prop in self.properties if (prop.name == propertie and prop.operator_token != "only")]

        # If associated_classes has the same elements as classes_names, return True
        print(associated_classes, classes_names)
        if set(associated_classes) == set(classes_names):
            return True
        
        return False
    

    def __str__(self) -> str:
        return f"Class: {self.name}\n" \
               f"  Primary Class Type: {self.primary_class_type}\n" \
               f"  Secondary Types: {self.secondary_types}\n" \
               f"  Subclass Of: {self.subclass_of}\n" \
               f"  Equivalent To: {self.equivalent_to}\n" \
               f"  Disjoint With: {self.disjoint_with}\n" \
               f"  Individous: {self.individous}\n" \
               f"  Properties: \n" \
               f"{chr(10).join([str(prop) for prop in self.properties])}"
        
