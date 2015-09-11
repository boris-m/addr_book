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

    def remove_undigit(self, number):
        return number


def main():
    pass


if __name__ == '__main__':
    main()

