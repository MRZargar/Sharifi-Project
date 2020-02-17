# import enum
import psycopg2

# class ColumnType(enum.Enum):
#     SERIAL = "SERIAL"
#     INT = "INTEGER"
#     DOUBLE = "DOUBLE PRECISION"
#     VARCHAR50 = "VARCHAR(50)"
#     VARCHAR100 = "VARCHAR(100)"

#     def __str__(self):
#         return self.value

# class Property(enum.Enum):
#     PRIMARY_KEY = "PRIMARY KEY"
#     NOT_NULL = "NOT NULL"

#     def __str__(self):
#         return self.value

# class Operator(enum.Enum):
#     EQUAL = "="
#     GREATER_THAN_OR_EQUAL = ">="
#     GREATER_THAN = ">"
#     LESS_THAN_OR_EQUAL = "<="
#     LESS_THAN = "<"
#     NOT_EQUAL = "<>"
#     LIKE = "LIKE"
#     AND = "AND"
#     OR = "OR"
#     BETWEEN = "BETWEEN"
#     IS_NULL = "IS NULL"
#     IS_NOT_NULL = "IS NOT NULL"
#     IN = "IN"

#     def __str__(self):
#         return self.value


class pgDB:
    def __init__(self, host, database, user, password):
        self.db = {}
        self.db["host"] = host
        self.db["database"] = database
        self.db["user"] = user
        self.db["password"] = password

    # def __init__(self, initFile, section):
    #     from configparser import ConfigParser

    #     parser = ConfigParser()
    #     parser.read_file(initFile)

    #     self.db = {}
    #     if parser.has_section(section):
    #         params = parser.items(section)
    #         for param in params:
    #             self.db[param[0]] = param[1]
    #     else:
    #         raise Exception('Section {0} not found in the {1} file'.format(section, initFile))
    
    def __connect(self):
        self.conn = None
        self.conn = psycopg2.connect(**self.db)
    
    def __disconnect(self):
        if self.conn is not None:
            self.conn.close()

    def __commit(self):
        self.conn.commit()

    def setQuery(self, sql):
        try:
            self.__connect()
            
            cur = self.conn.cursor()
            cur.execute(sql)
            cur.close()

            self.__commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.__disconnect()

    def getQuery(self, sql):
        try:
            self.__connect()
            
            cur = self.conn.cursor()
            cur.execute(sql)

            rows = cur.fetchall()

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.__disconnect()
            return rows

    # def createTable(self, name, *columnsName):
    #     sql = "CREATE TABLE " + name + "("
    #     for column in columnsName:
    #         for item in column:
    #             sql = sql + str(item) + " "
    #         sql = sql + ", "
    #     sql = sql[:-2] + ")"

    #     self.setQuery(sql)

    # def insert(self, tableName, **columnsName_columnsValue):
    #     sql = "INSERT INTO " + tableName + "("
        
    #     for name, value in columnsName_columnsValue.items():
    #         sql = sql + str(name) + ", "

    #     sql = sql[:-2] + ") VALUES ("
        
    #     for name, value in columnsName_columnsValue.items():
    #         if type(value) == type(""):
    #             sql = sql + '\'' + str(value) + "\', "
    #         else:
    #             sql = sql + str(value) + ", "
        
    #     sql = sql[:-2] + ")"

    #     self.setQuery(sql)


# ------------------------------------------------------------------------------------------------

# DB = pgDB("localhost", "test", "zargar", "Z@rgar76")

# DB.createTable("pythnTable", ("id", ColumnType.INT, Property.PRIMARY_KEY),
#                              ("name", ColumnType.VARCHAR50, Property.NOT_NULL), 
#                              ("alaki", ColumnType.DOUBLE))

# DB.insert("pythnTable", id = 1, name = "zargar", alaki = 132543541.12435454)

# print(DB.getQuery("select * from pythntable"))