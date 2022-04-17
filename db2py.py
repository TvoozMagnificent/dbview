def db2py(db_file, py_file, db_for_py):
    # read the database file by importing get_info from get_info.py
    import get_info
    # open the database file
    info = get_info.get_info(db_file)
    # generate the python file that can generate the database file
    result = "" # the result string
    if True:
        # write the header
        result+=('#!/usr/bin/env python3\n')
        # copyright: by TvoozMagnificent
        result+=('# Path: dbview/db2py.py\n')
        result+=('# Copyright: by TvoozMagnificent\n')
        # add the import statement and connect to the database
        result+=('import sqlite3\n')
        result+=('conn = sqlite3.connect("{}")\n'.format(db_for_py))
        # write the function that can generate the database file
        # delete the table if exists.
        # get table_name from the database file
        result+=('c = conn.cursor()\n')
        # info returns [[tablename1, [column1, ...], [[record1column1, ...], ...]], ...]
        # the first element is the list of table names
        for table in info:
            # for each table, write the function to create the table
            result+=('def create_table_{}():\n'.format(table[0]))
            # write the create table statement
            # first, drop the table if exists
            result+=('    c.execute("DROP TABLE IF EXISTS {}")\n'.format(table[0]))
            # then, create the table
            result+=('    c.execute("CREATE TABLE {} ('.format(table[0]))
            # write the column names
            for column in table[1]:
                result+=('{},'.format(column))
            # remove the last comma
            result=result[:-1]
            result+=(')")\n')
            # write the insert statement
            result+=('    c.execute("""INSERT INTO {} VALUES ('.format(table[0]))
            # write the values
            # note that if we see a value ' ', we need to write 'NULL'
            # remember, we are writing in a function, so we need to indent if we encounter a return.
            for record in table[2]:
                for value in record:
                    if value == ' ':
                        result+=('NULL,')
                    else:
                        result+=('"{}",'.format(value))
                # remove the last comma
                result=result[:-1]
                result+=('),(')
            # remove the last comma
            result=result[:-2]
            result+=('""")\n')
            # write the commit statement
            # remember, we are writing in a function, so we need to indent.
            result+=('    conn.commit()\n')
            # write the close statement
            result+=('    conn.close()\n')
            # end the function with return JIC
            result+=('    return\n')
            # pep8, so we add two newlines
            result+=('\n')
            result+=('\n')
        # call all the functions, creating a main function.
        result+=('def main():\n')
        # write the call to all the functions
        for table in info:
            result+=('    create_table_{}()\n'.format(table[0]))
        # end the main function
        result+=('    return\n')
        # pep8, so we add two newlines
        result+=('\n')
        result+=('\n')
        # call the main function
        result+=('main()\n')
        # add copyright again
        result+=('# Copyright: by TvoozMagnificent\n')
        # done.
    # write the result to the file
    with open(py_file, 'w') as f:
        f.write(result)
    # return the result
    return result




