import pyodbc

cnxn_str = ("Driver={SQL Server};"
            "Server=EDW;"
            "Database=CI_ERP;"
            "Trusted_Connection=yes;")
cnxn = pyodbc.connect(cnxn_str)

#paste query into 

sql = """
SELECT
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
	columns.column_id
"""

#read SQL query and print to terminal

cursor = cnxn.cursor()	
cursor.execute(sql) 
row = cursor.fetchone() 
while row:
    print (row) 
    row = cursor.fetchone()
