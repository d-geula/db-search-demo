import sqlite3
import pandas as pd

db = "Formula1.sqlite"

conn = sqlite3.connect(db)
cursor = conn.cursor()
table_name = 'stats'
cursor.execute(f"PRAGMA table_info([{table_name}])")
print(f"Table Name: {table_name}\nSchema:\n{cursor.fetchall()}\nSample Data:")
df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 3", conn)
print(df)


# CREATE VIEW stats AS SELECT surname,forename,raceId,positionOrder, points, laps FROM drivers JOIN results USING (driverId);

# -- SELECT surname, avg(positionOrder) as svg_positioj_order FROM drivers JOIN results USING (driverId) GROUP BY 1 order by 2
# SELECT surname,forename,raceId,positionOrder, points, laps FROM drivers JOIN results USING (driverId);

# SELECT forename, surname, COUNT(*) as wins
# FROM stats
# WHERE positionOrder = 1
# GROUP BY forename, surname
# ORDER BY wins DESC
# LIMIT 10;

# PRAGMA table_info([stats]);

# SELECT sql 
# FROM sqlite_schema 
# WHERE name in ('drivers', 'results');