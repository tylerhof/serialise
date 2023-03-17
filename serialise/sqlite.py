import contextlib
import sqlite3
from functools import partial

from exceptionhandling.exception_handler import ExceptionHandler, Safe
from exceptionhandling.functor import Functor

def execute_sql(connection_name, sql_lambda):
    with contextlib.closing(sqlite3.connect(connection_name)) as open_connection:
        open_connection.row_factory = sqlite3.Row
        with contextlib.closing(open_connection.cursor()) as cursor:
            return sql_lambda(open_connection, cursor)

class Execute(Functor):

    def __init__(self, connection_name, policy: ExceptionHandler = Safe()):
        super().__init__(policy)
        self.connection_name = connection_name

    def apply(self, input, **kwargs):
        return execute_sql(self.connection_name, partial(self.execute, input, **kwargs))

    def execute(self, input, connection, cursor, **kwargs):
        if 'value' in kwargs:
            cursor.execute(input, kwargs.get("value"))
            return cursor
        else:
            cursor.execute(input)
            return cursor

class FetchAll(Functor):

    def __init__(self, connection_name, policy: ExceptionHandler = Safe()):
        super().__init__(policy)
        self.connection_name = connection_name

    def apply(self, input, **kwargs):
        return execute_sql(self.connection_name, partial(self.execute, input, **kwargs))

    def execute(self, input, connection, cursor, **kwargs):
        if 'value' in kwargs:
            cursor.execute(input, kwargs.get("value"))
            return cursor.fetchall()
        else:
            cursor.execute(input)
            return cursor.fetchall()

class Upsert(Functor):

    def __init__(self, connection_name, policy: ExceptionHandler = Safe()):
        super().__init__(policy)
        self.connection_name = connection_name

    def apply(self, input, **kwargs):
        return execute_sql(self.connection_name, partial(self.execute, input, **kwargs))

    def execute(self, input, connection, cursor, **kwargs):
        if 'value' in kwargs:
            cursor.execute(input, kwargs.get("value"))
            connection.commit()
            return cursor
        else:
            cursor.execute(input)
            connection.commit()
            return cursor