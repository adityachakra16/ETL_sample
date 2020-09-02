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
            self.conn.autocommit = True

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

        print(f"{len(self.data)} records inserted successfully into mobile table")


class QueryHandler:
    def create_schema(self, schemaname):
        query = f"CREATE SCHEMA {schemaname}"
        return query

    def create_table(self, schema, table_structure:dict):
        tablename = table_structure["table_name"]
        attr_str = ""
        for column in table_structure["columns"]:
            attr_str += column + ", "

        if len(table_structure["primary_key"]) > 0:
            attr_str += "PRIMARY KEY ("
            idx = 1
            for pk in table_structure["primary_key"]:
                attr_str += pk
                if idx != len(table_structure["primary_key"]):
                    attr_str += ","
                idx += 1
            attr_str += ")"

        if len(table_structure["unique"]) > 0:
            attr_str += ", UNIQUE ("
            idx = 1
            for u in table_structure["unique"]:
                attr_str += u
                if idx != len(table_structure["unique"]):
                    attr_str += ","
                idx += 1

            attr_str += ")"

        query = f"CREATE TABLE {schema}.{tablename} ({attr_str});"
        return query

    def insert_foreign_key(self, schema, table_structure:dict):
        if len(table_structure["foreign_key"]) == 0:
            return None

        tablename = table_structure["table_name"]
        attr_str = ""
        for fk in table_structure["foreign_key"]:
            attr_str += fk

        query = f"ALTER TABLE {schema}.{tablename} ADD FOREIGN KEY {attr_str}"
        return query

    def create_trigger(self, tablename, trigger_func):
        query = f"CREATE TRIGGER t BEFORE INSERT OR UPDATE OR DELETE ON {tablename}\
                FOR EACH ROW EXECUTE PROCEDURE {trigger_func}"

        return query


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
