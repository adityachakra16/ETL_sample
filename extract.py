import os
import csv
import json

class Extract:
    def __init__(self):
        self.data_sources = json.load(open('config.json'))
        self.csv_path = self.data_sources['data_sources']['csv']


    def getCSVData(self, csv_name):
        if not os.path.exists(self.csv_path[csv_name]):
            raise Exception(f"{self.csv_path[csv_name]} does not exist")

        data = []
        columns = []
        reader = csv.DictReader(open(self.csv_path[csv_name], mode='r', encoding='utf-8-sig'))
        columns = reader.fieldnames
        data = [tuple([row[col] for col in columns]) for row in reader]
        return columns, data
