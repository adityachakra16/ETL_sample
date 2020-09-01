from utils import SingletonDecorator

@SingletonDecorator
class WarehouseDBConnection(object):
    def __init__(self):
        self.start = None

    def connect(self, db_name, user, password, host):
        if not self.conn_status:
            try:
                self.conn = psycopg2.connect(dbname=db_name, user=user,
                                    password = password, host = host)
                print (f"Connected to {db_name}")
            except Exception as e:
                print (e)

        return self.conn.cursor()

class Warehouse:
    def __init__(self):
        pg = PostgreSQL()



class WarehouseQueryHandler:
    def insert_currency_data():
        pass

    def insert_prices_data():
        pass
