from abstract_database import *
from abstract_security import *
from .responseContentParser import get_last_created_response_file_path,get_any_data
import psycopg2
import os
import pandas as pd

class DatabaseManager:
    def __init__(self, env_path):
        # Load environment configuration
        self.env_path = env_path
        self.dbname = get_env_value(key="abstract_ai_dbname", path=env_path)
        self.user = get_env_value(key="abstract_ai_user", path=env_path)
        self.password = get_env_value(key="abstract_ai_password", path=env_path)
        self.host = get_env_value(key="abstract_ai_host", path=env_path)
        self.port = int(get_env_value(key="abstract_ai_port", path=env_path))
        self.table_config_path = get_env_value(key="abstract_ai_table_configuration_file_path", path=env_path)
        
    def connect_db(self):
        """Establish a connection to the database."""
        try:
            return psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except psycopg2.OperationalError as e:
            print(f"Unable to connect to the database: {e}")
            sys.exit(1)

    def get_table_configuration(self, file_path=None):
        """Retrieve table configuration from a file."""
        table_configuration_file_path = file_path or self.table_config_path
        try:
            return safe_read_from_json(table_configuration_file_path)
        except Exception as e:
            print(f"No table config file path found: {e}")
            return []

    def get_dict_from_config(self, tableName, file_path=None):
        """Retrieve a table configuration by table name."""
        for config in self.get_table_configuration(file_path=file_path):
            if config.get('tableName').lower() == tableName.lower():
                return config

    def get_table_names(self, file_path=None):
        """Retrieve all table names from the configuration file."""
        return [config.get('tableName') for config in self.get_table_configuration(file_path=file_path)]

    def get_first_row_as_dict(self, tableName=None):
        """Fetch the first row of data from the specified table and return as a dictionary."""
        tableName = tableName or get_env_value(key="abstract_ai_table_name", path=self.env_path)
        query = f"SELECT * FROM {tableName} ORDER BY id ASC LIMIT 1;"

        conn = self.connect_db()
        cur = conn.cursor()
        try:
            cur.execute(query)
            first_row = cur.fetchone()
            col_names = [desc[0] for desc in cur.description]

            if first_row:
                return dict(zip(col_names, first_row))
            return None
        except psycopg2.Error as e:
            print(f"Error fetching the first row: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    def get_instruction_from_tableName(self, tableName=None):
        """Get instructions based on table configuration and data."""
        tableName = tableName or get_env_value(key="abstract_ai_table_name", path=self.env_path)
        table_samples = []
        table_samples.append({"DATABASE_CONFIG": self.get_dict_from_config(tableName), "explanation": "Database Table Configuration."})

        data = self.get_first_row_as_dict(tableName)
        if data:
            table_samples.append({"ACTUAL_DATABASE_ROW": data, "explanation": f"First row of data from table {tableName} returned as a dictionary."})

            value_keys = {column: get_value_keys(value) for column, value in data.items()}
            table_samples.append({"VALUE_KEYS": value_keys, "explanation": "Type Values for the Values in the Database SCHEMA."})

            table_samples.append({"AVAILABLE_FUNCTION_FOR_FILTERING": self.get_filtering_function(), "explanation": "Available function for filtering the database."})

        return table_samples

    def get_filtering_function(self):
        """Return a string representing the available function for filtering the database."""
        return """def search_multiple_fields(query):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(query)
        results = cur.fetchall()
        return results
    except psycopg2.Error as e:
        print(f"Error querying JSONB data: {e}")
    finally:
        cur.close()
        conn.close()
"""

    def search_multiple_fields(self, query,**kwargs):
        """Search the database using a query."""
        conn = self.connect_db()
        cur = conn.cursor()
        try:
            cur.execute(query)
            return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Error querying JSONB data: {e}")
        finally:
            cur.close()
            conn.close()

    def save_to_excel(self, rows, file_path="output.xlsx"):
        """Save query results to an Excel file."""
        excel_data = []
        if rows:
            for row in rows:
                row = list(row) if isinstance(row, tuple) else row
                excel_data.append(flatten_json(row, parent_key='', sep='_'))
            df = pd.DataFrame(excel_data)
            safe_excel_save(df, file_path)

    def get_query_save_to_excel(self, database_query, file_path="output.xlsx"):
        """Fetch query results and save them to an Excel file."""
        result = self.search_multiple_fields(**database_query)
        self.save_to_excel(result, file_path=file_path)
        return file_path

    def generate_query_from_recent_response(self, file_path):
        """Generate a query based on the most recent response and save the result to an Excel file."""
        response_content = get_response_content(file_path)
        database_query = response_content.get('database_query')
        if database_query:
            title = response_content.get('generate_title')
            new_directory = os.path.join(os.path.dirname(file_path), 'queries')
            os.makedirs(new_directory, exist_ok=True)

            new_file_path = os.path.join(new_directory, f"{title}.xlsx")
            self.get_query_save_to_excel(database_query, file_path=new_file_path)
            return new_file_path

    def get_db_query(self):
        """Get the latest database query and save the result."""
        file_path = get_latest_response()
        return self.generate_query_from_recent_response(file_path)
def ensure_db_manager(db_mgr=None,env_path=None):
    return db_mgr or DatabaseManager(env_path = env_path)
def generate_query_from_recent_response(file_path=None,db_mgr=None,env_path =None):
        """Generate a query based on the most recent response and save the result to an Excel file."""
        db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path)
        database_query = get_any_data(file_path=file_path,key_value='database_query')
        if database_query:
            response_content = get_response_content(file_path=file_path)
            title = response_content.get('generate_title')
            new_directory = os.path.join(os.path.dirname(file_path), 'queries')
            os.makedirs(new_directory, exist_ok=True)
            new_file_path = os.path.join(new_directory, f"{title}.xlsx")
            db_mgr.get_query_save_to_excel(database_query, file_path=new_file_path)
            return new_file_path
def get_db_query(db_mgr=None,env_path = None,file_path=None):
    """Get the latest database query and save the result."""
    db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path)
    file_path = file_path or get_last_created_response_file_path()
    return generate_query_from_recent_response(file_path=file_path,db_mgr=db_mgr,env_path=env_path)
def get_instruction_from_tableName(tableName=None,db_mgr=None,env_path = None,file_path=None):
    """Get the latest database query and save the result."""
    db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path)
    return db_mgr.get_instruction_from_tableName(tableName=tableName)
def search_multiple_fields(self, query,tableName=None,db_mgr=None,env_path = None,file_path=None,**kwargs):
    db_mgr = ensure_db_manager(db_mgr=db_mgr,env_path=env_path)
    return db_mgr.search_multiple_fields(query)
