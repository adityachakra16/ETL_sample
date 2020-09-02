from stage import QueryHandler
from stage import StageDBConnection
import psycopg2

class DBSetup:
    def __init__(self, schema):
        self.qh = QueryHandler()
        stagedb =  StageDBConnection()
        try:
            self.conn = stagedb.connect(db_name = "fdadb", user = "postgres", password = "postgres", host="localhost")
            self.conn.autocommit = True

            funcName = "create_schema"
            getattr(self, funcName)(schema)
        except Exception as e:
            print (e)
        finally:
            if self.conn:
                self.conn.close()

    def create_table_migration_files(self, tablename):
        f = open(tablename + ".sql", w)
        f.write(self.qh.create_table(tablename))
        f.close()


    def create_schema(self, schema):
        cursor = self.conn.cursor()

        for k, v in schema.items():
            query = self.qh.create_table(v)
            if query:
                cursor.execute(query)
                print (f"{k} table created")

        for k, v in schema.items():
            query = self.qh.insert_foreign_key(v)
            if query:
                cursor.execute(query)
                print (f"Foreign keys for {k} inserted")
