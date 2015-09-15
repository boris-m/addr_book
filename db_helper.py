import logging
import os
import sqlite3
import datetime
import run


class DbHelper(object):
    def __init__(self):
        self.storage_file="storage.db"
        logging.debug("init DB")
        super(DbHelper,self).__init__()

        if not os.path.isfile(self.storage_file):
            con = sqlite3.connect(self.storage_file)
            cur = con.cursor()
            create_table_query='CREATE TABLE records (id INTEGER PRIMARY KEY, firstName VARCHAR(100), lastName VARCHAR(100) , birthday VARCHAR(10), phone INTEGER, correct_phone INTEGER )'
            cur.execute(create_table_query)
            con.commit()
            self.db_connection = con
        else:
            self.db_connection = sqlite3.connect(self.storage_file)


    def _exec(self,query):
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        self.db_connection.commit()
        cursor.close()
        return res

    def is_record_duplicate(self,record):
          #TODO check another fields
          query='select id from records where firstName = "{fn}"'.format(fn = record.first_name)
          res=self._exec(query)
          if res != []:
              return True
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