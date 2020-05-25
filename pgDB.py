import psycopg2

class pgDB:
    def __init__(self, host = "", database = "", user = "", password = ""):
        self.remote_db = {}
        self.db = {}
        self.db["host"] = host
        self.db["database"] = database
        self.db["user"] = user
        self.db["password"] = password

    def dblink(self, host = "", database = "", user = "", password = ""):
        self.remote_db["host"] = host
        self.remote_db["database"] = database
        self.remote_db["user"] = user
        self.remote_db["password"] = password

    def __connect(self):
        self.conn = None
        self.conn = psycopg2.connect(**self.db)
    
    def __disconnect(self):
        if self.conn is not None:
            self.conn.close()

    def __dblink_get_connstr(self):
        connstr = ""
        if self.remote_db["host"] != "":
            connstr += "host={}".format(self.remote_db["host"]) + " "
        if self.remote_db["database"] != "":
            connstr += "dbname={}".format(self.remote_db["database"]) + " "
        if self.remote_db["user"] != "":
            connstr += "user={}".format(self.remote_db["user"]) + " "
        if self.remote_db["password"] != "":
            connstr += "password={}".format(self.remote_db["password"])
        
        return connstr

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

            self.__disconnect()
            return rows
        except (Exception, psycopg2.DatabaseError) as error:
            self.__disconnect()
            print(error)
    
    def dblink_get(self, sql, AS):
        connstr = self.__dblink_get_connstr()

        sql = """select * from dblink('{}','{}') as {};""".format(connstr, sql, AS)
        
        return self.getQuery(sql)

    def dblink_set(self, sql):
        connstr = self.__dblink_get_connstr()

        sql = """SELECT dblink_connect('{}');
                select dblink('{}');""".format(connstr, sql)
        
        return self.getQuery(sql)