from aws import *
import logging

def run_action(action,instance):
    """switch/case alike for defined action"""
    if action == "start":
        logging.info("Running START action on instance %s", instance.id)
        result=start_instance(instance)
    elif action == "stop":
        logging.info("Running STOP action on instance %s", instance.id)
        result=stop_instance(instance)
    elif action[:11] == "change_type":
        logging.info("Running CHANGE_TYPE action on instance %s", instance.id)
        instance_type = action.split(" ")[1]
        result = change_instance_type(instance, instance_type)
    else:
        logging.critical("Unknown action (%s) provided for instance %s", action,instance.id)
        return None
    return result
