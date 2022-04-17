def txt2py(txt_file, py_file, db_file):
    import sqlite3
    import re

    result=''
    # the result should be a python file that can result in a sqlite3 database representation of the txt file
    # add the copyright header
    result += '#!/usr/bin/env python3\n'
    result += '# Copyright: TvoozMagnificent\n'
    # import modules.
    result += 'import sqlite3\n'

    # Open the txt file
    with open(txt_file, 'r') as f:
        txt = f.read()
        # Remove whitespace except for newlines
        # DO NOT REMOVE NEWLINES
        # ONLY REMOVE SPACE AND TAB.
        txt = re.sub(r'[ \t]+', ' ', txt)


    # Split the txt file into a list of lines
    lines = txt.split('\n')

    # Remove empty lines
    lines = [line for line in lines if line]

    # get the number of tables
    # each table contains eactly three SPLIT lines, i.e.
    # +-------------+ ... +-------------+
    # count the number of lines that is the SPLIT line.
    SPLIT = ' +-'
    table_num = len([line for line in lines if line.startswith(SPLIT)])//3
    def get_nth_SPLIT(n):
        # return the index of the nth SPLIT line
        # i.e. the index of the line that is the nth SPLIT line
        # if n is 0, return the index of the first SPLIT line
        # if n is 1, return the index of the second SPLIT line
        # etc.
        # we are not sure how long each table is, so we need to loop through
        # all the lines until we find the nth SPLIT line.
        SPLIT = '+-'
        count = 0
        for i, line in enumerate(lines):
            if line.strip().startswith(SPLIT):
                count += 1
                if count == n:
                    return i
        # if we get here, we didn't find the nth SPLIT line
        raise ValueError('n is too large')
    # divide text into tables
    tables = [lines[get_nth_SPLIT(1+3*i)-1:get_nth_SPLIT(3+3*i)+1] for i in range(table_num)]


    # write the following:
    '''
    conn = sqlite3.connect(db_file)
    c = conn.cursor()'''
    result += 'conn = sqlite3.connect({})\n'.format(db_file)
    result += 'c = conn.cursor()\n'

    # create the tables
    for i, table in enumerate(tables):
        # get the table name
        table_name = table[0]
        # create the table with the given name and columns. We are not sure how many columns there are in a table.

        # get the column names
        col_names = table[2].split('|')

        # create the table
        # write the following:
        '''        c.execute(f'DROP TABLE IF EXISTS {table_name}')
        c.execute(f'CREATE TABLE {table_name} ({", ".join(col_names[1:-1])})')'''
        result += 'c.execute(f"DROP TABLE IF EXISTS {}")\n'.format(table_name)
        result += 'c.execute(f"CREATE TABLE {} ({})")\n'.format(table_name, ", ".join(col_names[1:-1]))


    # insert the data into the tables
    for i, table in enumerate(tables):
        # get the table name
        table_name = table[0]
        # get the column names
        col_names = table[2].split('|')
        # get the data
        data = table[4:-1]
        # insert the data into the table
        for row in data:
            # split the row into columns
            row = row.split('|')

            # if a value is blank, it is null, and we need to insert a NULL value
            # otherwise, we need to insert the value
            row = ["NULL" if col == '' else col for col in row]

            # insert the row into the table
            q='"' # quote

            # write the following:
            '''            c.execute(f'INSERT INTO {table_name} '
                      f'({", ".join([i.split(" ")[0] for i in col_names[1:-1]])}) '
                      f'VALUES ({", ".join([f"{q}{i}{q}" for i in row[1:-1]])})')'''
            result += 'c.execute(\'{}\')\n'.format(f'INSERT INTO {table_name} '
                      f'({", ".join([i.split(" ")[0] for i in col_names[1:-1]])}) '
                      f'VALUES ({", ".join([f"{q}{i}{q}" for i in row[1:-1]])})')




    # commit the changes
    result += 'conn.commit()\n'

    # close the connection
    result += 'conn.close()\n'

    # write result to file
    with open(py_file, 'w') as f:
        f.write(result)

    return result

txt2py('info1.txt', 'info1.py', 'info1.db')


