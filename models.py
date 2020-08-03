from abc import ABCMeta, abstractmethod

# Abstract Visitee
class Word:
    __metaclass__ = ABCMeta

    @abstractmethod
    def accept(self, visitor):
        pass


# Concept Visitee
class Concept(Word):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        visitor.visit_concept(self)


# Aspect Visitee
class Aspect(Word):
    def __init__(self, name):
        self.name = name
        self.particle = None

    def accept(self, visitor):
        visitor.visit_aspect(self)


# Characteristic Visitee
class Characteristic(Word):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        visitor.visit_characteristic(self)


# Property Visitee
class Property(Word):
    def __init__(self, name):
        self.name = name
        self.concept = None
        self.particle = None
        self.branch = None

    def accept(self, visitor):
        visitor.visit_property(self)


# Absctarct Visitor
class WordVisitor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_concept(self, element):
        pass

    @abstractmethod
    def visit_property(self, element):
        pass

    @abstractmethod
    def visit_aspect(self, element):
        pass

    @abstractmethod
    def visit_characteristic(self, element):
        pass


# Concrete Visitor
class NaturalLanguageTransformer(WordVisitor):
    def __init__(self, body):
        self.body = body

    def visit_concept(self, concept):
        self.body = self.body + f" the {concept.name}"

    def visit_property(self, property_):
        if property_.branch:
            self.body = (
                self.body
                + f" {property_.name} {property_.particle} {property_.branch}."
            )
        else:
            self.body = self.body + f" {property_.name}."

    def visit_aspect(self, aspect):
        if aspect.particle:
            self.body = self.body + f" {aspect.name} {aspect.particle}"
        else:
            self.body = self.body + f" {aspect.name}"

    def visit_characteristic(self, characteristic):
        self.body = self.body + f" {characteristic.name}"

