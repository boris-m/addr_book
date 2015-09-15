import logging
import time
import db_helper
from messages import Messages

class Check(object):
    def phone_number(self, num):


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
        except Exception as e:
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

class Application(object):

    def __init__(self):
        self.db = db_helper.DbHelper()
        self.stop_flag = True
        self.__helper=Check()
        logging.basicConfig(level = logging.DEBUG)

    def __del__(self):
        logging.debug("start destructor")

    def add_record(self):
        #TODO refactor it
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
        if self.db.is_record_duplicate(record):
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

        if self.__helper.phone_number(record.phone_number) != True:
            user_input = raw_input("you input {ph} as phone number, it looks like incorrect, save this number anyway?/"
                                   " (type yes to save, or no to go to command menu".format(ph = record.phone_number))
            if user_input == "yes":
                record.legal_phone_number=0
                self.db.add_record(record)
                return None
            else:
                return None

        record.legal_phone_number=0
        self.db.add_record(record)
        print "record sucessfully aded"

    def find_record(self):
        #TODO remove all non alfnum symbols, check encoding
        print Messages.find_record
        user_input = raw_input("input record parameters, please: ")
        query = user_input.strip("     \t\n\r")
        logging.debug("search query is {q}".format(q = query))
        return self.db.find_record(query)

    def select_all(self):
        self.db.select_all()

    def remove_record(self):
        print Messages.remove_record_first
        records_id = self.find_record()
        print "you can delete {rec} id`s".format(rec = records_id)
        user_input = raw_input("please input id of record should be deleted")
        id=int(user_input)
        if id not in records_id:
            print "no such id in find records"
            return None
        rec_to_delete=self.db.find_record_by_id(id)

        if rec_to_delete != None:
            rec_to_delete.print_record()
            print "are you really want to delete this record?"
            user_input = raw_input("please input id of record should be deleted (input yes or no)" )
            if user_input == "yes":
                self.db.remove_record(id)
                print "record deleted"
        else:
            print "no such record"

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
            self.db.check_birthdays()
            while self.stop_flag:
                self.loop()
        except Exception,e:
            print "error in program: {exc}".format(exc = e)
        finally:
            try:
                logging.error("destroing DB connection")
                self.db.db_connection.close()
            except Exception,e:
                print "probably connection already closed"

def main():
    a=Application()
    a.run()

def tmp():
    A=Application()
    #A.db.remove_record(5)
    #con= A.db_conection
    #cur=con.cursor()
    rec=Record()
    rec.last_name="testlastname"
    rec.first_name="testFirstname"
    rec.birthday="2003-09-14"
    rec.phone_number="12341243"
    rec.legal_phone_number=0
    A.db.find_record("tmp")
    #A.run()
    #print dir(A)
    A.db.is_record_duplicate(rec)
    #A._db_find_record_by_id(5)
    A.db.select_all()
    #A.db_conection.close()

if __name__ == "__main__":
    main()
    #tmp()