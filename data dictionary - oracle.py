import time
import polars as pl

start_time = time.time()

# SQL query for pull, execute this to graba a spreadsheet with all necessary data
# This only has to be done once as Oracle Tables are static
# Below is an example of the query I used

# SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, NULLABLE
# FROM ALL_TAB_COLUMNS
# WHERE (UPPER(TABLE_NAME) LIKE 'GL%'
#    OR UPPER(TABLE_NAME) LIKE 'AP%'
#    OR UPPER(TABLE_NAME) LIKE 'IBY%'
#    OR UPPER(TABLE_NAME) LIKE 'XLA%'
#    OR UPPER(TABLE_NAME) LIKE 'FND%'
#    OR UPPER(TABLE_NAME) LIKE 'EGP%'
#    OR UPPER(TABLE_NAME) LIKE 'POZ%'
#    OR UPPER(TABLE_NAME) LIKE 'HZ%'
#    OR UPPER(TABLE_NAME) LIKE 'FLA%'
#    OR UPPER(TABLE_NAME) LIKE 'FUN%'
#    OR UPPER(TABLE_NAME) LIKE 'CST%'
#    OR UPPER(TABLE_NAME) LIKE 'DOO%'
#    OR UPPER(TABLE_NAME) LIKE 'MSC%'
#    OR UPPER(TABLE_NAME) LIKE 'QP%'
#    OR UPPER(TABLE_NAME) LIKE 'RCV%'
#    OR UPPER(TABLE_NAME) LIKE 'WSH%'
#    OR UPPER(TABLE_NAME) LIKE 'RA%'
#    OR UPPER(TABLE_NAME) LIKE 'HR%'
#    OR UPPER(TABLE_NAME) LIKE 'WIS%'
#    OR UPPER(TABLE_NAME) LIKE 'INV%')
#    AND TABLE_NAME NOT LIKE '%\_' ESCAPE '\'

dd = pl.read_csv('path\\oracle_tables.csv')

# create empty column for ForeignKey
dd = dd.with_columns((pl.lit("N")).alias("FOREIGNKEY"))

# count the number of times a COLUMN_NAME is duplicated within the same column
counts = dd.filter(pl.col("COLUMN_NAME").apply(lambda x: any(substring.lower() in x.lower() for substring in ['id','Id','ID']))) \
                  .groupby("COLUMN_NAME").agg(pl.col("COLUMN_NAME").count().alias("TOTAL_RELATIONSHIPS"))
dd = dd.join(counts, on="COLUMN_NAME", how="left")

# take every TABLE_NAME where COLUMN_NAME is duplicated and create a lilst of those TABLE_NAME's to a new cell
relationships = dd.filter(pl.col("COLUMN_NAME").apply(lambda x: any(substring.lower() in x.lower() for substring in ['id','Id','ID']))) \
                  .groupby("COLUMN_NAME") \
                  .agg(pl.col("TABLE_NAME").apply(lambda col: col.to_list()).alias("RelationshipList"))
dd = dd.join(relationships, on="COLUMN_NAME", how="left")

# convert the list of table names into a single string
dd = dd.with_columns(pl.col("RelationshipList").alias("RELATIONSHIPS"))
dd = dd.with_columns("RelationshipList", dd["RELATIONSHIPS"].apply(lambda lst: " | ".join(lst)))
dd = dd.drop("RelationshipList")

# generate FOREIGN_KEYS based on cells in RELATIONSHIPS that have data
expression = pl.when(pl.col("RELATIONSHIPS").is_not_null()).then("Y").otherwise(pl.col("FOREIGNKEY"))
dd = dd.with_columns("FOREIGNKEY", expression)
dd = dd.drop("FOREIGNKEY")
dd = dd.rename({"literal":"FOREIGN_KEY"})

# reorder the dataframe
dd = dd.select(['TABLE_NAME','COLUMN_NAME','DATA_TYPE','DATA_LENGTH','NULLABLE','FOREIGN_KEY','TOTAL_RELATIONSHIPS','RELATIONSHIPS'])

print(dd)

dd.write_csv('path\\oracle_data_dictionary.csv')

print("Program took:", time.time() - start_time, "seconds to execute.")
