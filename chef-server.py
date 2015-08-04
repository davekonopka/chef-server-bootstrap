import troposphere.ec2 as ec2
from troposphere import Base64, FindInMap, GetAtt
from troposphere import Join, Output, Parameter, Ref, Template
from troposphere import Condition, Equals, And, Or, Not, If

template = Template()

# Mappings

# Ubuntu Trusty 64 bit HVM
template.add_mapping("RegionMap", {
    "us-east-1": {"AMI": "ami-7be63d10"}
})

# Parameters
keyname_param = template.add_parameter(Parameter(
    "KeyName",
    Type="String",
    Description="Name of an existing EC2 KeyPair to "
                "enable SSH access to the instance",
))

environment_param = template.add_parameter(Parameter(
    "Environment",
    Type="String",
    Default="development",
    Description="Name of an environment to put the instance in",
))

eip_param = template.add_parameter(Parameter(
    "EIP",
    Type="String",
    Default="0.0.0.0",
    MinLength=7,
    MaxLength=15,
    AllowedPattern="(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})",
    Description="Elastic IP Address to associate with the instance",
    ConstraintDescription="Must be a valid ip address."
))

template.add_parameter(Parameter(
    "InstanceType",
    Type="String",
    Description="EC2 instance type",
    Default="m3.medium",
    AllowedValues=[
        "m3.medium", "m3.large", "m3.xlarge", "m3.2xlarge",
        "c1.medium", "c1.xlarge", "cc1.4xlarge", "cc2.8xlarge", "cg1.4xlarge"
    ],
    ConstraintDescription="Must be a valid, EC2 classic "
                          "compatible instance type.",
))

# Conditions
template.add_condition(
    "EIPProvided",
    Not(
        Equals(
            Ref("EIP"),
            "0.0.0.0"
        )
    )
)

# Define the instance security group
instance_sg = template.add_resource(
    ec2.SecurityGroup(
        "InstanceSecurityGroup",
        GroupDescription="Enable SSH access to the world",
        SecurityGroupIngress=[
            ec2.SecurityGroupRule(
                IpProtocol="tcp",
                FromPort="22",
                ToPort="22",
                CidrIp="0.0.0.0/0",
            ),
        ]
    )
)

# Grab cloud-init script from file
cloud_init_file = open("bootstrap-chef.sh")
cloud_init = cloud_init_file.read()
cloud_init_file.close()

chef_server_instance = template.add_resource(ec2.Instance(
    "ChefServerInstance",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    KeyName=Ref(keyname_param),
    InstanceType=Ref("InstanceType"),
    SecurityGroups=[Ref(instance_sg)],
    Tags=[
        ec2.Tag("Name", "Chef Server"),
        ec2.Tag("Environment", Ref(environment_param))
    ],
    UserData=Base64(Join("", cloud_init.splitlines(True)))
))

eipassociation = template.add_resource(ec2.EIPAssociation(
    "EIPAssociation",
    InstanceId=Ref(chef_server_instance),
    EIP=Ref(eip_param),
    Condition="EIPProvided",
))

template.add_output([
    Output(
        "InstanceId",
        Description="InstanceId of the newly created EC2 instance",
        Value=Ref(chef_server_instance),
    ),
    Output(
        "ElasticIp",
        Description="Elastic IP associated with instance",
        Value=Join(" ", [
            "IP address", Ref(eip_param)
        ]),
    ),
])

print(template.to_json())
