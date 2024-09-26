import mysql.connector

# MySQL connection details
MYSQL_DB_HOST = "demomysql.mysql.database.azure.com"
MYSQL_DB_PORT = 3306
MYSQL_DB_USER = "applicare_saas"
MYSQL_DB_PASSWORD = "Arctech01"

def connect_to_database():
    # Connect to MySQL
    connection = mysql.connector.connect(
        host=MYSQL_DB_HOST,
        port=MYSQL_DB_PORT,
        user=MYSQL_DB_USER,
        password=MYSQL_DB_PASSWORD
    )
    return connection

def list_databases(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print("Databases:")
    for db in databases:
        print(f"- {db[0]}")
    return databases

def list_tables(connection, database_name):
    cursor = connection.cursor()
    cursor.execute(f"USE {database_name}")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\nTables in database '{database_name}':")
    for table in tables:
        print(f"- {table[0]}")
    return tables

def list_columns(connection, database_name, table_name):
    cursor = connection.cursor()
    cursor.execute(f"USE {database_name}")
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    print(f"\nColumns in table '{table_name}':")
    for column in columns:
        print(f"- {column[0]} ({column[1]})")
    return columns

if __name__ == "__main__":
    # Connect to the database server
    connection = connect_to_database()
    
    # List all databases
    databases = list_databases(connection)
    
    # For each database, list tables and their columns
    for db in databases:
        db_name = db[0]
        tables = list_tables(connection, db_name)
        
        # For each table, list columns
        for table in tables:
            table_name = table[0]
            list_columns(connection, db_name, table_name)
    
    # Close the connection
    connection.close()