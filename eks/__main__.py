import iam
from namespace import create_namespace
import helm_install
import vpc
import utils
import config as config_util
import external_dns
import pulumi
import pulumi_kubernetes as k8s
from pulumi_aws import eks
from pulumi import Config,Output

## EKS Cluster
config = Config()
eks_cluster_name = config.require("cluster_name")
skip_validation = config.require("skip_initial_validation")

eks_cluster = eks.Cluster(
    f"{eks_cluster_name}-cluster",
    name=f"{eks_cluster_name}",
    role_arn=iam.eks_role.arn,
    tags={
        'Name': f"{eks_cluster_name}",
    },
    vpc_config=eks.ClusterVpcConfigArgs(
        public_access_cidrs=['0.0.0.0/0'],
        security_group_ids=[vpc.eks_security_group.id],
        subnet_ids=vpc.subnet_ids[:3],
    ),
)

eks_node_group = eks.NodeGroup(
    f"{eks_cluster_name}-eks-node-group",
    cluster_name=eks_cluster.name,
    node_group_name=f"{eks_cluster_name}-pulumi-eks-nodegroup",
    node_role_arn=iam.ec2_role.arn,
    subnet_ids=vpc.subnet_ids[:3],
    tags={
        'Name': f"{eks_cluster_name}-pulumi-cluster-nodeGroup",
    },
    scaling_config=eks.NodeGroupScalingConfigArgs(
        desired_size=config.require_int("desired_node_pool_size"),
        max_size=config.require_int("max_node_pool_size"),
        min_size=config.require_int("min_node_pool_size"),
    ),
)
if skip_validation == "true":
    print("Not installing namespace or agents. Please set config option skip_initial_validation: false to install agents.")
else:
    if config.get('install_helm_charts') == "true":
        namespace=create_namespace('newrelic')
        helm_install.deploy_newrelic_agent()

pulumi.export('cluster-name', eks_cluster.name)
pulumi.export('kubeconfig', utils.generate_kube_config(eks_cluster))
