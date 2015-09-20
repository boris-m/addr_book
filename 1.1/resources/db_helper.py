import sys
from record import Record
from settings  import Settings
from db_queries  import DbQueries
import logging
import os
import sqlite3



class DbHelper(object):
    def __init__(self):
        logging.debug("[DbHelper] init ")
        self.conn = None
        self.__storage_file = Settings.db_file_path
        self.__queries = DbQueries()
        self.__check_db_exist()

    def __check_db_exist(self):
        logging.debug("[DbHelper] db file is {fl}".format(fl = self.__storage_file))
        if not os.path.isfile(self.__storage_file):
            logging.debug("[DbHelper] no db files found, init new DB")
            con = sqlite3.connect(self.__storage_file)
            cur = con.cursor()
            cur.execute(self.__queries.init_db)
            con.commit()
            self.conn = con
        else:
            logging.debug("[DbHelper] DB file found")
            self.conn = sqlite3.connect(self.__storage_file)

    def _exec(self,query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return res
    #+
    def __is_record_duplicate(self,record):
        result=[]
        query='select id from records where lastName = "{ln}" or phone = "{ph}"'.format(\
            ln = record.last_name, ph = record.phone_number)
        query_res=self._exec(query)
        print query_res
        if query_res != []:
              for i in query_res:
                 result.append(i[0])
              logging.debug("[is record duplicate] record is duplicate with next ID`s: {id}".format(id = result))
              return result
        logging.debug("[is record duplicate] record is NOT duplicate")
        return False

    def find_record(self,req):
        records_id=[]
        query='SELECT * from records where firstName like "%{q}%"'.format(q = req)
        res=self._exec(query)
        #print "there are  {n} records:".format(n=len(res))
        for i in res:
            rec=run.Record()
            rec.fill_record_from_db(i)
            records_id.append(rec.id)
            rec.print_record()
        return records_id

    def remove_record(self,id):
        id=int(id)
        query='DELETE  FROM records where id={uid}'.format(uid=id)
        self._exec(query)
    #+
    def find_record_by_id(self,id):
        query='SELECT * from records where id = "{q}"'.format(q = id)
        logging.debug("[find record by id] db query is : {q} ".format(q = query))
        res=self._exec(query)[0]
        logging.debug("[find record by id] db result is : {r} ".format(r = res))
        if res!=[]:
            rec=Record() #TODO refactor??
            rec.fill_record_from_db(res)
            return rec
        else:
            return None

    def set_record(self,id,record):

        query = self.__queries.update_record(record)
        result=self._exec(query)
    #+
    def select_all(self):
        result=[]
        query='SELECT * from records'
        res=self._exec(query)
        for i in res:
            rec=Record()
            rec.fill_record_from_db(i)
            result.append(rec)
        return result
    #+
    def add_record(self,record):
        logging.debug("[add record] start  with parameters: {p}]".format(p = record))
        duplicate = self.__is_record_duplicate(record)
        if duplicate is False:
            query=self.__queries.add_record(record)
            res=self._exec(query)
            logging.debug("[add record ] result is: {r}".format(r = res))
        else:
            if len((duplicate))!=0:
                for i in duplicate:
                    print "looks like you already have such record.\n{data}try different parameters"\
                        .format(data = self.find_record_by_id(i))
    #+- check query
    def check_birthdays(self):
        result=""
        db_data=self._exec(self.__queries.get_bdays)
        logging.debug("[check birthday] db query result {res}".format(res = db_data))
        if db_data == []:
            result = "no birthdays next 3 days "
        else:
            for i in db_data:
                name = i[0]
                date = i[1]
                timediff=float(i[2])
                if timediff<0:
                    result+="Today is {nm}`s birthday! \n".format(nm = name)
                else:
                    result+="{nm} has birthday on {dt} \n".format(nm = name, dt = date)
        return result


def debug():
    root = logging.getLogger()
    #root.setLevel(logging.DEBUG)
    #logging.StreamHandler(sys.stdout)
    db=DbHelper()
    rec=Record
    rec.last_name="testLname"
    rec.first_name="testFname"
    rec.birthday = "1777.10.10"
    rec.phone_number = "1111111111"
    rec.legal_phone_number = 1
    #db.check_birthdays()
    db.add_record(rec)

if __name__ == "__main__":
    debug()