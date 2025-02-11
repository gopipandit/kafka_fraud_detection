from dotenv import load_dotenv, dotenv_values
import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()


class Connector:
    def __init__(self):
        self.__host = os.getenv('hostname')
        self.__database = os.getenv('db_name')
        self.__user = os.getenv('user_name')
        self.__password = os.getenv('password')
        self.__port = os.getenv('port')

        self.__connection_string = f'postgresql://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__database}'
        self.__engine = create_engine(self.__connection_string)

    def get_data_from_pg(self, schema_name, table_name):
        query = f"""SELECT * FROM {schema_name}.{table_name}"""
        try:
            dataset = pd.read_sql_query(query, self.__engine)
            return dataset
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        finally:
            self.__engine.dispose()

    def execute_query(self, query):
        with self.__engine.connect() as executor:
            try:
                executor.execute(text(query))
                executor.commit()
                print("Query Executed Successfully")
            except Exception as e:
                print(f"Error occurred: {e}")
            finally:
                self.__engine.dispose()

    def drop_table(self, schema_name, table_name):
        query = f"""DROP TABLE {schema_name}.{table_name}"""
        with self.__engine.connect() as executor:
            try:
                executor.execute(text(query))
                executor.commit()
                print(f"{table_name} dropped.")
            except Exception as e:
                print(f"Error occurred: {e}")
            finally:
                self.__engine.dispose()

    def get_all_tables(self,schema_name):
        query = f"""SELECT DISTINCT tablename from pg_tables where schemaname = '{schema_name}';"""
        with self.__engine.connect() as executor:
            try:
                result = list(executor.execute(text(query)))
                tables = [list(i)[0] for i in result]
                print(f"Below tables are available in the {schema_name} schema-\n\n{tables}")
            except Exception as e:
                print(f"Error occurred: {e}")
            finally:
                self.__engine.dispose()

    def excel_to_pg_table(self, excel_path, schema_name, sheet_name=None, table_name=None):
        # Load the Excel file
        xls = pd.ExcelFile(excel_path)

        # Use the first sheet if no sheet name is provided
        if sheet_name is None:
            sheet_name = xls.sheet_names[0]

        # Default table name to the sheet name if not provided
        if table_name is None:
            table_name = sheet_name.lower().replace(' ', '_')

        # Load data from the specified sheet
        xls_data = pd.read_excel(excel_path, sheet_name=sheet_name)

        # Clean column names
        xls_data.columns = xls_data.columns.str.lower().str.replace(' ', '_')

        try:
            # Write data to PostgreSQL
            with self.__engine.connect() as connection:
                xls_data.to_sql(table_name, connection, if_exists='replace', index=False, schema=schema_name)
                print(f"Data from {sheet_name} loaded into {schema_name}.{table_name}")
        except Exception as e:
            print(f"Could not load {sheet_name} due to: {e}")



