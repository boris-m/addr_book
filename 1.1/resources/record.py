import logging


class Record(object):
    def __init__(self):
        self.id=None
        self.first_name=None
        self.last_name=None
        self.birthday=None
        self.phone_number=None
        self.legal_phone_number=0 #sqllite have no BOOL so 0 is False

    def __repr__(self):
        repr = "First name: {fn}\nLast name: {ln}\nBirthday: {bd}\nPhone-number:{pn}\n"\
            .format(fn = self.first_name, ln = self.last_name , bd = self.birthday, pn = self.phone_number)
        return repr

    def fill_record_from_db(self,data):
        logging.debug("[fill_record_from_db] data is: {dt}".format(dt = data))
        try:
            self.id=data[0]
            self.first_name=data[1]
            self.last_name=data[2]
            self.birthday=data[3]
            self.phone_number=data[4]
            self.legal_phone_number=data[5]
        except Exception,e:
            print "can not parse record:{err}".format(err=e)

    def fill_record_user_input(self , args):
        try:
            self.first_name=args[0]
            self.last_name=args[1]
            self.birthday=args[2]
            self.phone_number=args[3]
        except Exception as e:
            print "can not parse record:{err}".format(err=e)