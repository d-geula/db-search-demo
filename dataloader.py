import sqlite3
import pandas as pd

class DataLoader:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = sqlite3.connect(self.db_url)

    def load_data(self, table_name):
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
        return df
    
    def filter_table(self, sql_query):
        df = pd.read_sql_query(sql_query, self.conn)
        return df

    def get_schema(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info([{table_name}])")
        schema = cursor.fetchall()
        return schema
    
    def get_sample_data(self, table_name, limit=3):
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", self.conn)
        return df


# dl = DataLoader("Formula1.sqlite")
# print(dl.get_create_statement("drivers"))
# print(dl.get_sample_data("drivers"))