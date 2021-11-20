from pulumi_aws import ec2, get_availability_zones
from pulumi import Config
## VPC
config = Config()
eks_cluster_name = config.require("cluster_name")

vpc = ec2.Vpc(
    f"{eks_cluster_name}-vpc",
    cidr_block='10.100.0.0/16',
    instance_tenancy='default',
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        'Name': f"{eks_cluster_name}-vpc",
    },
)

igw = ec2.InternetGateway(
    f"{eks_cluster_name}-vpc-ig",
    vpc_id=vpc.id,
    tags={
        'Name': f"{eks_cluster_name}-pulumi-vpc-ig",
    },
)

eks_route_table = ec2.RouteTable(
    f"{eks_cluster_name}-vpc-route-table",
    vpc_id=vpc.id,
    routes=[ec2.RouteTableRouteArgs(
        cidr_block='0.0.0.0/0',
        gateway_id=igw.id,
    )],
    tags={
        'Name': f"{eks_cluster_name}-pulumi-vpc-rt",
    },
)

## Subnets, one for each AZ in a region

zones = get_availability_zones()
subnet_ids = []

for zone in zones.names:
    vpc_subnet = ec2.Subnet(
        f"{eks_cluster_name}-vpc-subnet-{zone}",
        assign_ipv6_address_on_creation=False,
        vpc_id=vpc.id,
        map_public_ip_on_launch=True,
        cidr_block=f'10.100.{len(subnet_ids)}.0/24',
        availability_zone=zone,
        tags={
            'Name': f"{eks_cluster_name}-pulumi-sn-{zone}",
            f"kubernetes.io/cluster/{eks_cluster_name}" : "shared",
            "kubernetes.io/role/internal-elb" : "1"
        },
    )
    ec2.RouteTableAssociation(
        f"{eks_cluster_name}-vpc-route-table-assoc-{zone}",
        route_table_id=eks_route_table.id,
        subnet_id=vpc_subnet.id,
    )
    subnet_ids.append(vpc_subnet.id)

## Security Group

eks_security_group = ec2.SecurityGroup(
    f"{eks_cluster_name}-eks-cluster-sg",
    vpc_id=vpc.id,
    description='Allow all HTTP(s) traffic to EKS Cluster',
    tags={
        'Name': f"{eks_cluster_name}-pulumi-cluster-sg",
    },
    ingress=[
        ec2.SecurityGroupIngressArgs(
            cidr_blocks=['0.0.0.0/0'],
            from_port=443,
            to_port=443,
            protocol='tcp',
            description='permit 443 tcp from any.'
        ),
        ec2.SecurityGroupIngressArgs(
            cidr_blocks=['0.0.0.0/0'],
            from_port=80,
            to_port=80,
            protocol='tcp',
            description='permit 80 tcp from any'
        ),
    ],
)
