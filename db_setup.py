from stage import QueryHandler
from stage import StageDBConnection
import psycopg2

class DBSetup:
    def __init__(self, schema, logging=None):
        self.qh = QueryHandler()
        stagedb =  StageDBConnection()
        try:
            self.conn = stagedb.connect(db_name = "fdadb", user = "postgres", password = "postgres", host="localhost")
            self.conn.autocommit = True

            funcName = "create_schema"
            getattr(self, funcName)(schema, logging)
        except Exception as e:
            print (e)
        finally:
            if self.conn:
                self.conn.close()

    def create_table_migration_files(self, tablename):
        f = open(tablename + ".sql", w)
        f.write(self.qh.create_table(tablename))
        f.close()


    def create_schema(self, schema, logging=None):

        schemaname = "Staging"
        cursor = self.conn.cursor()
        query = self.qh.create_schema(schemaname)
        cursor.execute(query)
        print (f"Schema {schemaname} created")

        if logging:
            query = self.qh.create_schema("logging")
            cursor.execute(query)
            print ("Logging schema created")
            query = self.qh.create_table("logging", logging)
            cursor.execute(query)
            print ("Logging table created")

        for k, v in schema.items():
            query = self.qh.create_table(schemaname, v)
            if query:
                cursor.execute(query)
                print (f"{k} table created")

                if logging:
                    #sql_file = open('sql/change_trigger.sql','r')
                    #cursor.execute(sql_file.read())
                    #sql_file.close()
                    query = self.qh.create_trigger(schemaname, v["table_name"], "change_trigger()")
                    cursor.execute(query)
                    print (f"Change trigger created for {schemaname}.{k}")

        for k, v in schema.items():
            query = self.qh.insert_foreign_key(schemaname, v)
            if query:
                cursor.execute(query)
                print (f"Foreign keys for {schemaname}.{k} inserted")
