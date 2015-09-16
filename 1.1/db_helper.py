from resources.settings  import Settings
from resources.db_queries  import DbQueries
import logging
import os
import sqlite3
import datetime
import run


class DbHelper(object):
    def __init__(self):
        self.conn = None
        self.__storage_file = Settings.db_file_path
        self.__queries = DbQueries()
        logging.debug("init DB helper")
        self.__check_db_exist()

    def __check_db_exist(self):
        if not os.path.isfile(self.__storage_file):
            logging.debug("no db files found, init new DB")
            con = sqlite3.connect(self.__storage_file)
            cur = con.cursor()
            cur.execute(self.__queries.init_db)
            con.commit()
            self.conn = con
        else:
            self.conn = sqlite3.connect(self.__storage_file)

    def _exec(self,query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return res

    def is_record_duplicate(self,record):
          query='select id from records where firstName = "{fn}" || lastName = "{ln}" || phone = "ph"'\
          .format(fn = record.first_name , ln = record.last_name, ph = record.phone_number)
          res=self._exec(query)
          if res != []:
              return res
          return False

    def find_record(self,req):
        records_id=[]
        query='SELECT * from records where firstName like "%{q}%"'.format(q = req)
        res=self._exec(query)
        print "there are  {n} records:".format(n=len(res))
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


        
    def find_record_by_id(self,id):
        query='SELECT * from records where id = "{q}"'.format(q = id)
        res=self._exec(query)[0]
        if res!=[]:
            record=run.Record() #TODO refactor??
            record.fill_record_from_db(res)
            return record
        else:
            return None

    def set_record(self,id,record):
        #TODO - implement
        return  None
        query='UPDATE records' \
              ' SET id = "{uid}", firstName = "{fn}" , lastName = "{ln}" ,birthday = "{bd}"  ,' \
              'phone = "{phone}" , correct_phone = "{cor_phone}"' \
              ' WHERE id={uid};'.format( uid = id , fn = record.first_name, ln = record.last_name ,\
               bd = record.birthday ,phone = record.phone_number, cor_phone = record.legal_phone_number )
        self._exec(query)

    def select_all(self):
        query='SELECT * from records'
        res=self._exec(query)
        for i in res:
            rec=run.Record()
            rec.fill_record_from_db(i)
            rec.print_record()

    def add_record(self,record):
        query='INSERT INTO records (id, firstName, lastName ,birthday ,phone, correct_phone) \
        VALUES(NULL, "{fn}", "{ln}" , "{bd}", "{phone}" , "{cor_phone}")'.format(\
            fn = record.first_name, ln = record.last_name , bd = record.birthday ,\
            phone = record.phone_number, cor_phone = record.legal_phone_number )

        res=self._exec(query)
        logging.debug(res)

    def check_birthdays(self):
        tmp_today=datetime.date.today()
        today="1000-{m}-{d}".format( m = tmp_today.month , d =tmp_today.day )
        future_date=str(datetime.date.today()+datetime.timedelta(days=3))
        query="""select *, julianday(strftime('%Y', 'now')||strftime('-%m-%d', birthday))-julianday('now') as bd  from records where bd between 0 and 3"""
        res=self._exec(query)
        logging.debug("check birthday db query result {res}".format(res = res))
        if res == []:
            print "no birthdays next 3 days "
            return None
        else:
            rec=run.Record()
            for i in res:
                rec.fill_record_from_db(i)
                try:
                    tmp=datetime.datetime.strptime(rec.birthday, "%Y-%m-%d").date()
                    diff=tmp.day - datetime.date.today().day
                    bd=None
                    print diff
                    if diff>0:
                        bd="at {d} day of {m} month, {n} days left".format(d = tmp.day,m = tmp.month, n = diff)
                    if diff == 0:
                        bd="TODAY!"
                    print "{fn} {ln} have birthday  {date}".format(fn=rec.first_name , ln=rec.last_name , date=bd)
                except Exception as e:
                    logging.error("some error in __check_birthdays: {err}".format(err = e))
        return None