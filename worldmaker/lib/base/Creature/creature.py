# # from worldmaker.lib.base import Location
import sqlite3
import numpy as np
from worldmaker.configs import CONFIGS
class CreatureManager(object):##负责CreatureUnit管理、与数据库进行交互
    def __init__(self,db_path):
        self.db_path=f'{CONFIGS["COMMON"]["database"]}/creatures.db' if db_path is None else db_path

class Feature:
    def __init__(self, name:str, ftype: str, dtype:str, valueset: set, description=None,distribution=None):
        
        self.name = name
        self.ftype=ftype# "discrete"|"continuous":how does the feature preform?
        self.dtype=dtype# "physical"|"magical"|"mental"
        self.values = valueset
        self.distribution = distribution

    def generate_values(self, size):
        if self.distribution is not None:
            return self.distribution.rvs(size)
        else:
            return np.random.choice(self.values, size=size)

class CreatureUnit(object):#生物单元，存储生物信息
    def __init__(self,id,name) -> None:
        self.id=id
        self.name=name
    def gender_system(self,gender_set: set,gender_ratio: dict):
        self.gender_set=gender_set
        self.gender_ratio=gender_ratio
        self.gender_generator=lambda size:np.random.choice(
            list(gender_ratio.keys()), 
            size=size, 
            p=list(gender_ratio.values())
            )

    

# # class Creature(object):
# #     def __init__(self,name:str,location:Location,age:float,gender,taxonomy):
        
        
        
# class Creature:
#     def __init__(self, name, classification=None):
#         self.name = name
#         self.classification = classification or {}

#     def get_classification(self):
#         return self.classification

#     def set_classification(self, classification):
#         self.classification = classification

#     def __str__(self):
#         return f"{self.name} - {self.classification}"
