
import json
import pulumi
import pulumi_aws
import pulumi_kubernetes as k8s
from pulumi import Config
import utils


def create_k8s_provider():
    config = Config()
    eks_cluster_name = config.require("cluster_name")
    cluster_name = pulumi.Output.all(pulumi_aws.eks.Cluster(eks_cluster_name)).apply(lambda args: args[0].name)
    k8s_provider_deployment = k8s.Provider(f"{cluster_name}-provider",
        kubeconfig=utils.generate_kube_config(eks_cluster_name)
    )
    return k8s_provider_deployment


#def get_k8s_provider():
#    config = Config()
#    eks_cluster_name = config.require("cluster_name")
#    cluster = pulumi_aws.eks.get_cluster(
#        name=f"{eks_cluster_name}"
#    )
#    k8s_provider_deployment = k8s.Provider(f"{cluster.name}-provider",
#        kubeconfig=utils.generate_kube_config(cluster)
#    )
#    return k8s_provider_deployment
