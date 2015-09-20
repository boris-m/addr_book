import logging
import sys
from resources.tasks import Tasks

def _execute_task(tasks_object):
        tasks=tasks_object
        user_input=raw_input("input command please: ")
        logging.debug("[exec task] {tsk}".format(tsk = user_input))
        task=getattr(tasks, str(user_input))
        task()

def main_loop(tasks=Tasks()):
    loop_stopper = False
    print (tasks._first_run()) #is it necessary to to wrap it ? potential bug place? - wrap it inside function because it is not major function
    print tasks._cmd_list
    while not loop_stopper:
        try:
            _execute_task(tasks_object=tasks)
        except KeyboardInterrupt:
            logging.debug("[main_loop] loop stopped by keyboard intererupt")
            loop_stopper = True
        except Exception as e:
            #loop_stopper = True
            print "error executing command, please try again"
            logging.error("[main_loop] error : {ex}".format(ex = e))


if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    main_loop()

