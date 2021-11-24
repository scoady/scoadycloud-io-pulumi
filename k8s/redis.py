from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s
import pulumi,helm_utils
from pulumi import ResourceOptions

def deploy():
    print("Hello")
    redis_deploy = Chart(
            "redis-helm",
            ChartOpts(
                namespace="app",
                repo="bitnami",
                version="15.5.5",
                chart="redis",
                transformations=[helm_utils.remove_status],
                fetch_opts=FetchOpts(
                    repo = "https://charts.bitnami.com/bitnami"
                ),
                values={
                    "global" : {
                    "auth" : {
                        "enabled" : False
                    }
                
                }
            ))
