# Chef Server bootstrap

Bootstrap a Chef Server from scratch.

## Components

* `bootstrap-chef.sh` Chef server bootstrap bash script.
* `Vargantfile` Vagrant test harness for bootstrap script.
* `chef-server.py` [Troposphere](https://github.com/cloudtools/troposphere) CloudFormation template for launching an EC2 instance.
* `chef-server.json` Generated CloudFormation json.

## Commands

### Generate CloudFormation json

* `python chef-server.py > chef-server.json`

### Launch CloudFormation stack

* `aws cloudformation create-stack --stack-name chef-server --template-body file://./chef-server.json --parameters ParameterKey=KeyName,ParameterValue=somekey`
