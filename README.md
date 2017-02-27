AWS Cron
========
Similar to regular cron but for EC2 instances.

#### Why ?
Because it's easier to let people tag their own instances than to give them permission and knowledge to run cli action by themselves.


#### How does it work
1. Tag your instance with pair of tags: `cron_schedule.X` and `cron_action.X` where _X_ is something meaningful or just a integer, i.e.
`cron_schedule.0: * 20 * * *` and `cron_action.0: shutdown`
2. Run aws_cron.py fron regular cron every minute ie.
`* * * * * /usr/local/bin/aws_cron.py`

#### Actions
* stop : shutdown instance
* start : run instance
* change_type _instance type_ :
    * if instance is in 'stopped' state -> change its type
    * if instance is in 'running' state -> **stop**, change type, start

#### IAM permissions
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstanceAttribute",
                "ec2:DescribeInstanceStatus",
                "ec2:DescribeInstances",
                "ec2:DescribeTags",
                "ec2:ModifyInstanceAttribute",
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

#### Logging
Logging configuration in `config.yaml`

