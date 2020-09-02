from extract import Extract
from transform import Transformation
from stage import Stage
from db_setup import DBSetup
import json

if __name__ == "__main__":
    schema = json.load(open('schema.json'))
    setup = DBSetup(schema["Schema"]["Staging"], schema["Schema"]["Logging"])
    #setup = DBSetup(tasks["Setup"], logging["t_history"])
    #Stage("fda", "Demographic")
