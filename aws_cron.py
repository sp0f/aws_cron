from time import localtime
import aws
from scheduler import *
from actions import *

def main():
    # TODO: get startup time
    start_time=localtime()
    instances=aws.get_croned_instances()

    for instance in instances:
        schedules, actions = decode_schedule_tags(instance)
        for item, schedule in schedules.items():
           if should_i_run(schedule, start_time):
                run_action(actions[item], instance)


if __name__ == '__main__':
    main()