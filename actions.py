from aws import *

def run_action(action,instance):
    """switch/case alike for defined action"""
    if action == "start":
        result=start_instance(instance)
    elif action == "stop":
        result=stop_instance(instance)
    elif action[:11] == "change_type":
        instance_type = action.split(" ")[1]
        result = change_instance_type(instance, instance_type)
    else:
        return None
    return result