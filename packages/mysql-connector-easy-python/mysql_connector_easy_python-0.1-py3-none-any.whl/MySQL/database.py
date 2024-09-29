# === [ Create _ connect DB ] === #

from mysql.connector import connect

# =============================== #

class MySQL :
    def __init__(self,
                 username:str,
                 password:str,
                 database:str,
                 host:str="localhost"
    ) :
        self.host = host # get host from user  
        self.username = username # get db username from user 
        self.password = password # get db password from user
        self.databasee_name = database # get db  name from user

        "''''''''''''''''''''''''"
        self.connect_database = self.connect_database
        self.database = self.connect_database
    # ========================= #
    def connect_database(self) :
        try :
            database = connect(
                host = self.host ,
                user = self.username ,
                password = self.password ,
                database = self.databasee_name
            )
            return database
        except Exception as Error :
            raise Exception(Error)
    # ========================= #