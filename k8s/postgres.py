from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s
import pulumi,helm_utils
from pulumi import ResourceOptions


def deploy():
    print("hello")
    config=Config()
    region=config.require("region")

    postgres_deploy = Chart(
    "postgres-helm",
    ChartOpts(
        namespace="app",
        repo="stable",
        version="10.13.8",
        chart="postgresql",
        transformations=[helm_utils.remove_status],
        fetch_opts=FetchOpts(
            repo = "https://charts.bitnami.com/bitnami"
        ),
        values={
            "global" : {
                "postgresql" : {
                    "postgresqlDatabase" : "tinyurl",
                },
                "storageClass" : "ebs-sc",
            },
            "replication" : {
                "enabled" : True,
                "slaveReplicas" : 2
            }
        
        }
    ))
