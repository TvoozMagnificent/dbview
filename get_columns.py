def get_columns(database, table_name):
    """
    Get columns from a table
    """
    # Get the columns from the table
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql = "SELECT * FROM " + table_name + " LIMIT 1"
    c.execute(sql)
    columns = [column[0] for column in c.description]
    # if column is a primary key, add "PRIMARY KEY" after it
    # similarly, if column is a foreign key, add "FOREIGN KEY" after it
    # if column is a unique key, add "UNIQUE KEY" after it
    # if column is a check constraint, add "CHECK" after it
    # if column is a not null constraint, add "NOT NULL" after it
    # if column is a default value, add "DEFAULT" after it
    # i.e. A column named ABC with PRIMARY KEY and NOT NULL will have "name"
    # as "ABC PRIMARY KEY NOT NULL"

    # Get the constraints from the table
    sql = "PRAGMA table_info(" + table_name + ")"
    c.execute(sql)
    constraints = c.fetchall()
    # if constraint is a primary key, add "PRIMARY KEY" after it
    # if constraint is a check constraint, add "CHECK" after it
    # if constraint is a not null constraint, add "NOT NULL" after it
    # if constraint is a default value, add "DEFAULT" after it
    # i.e. A column named ABC with PRIMARY KEY and NOT NULL will have "name"
    # as "ABC PRIMARY KEY NOT NULL"
    for column_index in range(len(columns)):
        if constraints[column_index][4] == 1:
            columns[column_index] = columns[column_index] + " PRIMARY KEY"
        if constraints[column_index][2] == 1:
            columns[column_index] = columns[column_index] + " NOT NULL"
        if constraints[column_index][4] != "" and constraints[column_index][4] != None:
            columns[column_index] = columns[column_index] + " DEFAULT " + constraints[column_index][4]

    c.close()

    return columns
