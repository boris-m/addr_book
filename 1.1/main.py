import logging
from resources.tasks import Tasks
import resources.task_executer as te


def main():
    loop_stopper = False
    tasks=Tasks()
    tasks.check_birthdays() #is it necessary to to wrap it ? potential bug place? - wrap it inside function because it is not major function
    while not loop_stopper:
        try:
            te.execute_input_task(tasks_object=tasks)
        except KeyboardInterrupt:
            logging.debug("main loopstopped by keyboard intererupt")
            loop_stopper = True
        except Exception as e:
            loop_stopper = True
            logging.error("error in main loop: {ex}".format(ex = e))




if __name__ == "__main__":
    #tmp()
    main()

