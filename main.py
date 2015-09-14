import os
import sqlite3
import datetime
import time
from messages import Messages


class Settings(object):
    def __init__(self):
        self.storage_file="storage.db"

class Record(object):
    def __init__(self):
        self.id=None
        self.first_name=None
        self.last_name=None
        self.birthday=None
        self.phone_number=None
        self.legal_phone_number=0 #sqllite have no BOOL so 0 is False

    def print_record(self):
        msg="""
        id         "{uid}"
        first name "{fn}"
        last name  "{ln}"
        birthday   "{bd}"
        phone      "{ph}" """.format(
            uid = self.id,
            fn  = self.first_name,
            ln  = self.last_name,
            bd  = self.birthday,
            ph  = self.phone_number
        )
        print msg
        return msg

    def fill_record(self,data):
        try:
            self.id=data[0]
            self.first_name=data[1]
            self.last_name=data[2]
            self.birthday=data[3]
            self.phone_number=data[4]
            self.legal_phone_number=data[5]
        except Exception,e:
            print "can not parse record:{err}".format(err=e)

class Application(Settings):
    def __init__(self):
        super(Application,self).__init__()
        self.stop_flag = True
        self.db_conection = self.__init_db()

    def __del__(self):
        self.db_conection.close()

    def __init_db(self):
        if not os.path.isfile(self.storage_file):
            con = sqlite3.connect(self.storage_file)
            cur = con.cursor()
            create_table_query='CREATE TABLE records (id INTEGER PRIMARY KEY, firstName VARCHAR(100), lastName VARCHAR(100) , birthday VARCHAR(10), phone INTEGER, correct_phone INTEGER )'
            cur.execute(create_table_query)
            con.commit()
            return con
        return sqlite3.connect(self.storage_file)

    def __check_birthdays(self):
        today=str(datetime.date.today())
        future_date=str(datetime.date.today()+datetime.timedelta(days=3))
        cur=self.db_conection.cursor()
        query='SELECT * FROM records WHERE birthday BETWEEN "{td}" AND "{fd}"'.format(td = today, fd = future_date)
        cur.execute(query)
        print cur.fetchall()

    def __print_record(self,record):
        msg="""
        id         "{uid}"
        first name "{fn}"
        last name  "{ln}"
        birthday   "{bd}"
        phone      "{ph}"
        """.format(
            uid = record.id,
            fn  = record.first_name,
            ln  = record.last_name,
            bd  = record.birthday,
            ph  = record.phone_number
        )

    def __db_add_record(self,record):
        query='INSERT INTO records (id, firstName, lastName ,birthday ,phone, correct_phone) \
        VALUES(NULL, "{fn}", "{ln}" , "{bd}", "{phone}" , "{cor_phone}")'.format(\
            fn = record.first_name, ln = record.last_name , bd = record.birthday ,\
            phone = record.phone_number, cor_phone = record.legal_phone_number )

        cur=self.db_conection.cursor()
        cur.execute(query)
        self.db_conection.commit()

    def add_record(self):
        print Messages.add_record
        user_input = raw_input("input record parameters, please: ")
        #TODO remove all non alfnum symbols, check encoding

        user_input = user_input.strip("     \t\n\r")
        user_input = user_input.split(',')

        if len(user_input) < 4:
            print "you input wrong data, please try again "
            return None
        raw_firstname = [user_input[0]]
        raw_lastname  = [user_input[1]]
        raw_birthday  = [user_input[2]]
        raw_phone     = [user_input[3]]
        #check input is correct
        print(raw_birthday)

    def __db_find_record(self,query):
        db_query='SELECT * from records where firstName like "%{q}%"'.format(q = query)
        cur=self.db_conection.cursor()
        cur.execute(db_query)
        res=cur.fetchall()
        print "we found {n} records:".format(n=len(res))
        for i in res:
            rec=Record()
            rec.fill_record(i)
            rec.print_record()

    def _db_find_record_by_id(self,id):
        db_query='SELECT * from records where id = "{q}"'.format(q = id)
        cur=self.db_conection.cursor()
        cur.execute(db_query)
        res=cur.fetchall()[0]
        record=Record()
        record.fill_record(res)
        record.print_record()

    def find_record(self):
        print Messages.find_record
        user_input = raw_input("input record parameters, please: ")
        #TODO remove all non alfnum symbols, check encoding

        user_input = user_input.strip("     \t\n\r")
        self.__db_find_record(user_input)

    def set_record(self,id,record):
        query='UPDATE records' \
              ' SET id = "{uid}", firstName = "{fn}" , lastName = "{ln}" ,birthday = "{bd}"  ,' \
              'phone = "{phone}" , correct_phone = "{cor_phone}"' \
              ' WHERE id={uid};'.format( uid = id , fn = record.first_name, ln = record.last_name ,\
               bd = record.birthday ,phone = record.phone_number, cor_phone = record.legal_phone_number )
        cur=self.db_conection.cursor()
        cur.execute(query)
        self.db_conection.commit()

    def __db_remove_record(self,id):
        id=int(id)
        query='DELETE  FROM records where id={uid}'.format(uid=id)
        cur=self.db_conection.cursor()
        cur.execute(query)
        self.db_conection.commit()

    def remove_record(self):
        print Messages.remove_record_first
        self.find_record()
        user_input = raw_input("please input id of record should be deleted")
        id=self._db_find_record_by_id(int(user_input))

    def select_all(self):
        db_query='SELECT * from records'
        cur=self.db_conection.cursor()
        cur.execute(db_query)
        res=cur.fetchall()
        for i in res:
            rec=Record()
            rec.fill_record(i)
            rec.print_record()

    def execute_task(self,command):

        if command=="add" or command == "a":
            self.add_record()
        elif command == "remove" or command == "r":
            self.remove_record()
        elif command == "change" or command == "c":
            self.set_record()
        elif command == "find" or command == "f":
            self.find_record()
        elif command == "show_all" or command == "s":
            self.select_all()
        else:
            print "no such command ({cmd})\r\n{man}".format(cmd=command, man=Messages.intro)

    def loop(self):
        user_input = raw_input("input command please: ")
        self.execute_task(user_input)
        time.sleep(1)

    def run(self):
        try:
            print Messages.intro
            while self.stop_flag:
                self.loop()
        except Exception,e:
            print "error in program: {exc}".format(exc = e)
        finally:
            try:
                print "destroing DB connection"
                self.db_conection.close()
            except Exception,e:
                print "probably connection already closed"

    def test(self):
        self.__check_birthdays()

def test():
    A=Application()
    con= A.db_conection
    cur=con.cursor()
    rec=Record()
    rec.last_name="testlastname"
    rec.first_name="testFirstname"
    rec.birthday="2003-09-14"
    rec.phone_number="12341243"
    rec.legal_phone_number=0
    #A.find_record("test")
    A.run()
    #A._db_find_record_by_id(5)
    A.select_all()
    A.db_conection.close()

if __name__ == "__main__":
    test()