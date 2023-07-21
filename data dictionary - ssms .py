import polars as pl
import pandas as pd
import os
import time
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import sqlalchemy as sa

start_time = time.time()

connection_string = "Driver={SQL Server};Server=EDW;Database=CI_ERP;Trusted_Connection=yes;"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

engine = create_engine(connection_url)

with engine.begin() as conn:
    dd = pd.read_sql_query(sa.text('''SELECT
	CONCAT(schemas.name,'||',tables.name,'||',columns.name) as FieldLineage,
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

os.makedirs(r'path',exist_ok=True)

dd.to_csv(r'path\file.csv')

dd = pl.read_csv('path\file.csv')

# instantiate columns for use later on
dd = dd.with_columns((pl.lit(None)).alias("EDWPrimaryKey"))
dd = dd.with_columns((pl.lit(None)).alias("ForeignKey"))

# generate edw primary keys based on the column id
dd = dd.with_columns(pl.when(pl.col("column_id") == 1).then("Y").otherwise(pl.col("EDWPrimaryKey")).alias("EDWPrimaryKey"))

# count the number of times a ColumnName is duplicated within the same column
counts = dd.filter(pl.col("ColumnName").apply(lambda x: any(substring.lower() in x.lower() for substring in ['id','Id','ID']))) \
				.filter(pl.col("ColumnName").apply(lambda x: all(substring.lower() not in x.lower() for substring in ["modified", "insert", "hashid","historyperiod","changetype","sceneriofy"]))) \
                .groupby("ColumnName").agg(pl.col("ColumnName").count().alias("TotalRelationships")) \
                .filter(pl.col("TotalRelationships") != 1) # filter out where a field relates with itself
dd = dd.join(counts, on="ColumnName", how="left")

# take every TABLE_NAME where ColumnName is duplicated and create a list of those TableName's to a new cell
relationships = dd.filter(pl.col("ColumnName").apply(lambda x: any(substring.lower() in x.lower() for substring in ['id','Id','ID']))) \
				.filter(pl.col("ColumnName").apply(lambda x: all(substring.lower() not in x.lower() for substring in ["modified", "insert", "hashid","historyperiod","changetype","sceneriofy"]))) \
                .groupby("ColumnName") \
                .agg(pl.col("TableName").apply(lambda col: col.to_list()).alias("RelationshipList"))
dd = dd.join(relationships, on="ColumnName", how="left")

# convert the list of table names into a single string
dd = dd.with_columns(pl.col("RelationshipList").alias("RELATIONSHIPS"))
dd = dd.with_columns("RelationshipList", dd["RELATIONSHIPS"].apply(lambda lst: ", ".join(lst)))
dd = dd.drop("RelationshipList")

# create a second Relationships column that returns null where there are no relationships
dd = dd.with_columns(pl.when(pl.col("TotalRelationships").is_null()).then(pl.lit(None)).otherwise(pl.col("RELATIONSHIPS")).alias("Relationships"))

# generate FOREIGN_KEYS based on cells in RELATIONSHIPS that have data
expression = pl.when(pl.col("Relationships").is_not_null()).then("Y").otherwise(pl.col("ForeignKey"))
dd = dd.with_columns("ForeignKey", expression)
dd = dd.drop("ForeignKey")
dd = dd.rename({"literal":"Foreign_Key"})

# create Definition column with automated entries for EDW created fields
dd = dd.with_columns((pl.lit(None)).alias("Definition"))

dd = dd.with_columns(
    pl.when(pl.col("ColumnName").str.contains("EdwInsertDate")).then("Date this record was inserted to table")
    .when(pl.col("ColumnName").str.contains("EdwModified")).then("EDW latest date this record was modified")
    .when(pl.col("ColumnName").str.contains("EdwHistoryPeriod")).then("EDW determined History Period")
    .when(pl.col("ColumnName").str.contains("EdwHashID")).then("EDW Unique hash ID")
    .when(pl.col("ColumnName").str.contains("EdwChangeType")).then("Boolean value to determine if data type has changed")
    .when(pl.col("ColumnName").str.contains("EdwScenarioFY")).then("Used to determine the source year for budget/forecast data from EPM")
    .otherwise(pl.col("Definition")).alias("Definition")
)

# create null columns to be populated manually
dd = dd.with_columns((pl.lit(None)).alias("VerifiedDefinition"))
dd = dd.with_columns((pl.lit(None)).alias("BPOwner"))

# remove original RELAITONSHIPS column 
dd = dd.drop("RELATIONSHIPS")

# reorder dataframe
dd = dd.select(['FieldLineage','SchemaName','TableName','ColumnName','DataTypeName','column_id','max_length','precision','scale','is_nullable','EDWPrimaryKey','Foreign_Key','TotalRelationships','Relationships','Definition','VerifiedDefinition','BPOwner'])

print(dd)

dd.write_csv('path\\datadictionary.csv')

print("Program took:", time.time() - start_time, "seconds to execute.")