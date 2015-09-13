import os
import sqlite3
import time
import datetime


class Settings(object):
    def __init__(self):
        self.storage_file="storage.db"

class Record(object):
    def __init__(self):
        self.first_name=None
        self.last_name=None
        self.birthday=None
        self.phone_number=None
        self.legal_phone_number=0 #sqllite have no BOOL so 0 is False

class Application(Settings):
    def __init__(self):
        super(Application,self).__init__()
        self.db_conection = self.__init_db()

    def __del__(self):
        self.db_conection.close()

    def __init_db(self):
        if not os.path.isfile(self.storage_file):
            con = sqlite3.connect(self.storage_file)
            cur = con.cursor()
            create_table_query='CREATE TABLE records (id INTEGER PRIMARY KEY, firstName VARCHAR(100), lastName VARCHAR(100) , birthday VARCHAR(10), phone INTEGER, correct_phone INTEGER )'
            cur.execute(create_table_query)
            insert_test_record_query='INSERT INTO records (id, firstName, lastName ,birthday ,phone, correct_phone) VALUES(NULL, "asdfasdf", "12123" , "{fd}", "79500305009" , "1")'.format(fd=str(datetime.date.today()+datetime.timedelta(days=2)))
            print insert_test_record_query
            cur.execute(insert_test_record_query)
            con.commit()
            return con
        return sqlite3.connect(self.storage_file)

    def __check_birthdays(self):
        today=str(datetime.date.today())
        print today
        future_date=str(datetime.date.today()+datetime.timedelta(days=3))
        print future_date
        cur=self.db_conection.cursor()
        query='SELECT * FROM records WHERE birthday BETWEEN "{td}" AND "{fd}"'.format(td = today, fd = future_date)
        print query
        cur.execute(query)
        print cur.fetchall()

    def add_record(self,record):
        query='INSERT INTO records (id, firstName, lastName ,birthday ,phone, correct_phone) \
        VALUES(NULL, "{fn}", "{ln}" , "{bd}", "{phone}" , "{cor_phone}")'.format(\
            fn = record.first_name, ln = record.last_name , bd = record.birthday ,\
            phone = record.phone_number, cor_phone = record.legal_phone_number )
        cur=self.db_conection.cursor()
        cur.execute(query)
        self.db_conection.commit()

        print query

    def test(self):
        self.__check_birthdays()


def test():
    A=Application()
    con= A.db_conection
    cur=con.cursor()
    rec=Record()
    rec.last_name="testlastname"
    rec.first_name="testFirstname"
    rec.birthday="2001-09-14"
    rec.phone_number="54326"
    rec.legal_phone_number=0
    A.add_record(rec)

    cur.execute("select * from records")
    print cur.fetchall()
    #A.test()
    A.db_conection.close()


if __name__ == "__main__":
    test()