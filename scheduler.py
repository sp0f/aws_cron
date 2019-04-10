import boto3
import logging

ec2 = boto3.resource('ec2', region_name='eu-west-1')

def decode_schedule_tags(instance):
    """
    building two dicts:
    scheudles indexed by cron action number and containing a schedule in original cron format
    actions indexed by cron action number and containing action to launch
    """

    #  TODO: add schedule format checking and multiple space removal
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

    #  TODO: add lists of values, ranges and step

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


def should_i_run_complex(schedule, start_time):
    """return True if corirespondig to this schedule action should be run, otherwise return False"""

    #  TODO: need to be tested !!!

    minutes, hour, day_of_month, month, day_of_week = schedule.split(" ")
    logging.debug("should_i_run() | decoding schedule tag")
    logging.debug("should_i_run() | SCHEDULE minutes: %s, hours: %s, day of month: %s, month: %s, day of week: %s",
                  minutes, hour, day_of_month, month, day_of_week)
    logging.debug("should_i_run | START_TIME minutes: %s, hours: %s, day of month: %s, month: %s, day of week: %s",
                  start_time.tm_min, start_time.tm_hour, start_time.tm_mday, start_time.tm_mon, start_time.tm_wday)
    if not check_field(month, start_time.tm_mon) and month != "*":
        # schedule is for different month
        return False
    elif not check_field(day_of_month, start_time.tm_mday) and day_of_month != "*":
        # different day of month
        return False
    elif not check_field(day_of_week, start_time.tm_wday) and day_of_week != "*":
        # different day of week
        return False
    elif not check_field(hour, start_time.tm_hour) and hour != "*":
        # different hour
        return False
    elif not check_field(minutes, start_time.tm_min) and minutes != "*":
        # different minute
        return False
    else:
        # action should be run just now !
        return True


def check_field(field_value, start_time):
    """in crontab there are 4 types of fields: simple(ie. 6), ranges (ie. 0-24), lists (ie. 0,1,10,14), and steps (ie. */2 or 12-18/2)
        this function returns True if start time value (ie. minutes) is compliant with corresponding schedule field"""
    special_set=set("-,/")
    if set(field_value).isdisjoint(special_set):
        return simple_check(field_value,start_time)
    elif "/" in field_value:
        return step_check(field_value,start_time)
    elif "-" in field_value:
        return range_check(field_value,start_time)
    else:
        return list_check(field_value,start_time)


def simple_check(field_value, start_time):
    if field_value == str(start_time):
        return True
    else:
        return False


def range_check(field_value, start_time):
    start, end = field_value.split("-")

    # check if start is < than end
    if int(start) > int(end):
        tmp=start
        start=end
        end=tmp

    if int(start) <= start_time <= int(end):
        return True
    else:
        return False


def list_check(field_value,start_time):
    if str(start_time) in field_value.split(","):
        return True
    else:
        return False


def step_check(field_value,start_time):
    # step can be used with ranges and * ie. */2 (every two hour) or 0-23/2
    range, step = field_value.split("/")

    if range == "*":
        if start_time % int(step) == 0:
            return True
        else:
            return False
    else:
        if range_check(range,start_time) and start_time % int(step) == 0:
            return True
        else:
            return False

