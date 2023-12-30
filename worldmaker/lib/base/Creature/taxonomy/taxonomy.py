import sqlite3
from worldmaker.configs import CONFIGS
from worldmaker.lib.base.Creature.creature import Creature

class TaxonomyManager:
    def __init__(self, db_path=None,levels=None, table="taxonomy"):
        self.db_path=f'{CONFIGS["COMMON"]["database"]}/creatures.db' if db_path is None else db_path
        self.levels=CONFIGS["CREATURE"]["levels"] if levels is None else levels
        self.conn = sqlite3.connect(db_path)
        self.table=table
        self.create_table()


    def create_table(self):
        cursor = self.conn.cursor()
        levstr=''.join([f'[{lev}] TEXT,\n' for lev in self.levels]).strip(",\n")
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                {levstr}
            )
        ''')
        self.conn.commit()

    def add_creature(self, creature):
        cursor = self.conn.cursor()
        cursor.execute(
            f'''
                INSERT INTO {self.table} (name, [{'], ['.join(self.levels)}])
                VALUES (?, {", ".join(["?" for _ in range(len(self.levels))])})
            ''', 
            (creature.name, *[creature1.classification.get(lev) for lev in self.levels])
        )
        self.conn.commit()
    def get_all_tax(self):
        
    def get_all_creatures(self):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table}')
        rows = cursor.fetchall()

        creatures = []
        for row in rows:
            creature = Creature(row[1], {
                "Kingdom": row[2],
                "Phylum": row[3],
                "Class": row[4],
                "Order": row[5],
                "Family": row[6],
                "Genus": row[7],
                "Species": row[8],
            })
            creatures.append(creature)

        return creatures

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

import sqlite3

class Creature:
    def __init__(self, name, species, genus, family):
        self.name = name
        self.species = species
        self.genus = genus
        self.family = family


# 创建数据库
conn = sqlite3.connect('taxonomy.db')
c = conn.cursor()

# 创建表
c.execute('''CREATE TABLE creatures
             (name text, species text, genus text, family text)''')

# 插入数据
creature1 = Creature('Lion', 'Panthera leo', 'Panthera', 'Felidae')
creature2 = Creature('Tiger', 'Panthera tigris', 'Panthera', 'Felidae')
creature3 = Creature('Polar Bear', 'Ursus maritimus', 'Ursus', 'Ursidae')
creature4 = Creature('Grizzly Bear', 'Ursus arctos horribilis', 'Ursus', 'Ursidae')

taxonomy = Taxonomy()
taxonomy.add_creature(creature1)
taxonomy.add_creature(creature2)
taxonomy.add_creature(creature3)
taxonomy.add_creature(creature4)

for creature in taxonomy.creatures:
    c.execute("INSERT INTO creatures VALUES (?, ?, ?, ?)", (creature.name, creature.species, creature.genus, creature.family))

# 提交更改并关闭连接
conn.commit()
conn.close()
