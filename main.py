import logging
import os
import sqlite3
import datetime
import time
from messages import Messages

class Settings(object):
    def __init__(self):
        self.storage_file="storage.db"

class Helper():
    def check_phone_number(self, num):


        return True
    def check_date_format(self, date):

        return True

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

    def fill_record_user_input(self , args):
        try:
            self.first_name=args[0]
            self.last_name=args[1]
            self.birthday=args[2]
            self.phone_number=args[3]
        except Exception,e:
            print "can not parse record:{err}".format(err=e)

    def fill_record_from_db(self,data):
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
        self.__helper=Helper()
        logging.basicConfig(level = logging.DEBUG)

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
        tmp_today=datetime.date.today()
        today="1000-{m}-{d}".format( m = tmp_today.month , d =tmp_today.day )
        future_date=str(datetime.date.today()+datetime.timedelta(days=3))
        cur=self.db_conection.cursor()
        query='SELECT * FROM records WHERE birthday BETWEEN "{td}" AND "{fd}"'.format(td = today, fd = future_date)
        cur.execute(query)
        res=cur.fetchall()
        if cur == []:
            print "no birthdays next 3 days "
            return None
        else:
            rec=Record()
            for i in res:
                rec.fill_record_from_db(i)
                try:
                    tmp=datetime.datetime.strptime(rec.birthday, "%Y-%m-%d").date()
                    diff=tmp.day - datetime.date.today().day
                    if diff>0:
                        bd="at {d} day of {m} month, {n} days left".format(d = tmp.day,m = tmp.month, n = diff)
                    if diff == 0:
                        bd="TODAY!"
                    print "{fn} {ln} have birthday  {date}".format(fn=rec.first_name , ln=rec.last_name , date=bd)
                except Exception as e:
                    logging.error("some error in __check_birthdays: {err}".format(err = e))
        return None

    def __is_record_duplicate(self,record):
        #TODO check another fields
        query='select id from records where firstName = "{fn}"'.format(fn = record.first_name)
        logging.debug(query)
        cur=self.db_conection.cursor()
        cur.execute(query)
        res=cur.fetchall()
        logging.debug(res)
        if res != []:
            return True
        return False

    def __db_add_record(self,record):
        query='INSERT INTO records (id, firstName, lastName ,birthday ,phone, correct_phone) \
        VALUES(NULL, "{fn}", "{ln}" , "{bd}", "{phone}" , "{cor_phone}")'.format(\
            fn = record.first_name, ln = record.last_name , bd = record.birthday ,\
            phone = record.phone_number, cor_phone = record.legal_phone_number )

        cur=self.db_conection.cursor()
        cur.execute(query)
        self.db_conection.commit()

    def add_record(self):
        record=Record()
        print Messages.add_record
        user_input = raw_input("input record parameters, please: ")
        try:
            user_input = user_input.strip("     \t\n\r")
            user_input = user_input.split(',')
            record.fill_record_user_input(user_input)
        except Exception as e:
            logging.warning("user input error: {e}".format(e = e))
            print "you input wrong data, please try again "
            return None

        if len(record.first_name)<2:
            print "you input wrong data, first name too short, please try again "
            return None

        if len(record.last_name)<2:
            print "you input wrong data, last name too short, please try again "
            return None
        if self.__is_record_duplicate(record):
            print "you already have such record,use another first name"
            return None

        if self.__helper.check_date_format(record.birthday) != True:
            print "you input wrong data, invalid birthday, please try again "
            user_input = raw_input("skip birthday? (type yes or no: ")
            if user_input is "yes":
                record.birthday=None
            else:
                user_input = raw_input("input  birthday  date using YYYY-MM-DD format (for example 1974-03-27)")
                if self.__helper.check_date_format(record.birthday) != True:
                    print "incorrect input"
                    return None

        if self.__helper.check_phone_number(record.phone_number) != True:
            user_input = raw_input("you input {ph} as phone number, it looks like incorrect, save this number anyway?/"
                                   " (type yes to save, or no to go to command menu".format(ph = record.phone_number))
            if user_input == "yes":
                record.legal_phone_number=0
                self.__db_add_record(record)
                return None
            else:
                return None

        record.legal_phone_number=0
        self.__db_add_record(record)
        print "record sucessfully aded"

    def _db_find_record(self,query):
        records_id=[]
        db_query='SELECT * from records where firstName like "%{q}%"'.format(q = query)
        cur=self.db_conection.cursor()
        cur.execute(db_query)
        res=cur.fetchall()
        print "we found {n} records:".format(n=len(res))
        for i in res:
            rec=Record()
            rec.fill_record_from_db(i)
            records_id.append(rec.id)
            rec.print_record()
        return records_id

    def _db_find_record_by_id(self,id):
        db_query='SELECT * from records where id = "{q}"'.format(q = id)
        cur=self.db_conection.cursor()
        cur.execute(db_query)
        res=cur.fetchall()[0]
        if res!=[]:
            record=Record()
            record.fill_record_from_db(res)
            return record
        else:
            return None

    def find_record(self):
        print Messages.find_record
        user_input = raw_input("input record parameters, please: ")
        #TODO remove all non alfnum symbols, check encoding
        user_input = user_input.strip("     \t\n\r")
        return self._db_find_record(user_input)

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
        records_id = self.find_record()
        user_input = raw_input("please input id of record should be deleted")
        id=int(user_input)
        if id not in records_id:
            print "no such id in find records"
            return None
        rec_to_delete=self._db_find_record_by_id(id)
        allowed_id=[]
        if rec_to_delete != None:
            rec_to_delete.print_record()
            print "are you really want to delete this record?"
            user_input = raw_input("please input id of record should be deleted (input yes or no)" )
            if user_input == "yes":
                self.__db_remove_record(id)
                print "record deleted"
        else:
            print "no such record"

    def select_all(self):
        db_query='SELECT * from records'
        cur=self.db_conection.cursor()
        cur.execute(db_query)
        res=cur.fetchall()
        for i in res:
            rec=Record()
            rec.fill_record_from_db(i)
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
            self.__check_birthdays()
            while self.stop_flag:
                self.loop()
        except Exception,e:
            print "error in program: {exc}".format(exc = e)
        finally:
            try:
                logging.error("destroing DB connection")
                self.db_conection.close()
            except Exception,e:
                print "probably connection already closed"

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
    #print dir(A)
    #A._Application__is_record_duplicate(rec)
    #A._db_find_record_by_id(5)
    #A.select_all()
    A.db_conection.close()

if __name__ == "__main__":
    test()