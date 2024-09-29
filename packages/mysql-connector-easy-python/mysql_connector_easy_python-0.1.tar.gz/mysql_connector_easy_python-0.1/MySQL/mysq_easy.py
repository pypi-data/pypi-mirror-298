from database import MySQL

# ========================= #

class Database(MySQL) :
    "Create table function"
    def create_table(self,table_name:str,**kwargs) :
        "Enter the table name -> str -> create_table('Test',a='INTEGER',...)"
        keys = list(kwargs.keys())
        keys_ = []
        for i in keys:
            keys_.append(f"{i} {kwargs[i]}")
    
        command = f"""CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join(keys_)}
        )
        """
        try :
            db = self.database()
            cursor = db.cursor()
            cursor.execute(command)
            db.commit() 
            return 
        except Exception as Error :
            raise Error
    # ======================= #
    "Insert vlaue into db"
    def insert_value(self,table_name:str,**kwargs) :
        try :
            db = self.database()
            cursor = db.cursor()
            sql = f"INSERT INTO {table_name} ({', '.join(list(kwargs.keys()))}) VALUES ({', '.join(['%s'] * len(kwargs)) })"
            cursor.execute(sql, tuple(kwargs.values())) 
            db.commit()
        except Exception as Error :
            raise Exception(Error)
    # ======================= #
    def get_values(self,table_name:str) -> list :
        try :
            db = self.database()
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            result = cursor.fetchall()
            return result
        except Exception as Error :
            raise Error