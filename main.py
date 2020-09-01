from extract import Extract
from transform import Transformation
from stage import Stage

if __name__ == "__main__":
    task = "stage"
    if task == "both":
        Stage("csv", "CryptoMarkets")
        Transformation()
    elif task == "stage":
        Stage("csv", "CryptoMarkets")
    elif task == "transform":
        Transformation("CryptoMarkets")
