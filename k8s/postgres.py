from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s
import pulumi,helm_utils
from pulumi import ResourceOptions
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs

def deploy():
    print("hello")
    config=Config()
    region=config.require("region")

    postgres_deploy = Release(
    "postgres-helm",
        name="postgres-helm",
        namespace="app",
        version="10.13.8",
        chart="postgresql",
        repository_opts=RepositoryOptsArgs(
            repo = "https://charts.bitnami.com/bitnami"
        ),
        cleanup_on_fail=True,
        create_namespace=True,
        disable_crd_hooks=False,
        disable_webhooks=False,
        force_update=True,
        disable_openapi_validation=True,
        recreate_pods=True,
        atomic=True,
        replace=True,
        values={
        "service" : {
            "annotations" : {
                "prometheus.io/scrape" : "true",
            }
        },
        "postgresqlDatabase" : "tinyurl",
        "postgresqlPassword" : "password",
        "postgressqlUsername" : "scoady",
        "metrics" : {
            "annotations" : {
                "prometheus.io/scrape" : "true",
                "prometheus.io/port" : "9188"
            },
            "enabled" : True,
            "serviceMonitor" : {
                "enabled" : False,
            },
            "global" : {
                "postgresql" : {
                    "postgresqlDatabase" : "tinyurl",
                    "postgresqlUsername" : "scoady",
                    "postgresqlPassword" : "password"
                },
                "storageClass" : "ebs-sc",
            },
            "replication" : {
                "enabled" : False,
            }
        
        }
        }
    )
