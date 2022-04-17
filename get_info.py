from get_tables import get_tables
from get_columns import get_columns

def get_info(database):
    '''
    Get the info as a list of table lists,
    each table list is a list where the first element is the table name,
    the second element is the list of all the columns of that table,
    the third element is the list of records,
    each record is a list of values.
    i.e. [[table name, [column 1, column 2, ...],
    [[record 1 value 1, record 1 value 2, ...], [record 2 value 1, record 2 value 2, ...], ...]], ...]
    '''
    # initialize
    info = []
    # get the tables
    tables = get_tables(database)
    # get the info for each table
    for table in tables:
        # get the columns
        columns = get_columns(database, table)
        # get the records by using select *
        import sqlite3
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ' + table)
        records = cursor.fetchall()

        # if a value is null, we replace it with spaces instead.
        records = [[' ' if x is None else x for x in record] for record in records]

        # add the info to the list
        info.append([table, columns, records])
    return info

