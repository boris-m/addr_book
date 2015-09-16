class DbQueries(object):
    def __init__(self):
        self.init_db='CREATE TABLE records (id INTEGER PRIMARY KEY, firstName VARCHAR(100), lastName VARCHAR(100) ,\
        birthday VARCHAR(10), phone INTEGER, correct_phone INTEGER )'
