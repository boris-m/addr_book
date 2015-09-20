class TasksTest(object):

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

    def show_all(self):
        print self._db_hlp.select_all()

    def exit(self):
        sys.exit(0)

