import pandas as pd
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import sqlalchemy as sa

# database connection
connection_string = "Driver={SQL Server};Server=EDW;Database=CI_ERP;Trusted_Connection=yes;"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

engine = create_engine(connection_url)

# sql string execution
with engine.begin() as conn:
    df = pd.read_sql_query(sa.text('''SELECT
	schemas.name AS SchemaName,
	tables.name AS TableName,
	columns.name AS ColumnName,
	types.name AS DataTypeName,
	columns.column_id,
	columns.max_length,
	columns.precision,
	columns.scale,
	columns.is_nullable
	FROM sys.tables
	INNER JOIN sys.columns
	ON tables.object_id = columns.object_id
	INNER JOIN sys.types
	ON types.user_type_id = columns.user_type_id
	INNER JOIN sys.schemas
	ON schemas.schema_id = tables.schema_id
	ORDER BY schemas.name,
	tables.name,
	columns.column_id'''), conn)

# print functions
print(df)
print(df.info())
print(df.describe())
print(df['TableName'].unique()) # names of all unique tables
print(len(df['ColumnName'].unique())) # how many unique column names
