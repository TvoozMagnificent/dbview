from get_info import get_info

def organize(database,n="default"):
    '''Return a pretty string representation of the database using get_info

    The info is a list of table lists,
    each table list is a list where the first element is the table name,
    the second element is the list of all the columns of that table,
    the third element is the list of records,
    each record is a list of values.
    i.e. [[table name, [column 1, column 2, ...],
    [[record 1 value 1, record 1 value 2, ...], [record 2 value 1, record 2 value 2, ...], ...]], ..'''

    from functools import reduce

    info = get_info(database)

    def flat(l):
        '''Return a flattened version of l'''
        if isinstance(l,list):
            return reduce(lambda x,y:x+y, [flat(i) for i in l])
        else:
            return [l]

    if n == "default":
        n = max([len(str(i)) for i in flat(info)])

    string = '\n\n\n'
    for table in info:
        string += '\n' + table[0].center(len(table[1])*(5+n)+1) + '\n'*2
        string += f'   {("+---"+"-"*n)*len(table[1])+"+"}\n'
        for column in table[1]:
            string += '   |'+column.ljust(n)
        string += f'   |\n   {("+---"+"-"*n)*len(table[1])+"+"}\n'
        for record in table[2]:
            for value in record:
                string += '   |'+str(value).ljust(n)
            string += '   |\n'
        string += f'   {("+---"+"-"*n) * len(table[1]) + "+"}\n\n\n'
    return string
