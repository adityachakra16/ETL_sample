from extract import Extract
from transform import Transformation

if __name__ == "__main__":
    #extractor = Extract()
    #print (extractor.getAPISData("Pollution"))
    #print (extractor.getCSVData("CryptoMarkets"))
    transformer = Transformation('api', 'Pollution')
