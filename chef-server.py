import troposphere.ec2 as ec2
from troposphere import Base64, FindInMap, Parameter, Ref, Template

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

template.add_parameter(Parameter(
    "InstanceType",
    Type="String",
    Description="EC2 instance type",
    Default="m3.medium",
    AllowedValues=[
        "m3.medium", "m3.large", "m3.xlarge", "m3.2xlarge",
        "c1.medium", "c1.xlarge", "cc1.4xlarge", "cc2.8xlarge", "cg1.4xlarge"
    ],
    ConstraintDescription="Must be a valid, EC2 classic compatible instance type.",
))

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

ec2_instance = template.add_resource(ec2.Instance(
    "ChefServerInstance",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    KeyName=Ref(keyname_param),
    InstanceType=Ref("InstanceType"),
    SecurityGroups=[Ref(instance_sg)],
    UserData=Base64(cloud_init)
))

print(template.to_json())
