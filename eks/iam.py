from pulumi_aws import config, iam
import json
from pulumi import Config

## EKS Cluster Role

config = Config()
eks_cluster_name=config.require("cluster_name")
eks_role = iam.Role(
    f"{eks_cluster_name}-eks-iam-role",
    assume_role_policy=json.dumps({
        'Version': '2012-10-17',
        'Statement': [
            {
                'Action': 'sts:AssumeRole',
                'Principal': {
                    'Service': 'eks.amazonaws.com'
                },
                'Effect': 'Allow',
                'Sid': ''
            }
        ],
    }),
)

iam.RolePolicyAttachment(
    f"{eks_cluster_name}-eks-service-policy-attachment",
    role=eks_role.id,
    policy_arn='arn:aws:iam::aws:policy/AmazonEKSServicePolicy',
)


iam.RolePolicyAttachment(
    f"{eks_cluster_name}-eks-clusterpolicy-attachment",
    role=eks_role.id,
    policy_arn='arn:aws:iam::aws:policy/AmazonEKSClusterPolicy',
)

## Ec2 NodeGroup Role

ec2_role = iam.Role(
    f"{eks_cluster_name}-ec2-nodegroup-iam-role",
    assume_role_policy=json.dumps({
        'Version': '2012-10-17',
        'Statement': [
            {
                'Action': 'sts:AssumeRole',
                'Principal': {
                    'Service': 'ec2.amazonaws.com'
                },
                'Effect': 'Allow',
                'Sid': ''
            }
        ],
    }),
)

iam.RolePolicyAttachment(
    f"{eks_cluster_name}-eks-workernode-policy-attachment",
    role=ec2_role.id,
    policy_arn='arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy',
)


iam.RolePolicyAttachment(
    f"{eks_cluster_name}-eks-cni-policy-attachment",
    role=ec2_role.id,
    policy_arn='arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy',
)

iam.RolePolicyAttachment(
    f"{eks_cluster_name}-ec2-container-ro-policy-attachment",
    role=ec2_role.id,
    policy_arn='arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly',
)
