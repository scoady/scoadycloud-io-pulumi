from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s
import pulumi,helm_utils
from pulumi import ResourceOptions



def deploy():
    print("hello")
    kafka_deploy = Chart(
    "kafka-helm",
    ChartOpts(
        namespace="app",
        repo="bitnami",
        version="14.4.1",
        chart="kafka",
        transformations=[helm_utils.remove_status],
        fetch_opts=FetchOpts(
            repo = "https://charts.bitnami.com/bitnami"
        ),
        values={
            "metrics" : {
                "kafka" : {
                    "enabled" : True
                }
            }
        }
    ))
