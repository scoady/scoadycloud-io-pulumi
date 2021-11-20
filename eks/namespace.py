from pulumi_kubernetes.core.v1 import Namespace
import pulumi

def create_namespace(namespace_name) -> Namespace:
    """
    Create a namespace with recommended labels in EKS cluster
    """
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
