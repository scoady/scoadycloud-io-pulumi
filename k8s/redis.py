from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s
import pulumi,helm_utils
from pulumi import ResourceOptions
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs

def deploy():
    print("Hello")
    redis_deploy = Release(
            "redis-helm",
                name="redis-helm",
                namespace="app",
                version="15.5.5",
                chart="redis",
                repository_opts=RepositoryOptsArgs(
                    repo = "https://charts.bitnami.com/bitnami"
                ),
                cleanup_on_fail=True,
                create_namespace=True,
                disable_crd_hooks=False,
                disable_webhooks=False,
                disable_openapi_validation=True,
                recreate_pods=True,
                verify=False,
                reset_values=True,
                keyring="",
                atomic=True,
                values={
                    "auth" : {
                        "password": "thisisatest"
                    },
                    "metrics" : {
                        "podAnnotations" : {
                            "prometheus.io/scrape" : "true",
                            "prometheus.io/port" : "9121"
                        },
                        "enabled" : True,
                        "serviceMonitor" : {
                            "enabled" : False
                        },
                    },
                    "usePassword" : False,
                    "global" : {
                        "usePassword" : False,
                        "auth" : {
                            "enabled" : False
                        }
                    }
                }
    )
