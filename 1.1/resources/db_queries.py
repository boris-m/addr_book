class DbQueries(object):
    def __init__(self):
        self.init_db = 'CREATE TABLE records (id INTEGER PRIMARY KEY, firstName VARCHAR(100), lastName VARCHAR(100) ,\
        birthday VARCHAR(10), phone INTEGER, correct_phone INTEGER )'

        self.get_bdays = "select firstName, birthday, julianday(strftime('%Y', 'now')||strftime('-%m-%d', birthday))-julianday('now')\
         as bd  from records where bd between -1 and 3" #-1 - to get todays birthdays

    def add_record(self ,record):
        query='INSERT INTO records (id, firstName, lastName ,birthday ,phone, correct_phone) \
        VALUES(NULL, "{fn}", "{ln}" , "{bd}", "{phone}" , "{cor_phone}")'.format(\
            fn = record.first_name, ln = record.last_name , bd = record.birthday ,\
            phone = record.phone_number, cor_phone = record.legal_phone_number )
        return query

    def update_record(self ,record):
        query = 'UPDATE records' \
              ' SET id = "{uid}", firstName = "{fn}" , lastName = "{ln}" ,birthday = "{bd}"  ,' \
              'phone = "{phone}" , correct_phone = "{cor_phone}"' \
              ' WHERE id={uid};'.format( uid = id , fn = record.first_name, ln = record.last_name ,\
               bd = record.birthday ,phone = record.phone_number, cor_phone = record.legal_phone_number )
        return  record