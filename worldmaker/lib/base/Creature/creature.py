from worldmaker.lib.base import Location


class Creature(object):
    def __init__(self,name:str,location:Location,age:float,gender,taxonomy):
        
        
        
class Creature:
    def __init__(self, name, classification=None):
        self.name = name
        self.classification = classification or {}

    def get_classification(self):
        return self.classification

    def set_classification(self, classification):
        self.classification = classification

    def __str__(self):
        return f"{self.name} - {self.classification}"
