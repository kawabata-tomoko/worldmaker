import sqlite3

class TaxonomyManager:
    def __init__(self, db_path="taxonomy.db",levels=["kingdom"]):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS creatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                kingdom TEXT,
                phylum TEXT,
                clazz TEXT,
                order_name TEXT,
                family TEXT,
                genus TEXT,
                species TEXT
            )
        ''')
        self.conn.commit()

    def add_creature(self, creature):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO creatures (name, kingdom, phylum, clazz, order_name, family, genus, species)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (creature.name, creature.classification.get("Kingdom"), creature.classification.get("Phylum"),
              creature.classification.get("Class"), creature.classification.get("Order"),
              creature.classification.get("Family"), creature.classification.get("Genus"),
              creature.classification.get("Species")))
        self.conn.commit()

    def get_all_creatures(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM creatures')
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
