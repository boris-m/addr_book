from messages import Messages

class Settings(object):
    def __init__(self):
        self.dialpan=None

class Record(object):
    def __init__(self):
        self.first_name=None
        self.last_name=None
        self.birth_date=None
        self.phone_number=None
        self.legal_phone_number=False

class AdressBook(object):
    def __init__(self):
        pass
    def get_record_by_name(self,name):
        pass
    def get_record_by_number(self,number):
        pass
    def set_record(self,record):
        pass
    def remove_record(self,record):
        pass

class PhoneNumberValidater(object):
    def validate(self,number):
        result=False
        number=self.remove_undigit(number)
        return result

    def _remove_undigit(self, number):
        return number

class Tasks(object):

    def test(self):
        print "just test task"

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

    def remove(self):
        pass

    def change(self):
        pass

    def find(self):
        pass

    def show_all(self):
        pass



def execute_task(command):
    task=Tasks()
    if command=="add" or command == "a":
        task.add_record()
    elif command == "remove" or command == "r":
        task.remove()
    elif command == "change" or command == "c":
        task.remove()
    elif command == "find" or command == "f":
        task.find()
    elif command == "show_all" or command == "s":
        task.show_all()
    else:
        print "no such command ({cmd})\r\n{man}".format(cmd=command, man=Messages.intro)
def main():
    stop_flag=True
    print Messages.intro

    try:
        while stop_flag:
            user_input = raw_input("input command please: ")
            execute_task(user_input)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

