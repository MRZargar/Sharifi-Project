import psycopg2

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