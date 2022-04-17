def db2txt(db_file, txt_file):
    '''Read a database file and write pretty text to a text file by importing organize.'''
    import organize
    with open(txt_file, 'w') as txt:
        txt.write(organize.organize(db_file))

