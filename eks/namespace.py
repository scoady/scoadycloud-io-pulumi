from pulumi_kubernetes.core.v1 import Namespace
import pulumi_kubernetes as k8s
import pulumi
from pulumi import Config,Output
import config as config_util
import utils

def create_namespace(namespace_name) -> Namespace:
    """
    Create a namespace with recommended labels in EKS cluster
    """
    config = Config()
    eks_cluster_name = config.require("cluster_name")
    labels = {
        "name": namespace_name,
    }
    namespace = Namespace(
        f"{namespace_name}",
        metadata={
            "name": namespace_name,
            "labels": labels,
        },
        opts=pulumi.ResourceOptions(
            delete_before_replace=True,
        ),
    )
    return namespace
