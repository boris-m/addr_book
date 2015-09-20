import logging



def execute_task(tasks_object,arg):
        tasks=tasks_object
        try:
            logging.debug("[exec task] {tsk}".format(tsk = arg))
            task=getattr(tasks, arg)
            task()
        except Exception as e:
            logging.error( "[exec task] error:{err}".format(err = e))
            print "try one more time"