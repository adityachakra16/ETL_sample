from stage import QueryHandler
from stage import StageDBConnection
import psycopg2

class Logging:
    def __init__(self, query_handler, logschemaname, logtablename, logtable_structure, cursor, funcName):
        self.funcName = funcName
        self.qh = query_handler
        cursor.execute(self.qh.create_schema(logschemaname))
        print ("Logging schema created")
        cursor.execute(self.qh.create_table(logtablename, logtable_structure))
        print ("Logging table created")
        #sql_file = open('sql/change_trigger.sql','r')
        #cursor.execute(sql_file.read())
        #sql_file.close()

    def __call__(self, schemaname, tablename, cursor):
        cursor.execute(self.qh.create_trigger(schemaname, tablename, self.funcName))
        print (f"Change trigger created for {schemaname}.{tablename}")


class DBSetup:
    def __init__(self, schema, schemaname, logging=None):
        self.qh = QueryHandler()
        stagedb =  StageDBConnection()
        try:
            self.conn = stagedb.connect(db_name = "fdadb", user = "postgres", password = "postgres", host="localhost")
            self.conn.autocommit = True

            funcName = "create_schema"
            getattr(self, funcName)(schema, schemaname, logging)
        except Exception as e:
            print (e)
        finally:
            if self.conn:
                self.conn.close()

    def create_table_migration_files(self, tablename):
        f = open(tablename + ".sql", w)
        f.write(self.qh.create_table(tablename))
        f.close()


    def create_schema(self, schema, schemaname, logging_structure=None, migration_files=False, execute_later=False):
        cursor = self.conn.cursor()
        cursor.execute(self.qh.create_schema(schemaname))
        print (f"Schema {schemaname} created")

        log = None
        if logging_structure:
            log = Logging(self.qh, "Logging", "logging", logging_structure, cursor, "change_trigger()")

        for k, v in schema.items():
            query = self.qh.create_table(schemaname, v)
            if query:
                cursor.execute(query)
                print (f"{k} table created")
                if log:
                    log(schemaname, k, cursor)

        for k, v in schema.items():
            query = self.qh.insert_foreign_key(schemaname, v)
            if query:
                cursor.execute(query)
                print (f"Foreign keys for {schemaname}.{k} inserted")
