import sys
from db_helper import DbHelper
from messages import Messages


class Tasks(object):

    def __init__(self):
        self._db_hlp = DbHelper()
        self._cmd_list = self._get_cmd_list()

    def _first_run(self):
        #print birthday dates
        return self._db_hlp.check_birthdays()

    def _get_cmd_list(self):
        res="available commands: \r\n"
        for i in dir(self):
            if not i.startswith('_'):
                res += "- "+i +"\r\n"
        return res[:-2]

    def add_record(self):
        user_input = raw_input(Messages.add_record)
        user_input = self.__check_input(user_input)

    def show_all(self):
        for i in self._db_hlp.select_all():
            print i

    def exit(self):
        sys.exit(0)





def test():
    #pass
    t=Tasks()
    t.add_record()
    #t.show_all()
    #print t._cmd_list
if __name__ == "__main__":
    test()