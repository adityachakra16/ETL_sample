import os
import csv
import json

class Extract:
    def __init__(self):
        self.data_sources = json.load(open('config.json'))
        self.csv_path = self.data_sources['data_sources']['csv']
        self.fda_path = self.data_sources['data_sources']['fda']


    def getCSVData(self, csv_name):
        if not os.path.exists(self.csv_path[csv_name]):
            raise Exception(f"{self.csv_path[csv_name]} does not exist")

        data = []
        columns = []
        reader = csv.DictReader(open(self.csv_path[csv_name], mode='r', encoding='utf-8-sig'))
        columns = reader.fieldnames
        data = [tuple([row[col] for col in columns]) for row in reader]
        return columns, data

    def getFDAData(self, filename):
        if not os.path.exists(self.fda_path[filename]):
            raise Exception(f"{self.fda_path[filename]} does not exist")

        data = []
        columns = []
        with open(self.fda_path[filename]) as f:
            firstline = True
            for line in f:
                if firstline:
                    columns = line.strip('\n').split('$')
                    firstline = False
                else:
                    data.append(tuple(line.strip('\n').split('$')))

        return columns, data
