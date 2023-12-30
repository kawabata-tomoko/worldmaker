import os
import sqlite3 as sql
from collections.abc import Iterable
import pandas as pd
from tesla.configs.globals_elements import LEVEL
from tesla.configs.config_setting import CONFIGS
class TaxonData:
    keys=["FeatureID"]+LEVEL
    def __init__(self,db_name="Taxon_database.db"):
        self.db_name=db_name
        self.state=False
        # self.connect()
        
    def connect(self):
        """
        The function connects to a taxon database and returns a cursor object.
        :return: The method is returning the cursor object.
        """
        if not os.path.exists(self.db_name):
            raise FileNotFoundError(f"{self.db_name} is not vaild taxon database.")
        self.connect = sql.connect(self.db_name)
        self.cursor = self.connect.cursor()
        self.state=True
        return self.cursor
    
    def query_by_name(self,lev,name):
        """
        The function queries a database table called "Taxon" by a specified level and name.
        
        :param lev: The parameter "lev" represents the level of the taxon you want to query. It could be
        a specific level such as "genus", "family", or "order"
        :param name: The name of the taxon you want to query
        :return: the result of executing the SQL command.
        """
        command=f"SELECT * FROM Taxon WHERE [{lev}]='{name}'"
        return self.execute(command)
    
    def query_by_id(self,feature):
        """
        The function queries the Taxon table in a database by a given feature ID.
        
        :param feature: The `feature` parameter is a string that represents the ID of a specific feature
        :return: the result of executing the SQL command.
        """
        command=f"SELECT * FROM Taxon WHERE FeatureID='{feature}'"
        return self.execute(command)
    
    def add_record(self,record):
        """
        The function `add_record` inserts a record into a database table called "Taxon" using the
        provided record dictionary or iterable.
        
        :param record: The `record` parameter is the data that you want to add to the database table. It
        can be either a dictionary or an iterable (such as a list or tuple). The keys of the dictionary
        or the indices of the iterable correspond to the column names of the table, and the values
        correspond to
        """
        if type(record)==dict:
            values=(record[i] if i in record else 'Unknown' for i in self.keys)
        elif isinstance(record,Iterable):
            values=(record[i] if i<len(record) else 'Unknown' for i in range(self.keys))
        else:
            raise TypeError("Not valid type.")
        command=f"INSERT INTO Taxon {str(tuple(self.keys))} VALUES {str(values)};"
        self.execute(command)
        self.cursor.commit()
        
    def delete_record_by_id(self,feature):
        """
        The function deletes a record from the Taxon table based on the provided feature ID.
        
        :param feature: The `feature` parameter is the ID of the record that you want to delete from the
        `Taxon` table
        """
        command=f"DELETE FROM Taxon WHERE FeatureID='{feature}'"
        self.execute(command)
        self.cursor.commit()
        
    def delete_record_by_name(self,lev,name):
        """
        The function deletes a record from the Taxon table based on the specified level and name.
        
        :param lev: The parameter "lev" represents the level of the taxonomic rank, such as kingdom,
        phylum, class, order, family, genus, or species
        :param name: The `name` parameter is the name of the record that you want to delete from the
        database table
        """
        command=f"SELECT * FROM Taxon WHERE [{lev}]='{name}'"
        self.execute(command)
        self.cursor.commit()
        
    def execute(self,command):
        """
        The function executes a given command using a cursor and returns the formatted result.
        
        :param command: The `command` parameter is a string that represents a SQL query or command that
        you want to execute on a database
        :return: The code is returning the result of executing the SQL command and formatting the
        fetched data.
        """
        self.cursor.execute(command)
        return self.formatter(self.cursor.fetchall())
    
    def formatter(self,results):
        """
        The function takes a list of lists and converts it into a list of dictionaries using the keys
        provided.
        
        :param results: The "results" parameter is a list of lists. Each inner list represents a row of
        data, and each element in the inner list represents a column value
        :return: a list of dictionaries. Each dictionary in the list is created by mapping the keys from
        the `self.keys` list to the corresponding values in each item of the `results` list.
        """
        return [{self.keys[i]:item[i] for i in range(len(item))} for item in results]
    
    def close(self):
        """
        The close function closes the cursor and connection and sets the state to False.
        """
        if hasattr(self,"cursor"):
            self.cursor.close()
        if isinstance(self.connect, sql.Cursor):
            self.connect.close()
        self.state=False
    @staticmethod
    def to_tax(infos):
        return pd.DataFrame.from_records(infos,index="FeatureID")
    
TAXON_DB=TaxonData(f"{CONFIGS.common.defaults()['database']}/Taxon_database.db")
TAXON_DB.connect()
# __all__=["TAXON_DB"]