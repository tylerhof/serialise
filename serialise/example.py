import contextlib
import sqlite3
from datetime import datetime

from serialise.file import SaveDictsAsCsv, OpenFile
from serialise.sqlite import FetchAll, Execute, Upsert

my_dicts = [{'loss': 0.411, 'accuracy': 0.996,
             'val_loss':  0.147, 'val_accuracy': 0.99},
            {'loss': 0.115, 'accuracy': 0.997,
             'val_loss': 0.100, 'val_accuracy': 0.99}]
write = OpenFile('../data/test.csv', lambda file: SaveDictsAsCsv(file))
write(my_dicts)

connection_name = '../data/test.db'

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

execute = Execute(connection_name)
execute('DROP TABLE projects')
execute(sql_create_projects_table)

add_project = """ INSERT into projects (name,begin_date,end_date)
              VALUES(?,?,?)"""
project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')

upsert = Upsert(connection_name)
upsert(add_project, value=project)

fetch = FetchAll(connection_name)
result = fetch("SELECT * FROM projects")
print(result.value)

update_sql = """UPDATE projects
              SET end_date = ?
              WHERE name = ?"""

now = datetime.utcnow()
year_month_day_format = '%Y-%m-%d'
update_info = (now.strftime(year_month_day_format), "Cool App with SQLite & Python")

upsert(update_sql, value=update_info)
result = fetch("SELECT * FROM projects")
print(result.value)