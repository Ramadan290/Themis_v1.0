"""

This file establishes connection with database to get url which will be used to create a db session

"""

import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

Base = declarative_base()

connection_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ABDALLAH\\SQLEXPRESS;"
    "DATABASE=THEMIS;"
    "UID=db_themis_admin;"
    "PWD=RoqZak226@;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=5;"
)


DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_str)}"