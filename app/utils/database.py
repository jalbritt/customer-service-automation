from psycopg2 import connect


class Database:
    def __init__(self):
        self.user = 'myuser'
        self.password = 'mypassword'
        self.host = 'localhost'
        self.port = '5432'
        self.dbname = 'mydb'
        self.conn = None


def ConnectPostgres(self):
    try:
        conn = connect(user=self.user, password=self.password, host=self.host, port=self.port, dbname=self.dbname)
        return conn
    except Exception as e:
        # TODO: Log the error
        print(e)
        return None
