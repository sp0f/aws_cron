import boto3
import logging

ec2 = boto3.resource('ec2')

def decode_schedule_tags(instance):
    """
    building two dicts:
    scheudles indexed by cron action number and containing a schedule in original cron format
    actions indexed by cron action number and containing action to launch
    """

    tags = instance.tags
    schedules = {}
    actions = {}
    for tag in tags:
        if tag['Key'][:4] == "cron":
            tag_type, tag_number = tag['Key'].split(".")
            if tag_type == "cron_schedule":
                schedules[tag_number] = tag['Value']
                logging.debug("decode_schedule_tags() | Adding schedule %s to schedules dict as position %s", tag['Value'], tag_number)
            elif tag_type == "cron_action":
                actions[tag_number] = tag['Value']
                logging.debug("decode_schedule_tags() | Adding action %s to actions dict as position %s", tag['Value'], tag_number)
    return schedules, actions


def should_i_run(schedule, start_time):
    """return True if corespondig to this schedule action should be run, otherwise return False"""
    minutes, hour, day_of_month, month, day_of_week = schedule.split(" ")
    logging.debug("should_i_run() | decoding schedule tag")
    logging.debug("should_i_run() | SCHEDULE minutes: %s, hours: %s, day of month: %s, month: %s, day of week: %s",
                  minutes, hour, day_of_month, month, day_of_week)
    logging.debug("should_i_run | START_TIME minutes: %s, hours: %s, day of month: %s, month: %s, day of week: %s",
                  start_time.tm_min, start_time.tm_hour, start_time.tm_mday, start_time.tm_mon, start_time.tm_wday)

    if month != str(start_time.tm_mon) and month != "*":
        # schedule is for different month
        return False
    elif day_of_month != str(start_time.tm_mday) and day_of_month != "*":
        # different day of month
        return False
    elif day_of_week != str(start_time.tm_wday) and day_of_week != "*":
        # different day of week
        return False
    elif hour != str(start_time.tm_hour) and hour != "*":
        # different hour
        return False
    elif minutes != str(start_time.tm_min) and minutes != "*":
        # different minute
        return False
    else:
        # action should be run just now !
        return True
