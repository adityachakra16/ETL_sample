from postgres import PostgreSQL
from extract import Extract
import psycopg2
import psycopg2.extras
from utils import SingletonDecorator

@SingletonDecorator
class StageDBConnection(object):
    def __init__(self):
        self.conn = None
        self.conn_status = False

    def connect(self, db_name, user, password, host):
        if not self.conn_status:
            try:
                self.conn = psycopg2.connect(dbname=db_name, user=user,
                                    password = password, host = host)
                print (f"Connected to {db_name}")
            except Exception as e:
                print (e)

        return self.conn


class Stage:
    def __init__(self, dataSource, dataSet):
        stagedb = StageDBConnection()
        extractObj = Extract()
        self.qh = QueryHandler()
        try:
            self.conn = stagedb.connect(db_name = "fdadb", user = "postgres", password = "postgres", host="localhost")
            if dataSource == 'csv':
                self.columns, self.data = extractObj.getCSVData(dataSet)
            elif dataSource == 'fda':
                self.columns, self.data = extractObj.getFDAData(dataSet)
            else:
                print ("Data Source not supported")
            funcName = "stage"
            getattr(self, funcName)("Reaction")  #TODO: Hashmap to track db and tables
        except Exception as e:
            print (e)
        finally:
            if self.conn:
                self.conn.close()


    def stage(self, tablename):
        with self.conn.cursor() as cursor:
            psycopg2.extras.execute_batch(cursor, self.qh.insert_data(tablename, self.columns), self.data)
        self.conn.commit()

        print(f"{len(self.data)} records inserted successfully into mobile table")


class QueryHandler:
    def create_table(self, tablename, **kwargs):
        attr_str = ""
        for col_name, props in kwargs.items():
            attr_str += str(col_name) + " " + props + ","

        query = f"CREATE TABLE {tablename} ({attr_str})"

    def insert_data(self, table, columns):
        attr_str = ""
        for col in columns[:len(columns)-1]:
            attr_str += str(col) + ", "
        attr_str += columns[len(columns)-1]
        query = f"INSERT INTO {table} ({attr_str}) VALUES (" + "%s,"*(len(columns)-1) + "%s)"

        return query

    def retreive_data(self, table, columns):
        attr_str = ""
        for col in columns[:len(columns)-1]:
            attr_str += str(col) + ", "
        attr_str += columns[len(columns)-1]

        query = f"SELECT {attr_str} FROM {table}"
        return query
