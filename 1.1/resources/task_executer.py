import logging

def execute_input_task(tasks_object):
        tasks=tasks_object
        user_input=raw_input("input command please: ")
        try:
            logging.debug("[exec task] {tsk}".format(tsk = user_input))
            task=getattr(tasks, str(user_input))
            task()
        except Exception as e:
            logging.error( "[exec task] error:{err}".format(err = e))
            print "try one more time"

def execute_task(tasks_object,arg):
        tasks=tasks_object
        try:
            logging.debug("[exec task] {tsk}".format(tsk = arg))
            task=getattr(tasks, arg)
            task()
        except Exception as e:
            logging.error( "[exec task] error:{err}".format(err = e))
            print "try one more time"__author__ = 'bmolchan'
