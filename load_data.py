import psycopg2
import pandas as pd

class QueryHandler:
    def insert_economy_data():
        query = "INSERT INTO economy (year, gdb_in_c) VALUES (%s, %s)"
        return query

    def insert_pollution_data():
        query = "INSERT INTO pollution (city, country, parameter, value, unit) VALUES (%s, %s, %s, %s, %s)"
        return query

    def insert_crypto_data():
        pass

class PostgreSQL:
    def __init__(self, user, password, host, db_name, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.qh = QueryHandler()
        try:
            print (f"Connection attempt to {self.db_name} by {self.user} on {self.host} ...")
            self.conn = psycopg2.connect(dbname=self.db_name, user=self.user,
                                    password = self.password, host = self.host)
            print ("Connected!")
            self.cur = self.conn.cursor()
        except Exception as e:
            print ("Cannot connect to PostgreSQL server")
            print (e)

    def create_tables(self):
        pass

    def delete_tables(self):
        pass

    def insert_into_db(self, data):
        for index, row in data.iterrows():
            self.cur.execute(self.qh.insert_pollution_data(), (row['city'], row['country'], row['parameter'], row['value'], row['unit']))
            self.conn.commit()

    def delete_from_db(self, data):
        pass
