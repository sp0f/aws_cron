import boto3

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
    print "Starting instance: "+instance.id
    instance_state=instance.state['Name']
    if instance_state != "stopped":
        print "Instance in state {}. Can't start!".format(instance_state)
        return None
    else:
        result=instance.start(AdditionalInfo="Starged by AWS cron")
        # TODO: set waiter
        return result


def stop_instance(instance):
    print "Stopping instance: "+instance.id
    instance_state=instance.state['Name']
    if instance_state != "running":
        print "Instance in state {}. Can't stop!".format(instance_state)
        return None
    else:
        result = instance.stop()
        # TODO: set waiter
        return result

def change_instance_type(instance,instance_type):
    print "Change instance {} type to {}".format(instance.id,instance_type)
    instance_state=instance.state['Name']
    if instance_state != "running" and instance_state != "stopped":
        print "Instance {} in state {}. Can't change type.".format(instance.id,instance_state)
        return None
    elif instance.state['Name'] == "running":
        print "Instance {} in 'running' state. Stopping it first.".format(instance.id)
        instance.stop()
        instance.wait_until_stopped()
        instance.modify_attribute(
            InstanceType={
                'Value': instance_type
            }
        )
        instance.start()
    else:
        instance.modify_attribute(
            InstanceType={
                'Value': instance_type
            }
        )


