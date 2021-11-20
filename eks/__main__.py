import iam
from namespace import create_namespace
import helm_install
import vpc
import utils
import install_agents
import pulumi
from pulumi_aws import eks
from pulumi import Config

## EKS Cluster
config = Config()
eks_cluster_name = config.require("cluster_name")
eks_cluster = eks.Cluster(
    f"{eks_cluster_name}-cluster",
    role_arn=iam.eks_role.arn,
    tags={
        'Name': f"{eks_cluster_name}",
    },
    vpc_config=eks.ClusterVpcConfigArgs(
        public_access_cidrs=['0.0.0.0/0'],
        security_group_ids=[vpc.eks_security_group.id],
        subnet_ids=vpc.subnet_ids,
    ),
)

eks_node_group = eks.NodeGroup(
    f"{eks_cluster_name}-eks-node-group",
    cluster_name=eks_cluster.name,
    node_group_name=f"{eks_cluster_name}-pulumi-eks-nodegroup",
    node_role_arn=iam.ec2_role.arn,
    subnet_ids=vpc.subnet_ids,
    tags={
        'Name': f"{eks_cluster_name}-pulumi-cluster-nodeGroup",
    },
    scaling_config=eks.NodeGroupScalingConfigArgs(
        desired_size=2,
        max_size=2,
        min_size=1,
    ),
)

namespace=create_namespace('newrelic')
helm_install.deploy_newrelic_agent()

pulumi.export('cluster-name', eks_cluster.name)
pulumi.export('kubeconfig', utils.generate_kube_config(eks_cluster))
