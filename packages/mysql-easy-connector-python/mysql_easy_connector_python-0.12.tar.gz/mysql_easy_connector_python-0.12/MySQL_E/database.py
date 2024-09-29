from mysql.connector import connect
# ====================== #

class MyDatabase :
    def __init__(self,
                 username:str,
                 password:str,
                 database:str,
                 host:str="localhost") :
        self.host = host
        self.username = username
        self.password = password
        self.databasee_ = database
        self.connect = self.connect
        self.database = self.connect

    # ================ #
    def connect(self) :
        try :
            database = connect(
                host = self.host ,
                user = self.username ,
                password = self.password ,
                database = self.databasee_
            )
            
            return database
        except Exception as Error :
            raise Error
    # ================ #