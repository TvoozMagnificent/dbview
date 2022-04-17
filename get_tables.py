def get_tables(database):
    '''Get the name of all tables in the database'''
    # database is a string.
    # Returns a list of strings.
    # Each string is the name of a table in the database.

    # Get the list of tables in the database
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    conn.close()
    return [table[0] for table in tables]


