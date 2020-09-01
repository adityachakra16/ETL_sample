from stage import StageDBConnection, QueryHandler
import pandas as pd
import numpy as np

class Transformation:
    def __init__(self, dataSet):
        stagedb = StageDBConnection()
        self.sqh = StageQueryHandler()
        self.conn = stagedb.connect(db_name = dataSet, user = "postgres", password = "postgres", host="localhost")
        self.cur = self.conn.cursor()
        data = getattr(self, 'retrieve_data')()
        data = getattr(self, 'clean_data')(data)


    def retrieve_distinct_crypto(self):
        self.cur.execute(self.sqh.distinct_crypto_names_symbol())
        return np.array(self.cur.fetchall(), dtype=np.dtype(np.ndarray('int, U100, U100, U100, U100, int, float, float, float, float, float, float, float, float')))

    def clean_crypto_name_symbol(self, data):
        #data[1:10, 1:5] = np.char.rstrip(data[1:10, 1:5])
        #cleaned_data.append(col_data)
        return data

    def retrieve_price_data(self):
        pass

    def calc_price_change(self):
        pass

    def round_price_data(self):
        pass
