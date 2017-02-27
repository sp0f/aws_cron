import boto3
import logging

ec2 = boto3.resource('ec2')

def get_croned_instances():
    """returns collection of all instances with proper AWS Cron tags:
        * cron-schedule-[0...n]
        * cron-schedule-[0...n]
    """
    instances=ec2.instances.filter(Filters=[
        {
            "Name": "tag-key",
            "Values": ["cron_schedule*"]
        },
        {
            "Name": "tag-key",
            "Values": ["cron_action*"]
        }
    ])
    return instances

def start_instance(instance):
    """start stopped instace"""
    instance_state=instance.state['Name']
    if instance_state != "stopped":
        logging.critical("Instance %s in state %s - can't START", instance.id, instance_state)
        return None
    else:
        result=instance.start(AdditionalInfo="Starged by AWS cron")
        # TODO: set waiter
        return result


def stop_instance(instance):
    """stop running instance"""
    instance_state=instance.state['Name']
    if instance_state != "running":
        logging.critical("Instance %s in state %s - can't STOP", instance.id, instance_state)
        return None
    else:
        result = instance.stop()
        # TODO: set waiter
        return result

def change_instance_type(instance,instance_type):
    """change instance type. If instance is in 'running' state shut it down first and start again after type change"""
    logging.info("Changing instance %s type to %s", instance.id, instance_type)
    instance_state = instance.state['Name']
    if instance_state != "running" and instance_state != "stopped":
        logging.critical("Instance %s in state %s. Can't CHANGE TYPE", instance.id, instance_state)
        return None
    elif instance.state['Name'] == "running":
        logging.warning("Instance %s is in 'running' state. Stopping it first.", instance.id)
        instance.stop()
        logging.debug("change_instance_type() | Waiting for instance %s to stop", instance.id)
        instance.wait_until_stopped()
        logging.debug("change_instance_type() | Instance %s has stopped", instance.id)
        instance.modify_attribute(
            InstanceType={
                'Value': instance_type
            }
        )
        logging.debug("change_instance_type() | Starting instance %s as %s", instance.id, instance_type)
        instance.start()
    else:
        instance.modify_attribute(
            InstanceType={
                'Value': instance_type
            }
        )

