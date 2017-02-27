from time import localtime, strftime
import logging
import aws
from scheduler import *
from actions import *
import config

def main():
    start_time = localtime()
    instances = aws.get_croned_instances()

    # logging configuration
    logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', filename=config.log_file_path, level=config.log_level)
    # suppress most of boto library logs
    logging.getLogger('botocore').setLevel(config.boto_log_level)
    logging.getLogger('boto3').setLevel(config.boto_log_level)

    logging.debug("aws_cron start time %s", strftime("%d-%m-%Y %H:%M:%S %Z", start_time))
    for instance in instances:
        schedules, actions = decode_schedule_tags(instance)
        for item, schedule in schedules.items():
           if should_i_run(schedule, start_time):
                run_action(actions[item], instance)


if __name__ == '__main__':
    main()