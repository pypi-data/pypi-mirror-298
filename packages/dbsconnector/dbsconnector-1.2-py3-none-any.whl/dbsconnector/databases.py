# importing necessary libraries
import pandas as pd
from pymongo import MongoClient
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")


# Connect to csv:
class CSV:
    def __init__(self):
        pass

    # load csv file:
    def load_csv(self, filepath: Path, delimiter: str) -> pd.DataFrame:
        filepath = Path(filepath)
        return pd.read_csv(filepath, delimiter=delimiter)

    # convert dataframe to csv file:
    def to_csv(self, data: pd.DataFrame, filepath: Path):
        filepath = Path(filepath)
        data.to_csv(filepath, index=False)


# Connect to Excel Sheet:
class Excel:
    def __init__(self):
        pass

    # load excel sheet:
    def load_excelsheet(self, filepath: Path, sheet_name: str) -> pd.DataFrame:
        filepath = Path(filepath)
        return pd.read_excel(filepath, sheet_name=sheet_name)

    # convert dataframe to excel sheet:
    def to_excel(self, data: pd.DataFrame, filepath: Path, sheet_name: str):
        filepath = Path(filepath)
        data.to_excel(filepath, sheet_name, index=False)


# Connect to Google Sheet:
class GSheet:
    def __init__(self):
        pass

    # load google sheet
    def load_gsheet(self, gsheet_id: str, sheet_name: str) -> pd.DataFrame:
        base_url = "https://docs.google.com/spreadsheets/d"
        sheet_csv = "gviz/tq?tqx=out:csv&sheet="
        url = f"{base_url}/{gsheet_id}/{sheet_csv}{sheet_name}"
        return pd.read_csv(url)


# Connect to MOngoDB:
class MongoDB:
    # initialize the mongo client:
    def __init__(self, host_url: str):
        self.mongoclinet: MongoClient = MongoClient(host_url)

    # load data from mongodb:
    def load_data(self, database: str, collection_name: str) -> pd.DataFrame:
        database_connect = self.mongoclinet[database]
        collection = database_connect[collection_name]
        records = collection.find()
        data = list(records)
        df = pd.DataFrame(data)
        df.drop("_id", axis=1, inplace=True)
        return df

    # upload data to mongodb:
    def upload_data(self, database: str, collection_name: str, data: pd.DataFrame):
        database_connect = self.mongoclinet[database]
        collection = database_connect[collection_name]
        data_dict = data.to_dict(orient="records")
        collection.insert_many(data_dict)

    # upload object to mongodb:
    def upload_object(
        self, database: str, collection_name: str, object_name: str, object_
    ):
        database_connect = self.mongoclinet[database]
        collection = database_connect[collection_name]
        record = {"object_name": object_name, "object": object_}
        collection.insert_one(record)

    # load object from mongodb:
    def load_object(self, database: str, collection_name: str, object_name: str):
        database_connect = self.mongoclinet[database]
        collection = database_connect[collection_name]
        object_ = collection.find_one({"obajct_name": object_name})
        return object_
