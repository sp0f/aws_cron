AWS Cron
========
Similar to regular cron but for EC2 instances.

#### How does it work
1. Tag your instance with pair of tags: cron_schedule._X_ and cron_action._X_ where _X_ is a integer, ie
`cron_schedule.0: * 20 * * *` and `cron_action.0: shutdown`
2. Run aws_cron.py fron regular cron every minute ie.
`* * * * * /usr/local/bin/aws_cron.py`

#### Planed actions
* stop : shutdown instance
* start : run instance
* change_type _instance type_ :
    * if instance is in 'stopped' state -> change its type
    * if instance is in 'running' state -> stop, change type, start

#### Why ?
Because it's easier to let people tag their own instances than to give them permission and knowledge to run cli action by them self.