from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s
import pulumi
from pulumi import ResourceOptions




def deploy(): 
    config=Config()
    crds = k8s.yaml.ConfigFile(
        "prom-crds",
         file="./prom.yaml",
         transformations=[remove_status]
    )
    jenkins_helm = Chart(
    "kube-prometheus",
    ChartOpts(
        namespace="",
        chart="kube-prometheus-stack",
        version="20.0.1",
        fetch_opts=FetchOpts(
            repo="https://prometheus-community.github.io/helm-charts",

        ),
        transformations=[remove_status],
        ),
        opts=ResourceOptions(depends_on=[crds])
    )



# Remove the .status field from CRDs
def remove_status(obj, opts):
    if obj["kind"] == "CustomResourceDefinition":
        del obj["status"]
        del obj["metadata"]["annotations"]
