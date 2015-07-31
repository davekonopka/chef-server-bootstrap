import troposphere.ec2 as ec2
from troposphere import Base64, Ref, Template

template = Template()

# Define the instance security group
instance_sg = template.add_resource(
    ec2.SecurityGroup(
        "InstanceSecurityGroup",
        GroupDescription="Enable SSH and HTTP access on the inbound port",
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
    "Ec2Instance",
    ImageId="ami-7be63d10",
    KeyName="experiment_dkonopka.pem",
    InstanceType="m3.medium",
    SecurityGroups=[Ref(instance_sg)],
    UserData=Base64(cloud_init)
))

print(template.to_json())
