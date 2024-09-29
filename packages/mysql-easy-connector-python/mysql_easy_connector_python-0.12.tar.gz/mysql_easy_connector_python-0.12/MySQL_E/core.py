from database import MyDatabase

# ====================== #

class Database(MyDatabase) :          
    # "Create table in the db"
    def create_table(self,table_name:str,**kwargs) :
        """
        Put their values and input type in kwargs
        """


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
    # "Insert value in the table"
    def insert_value(self,table_name:str,**kwargs) :
        try :
            db = self.database()
            cursor = db.cursor()
            sql = f"INSERT INTO {table_name} ({', '.join(list(kwargs.keys()))}) VALUES ({', '.join(['%s'] * len(kwargs)) })"
            cursor.execute(sql, tuple(kwargs.values())) 
            db.commit()
        except Exception as Error :
            raise Error
    # get all values
    def get_all_values(self,table_name:str) -> list:
        try :
            db = self.database()
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            result = cursor.fetchall()
            return result
        except Exception as Error :
            raise Error