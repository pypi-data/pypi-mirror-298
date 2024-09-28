# Database Connector Package

# Overview
**dbsconnector** is a Python package designed to simplify data integration from various sources, including CSV, Excel, Google Sheets, and MongoDB. The package provides a unified interface to connect, load, and process data with minimal setup, making it easier for Developers and Data Scientists to work across multiple data formats.

# Current Features:
- Connect to CSV files and load them into a Pandas DataFrame
- Handle Excel files with multiple sheets
- Fetch data from Google Sheets using an API key
- Interact with MongoDB collections

# Future Features (Upcoming):
- Support for more databases (SQL, NoSQL)
- Cloud storage integration (AWS S3, Google Cloud, etc.)
- API-based data sources

# Installation
To install the package, use pip:
```bash
pip install dbsconnector==1.4
```

# How to use this package?

## Connecting to csv
```py
# import the module:
from dbsconnector.databases import CSV

# load csv file:
df = CSV().load_csv(filepath="filedir/filename.csv", delimiter=",")

# convert dataframe to csv file:
CSV().to_csv(data=df, filepath="filepath.csv")
```


## Connecting to Excel
```py
# import the module:
from dbsconnector.databases import Excel

# load the data:
df = Excel().load_excelsheet(filepath='filedir/filename.xlsx', sheet_name='sheet_name')

# convert dataframe to excel sheet:
Excel().to_excel(data=df, filepath='filedir/filename.xlsx', sheet_name='sheet_name')
```


## Connecting to gsheet
```py
# import the module:
from dbsconnector.databases import GSheet

# load the data:
df = GSheet().load_gsheet(gsheet_id='17r9f4BL7sjmdLBnt92OdQP3CHK5bdT3hozg6DUJXGqU',sheet_name='sample_sheet')
```


## Connecting to MongoDB
```py
# import the module:
from dbsconnector.databases import MongoDB

# load data from mongodb:
df = MongoDB(host_url="mongodb://localhost:27017").load_data(database="database_name", collection_name="collection_name")

# upload data to mongodb:
MongoDB(host_url="mongodb://localhost:27017").upload_data(database="database_name", collection_name="collection_name", data=df)

# upload any kind of objects (preprocessor object or ML model object) to mongodb:
MongoDB(host_url="mongodb://localhost:27017").upload_object(database="database_name", collection_name="collection_name", object_name="preprocessor_object", object_=preprocessor)

# loading object from mongodb:
pre_obj = MongoDB(host_url="mongodb://localhost:27017").load_object(database="database_name", collection_name="collection_name", object_name="preprocessor_object")
```


# Contributions
* Contributions are welcome! Please open an issue or submit a pull request on GitHub for adding new features, fixing bugs, or improving documentation. Open-source collaboration is highly encouraged!

# License
This project is licensed under the MIT License.

# Contact
For any questions or suggestions, please contact [yuvaneshkm05@gmail.com](yuvaneshkm05@gmail.com)

# Connect
Connect with me on [LinkedIn](https://www.linkedin.com/in/yuvaneshkm)
