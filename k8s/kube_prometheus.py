from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s
import pulumi
from pulumi import ResourceOptions




def deploy(): 
    config=Config()
    grafana_admin_password=config.require("grafana_admin_pass")
    grafana_admin_user=config.require("grafana_admin_user")
    prom_helm = Chart(
    "prometheus-community",
    ChartOpts(
        namespace="monitoring",
        repo="prometheus-community",
        version="19.2.3",
        chart="kube-prometheus-stack",
        transformations=[remove_status],
        fetch_opts=FetchOpts(
            repo = "https://prometheus-community.github.io/helm-charts"
        ),
        values={
            "grafana" : {
                "service" : {
                    "enabled" : True,
                    "port" : "443",
                    "type" : "LoadBalancer",
                    "annotations": {
                        "service.beta.kubernetes.io/aws-load-balancer-backend-protocol" : "http",
                        "service.beta.kubernetes.io/aws-load-balancer-ssl-cert" : "arn:aws:acm:us-west-1:662892719773:certificate/fb18919a-b4d7-412c-969b-e7350dffe12c",
                        "service.beta.kubernetes.io/aws-load-balancer-ssl-ports" : "443",
                        "external-dns.alpha.kubernetes.io/hostname" : "grafana.web.scoady.io",
                        "service.beta.kubernetes.io/aws-load-balancer-type" : "nlb"                 
                    }
                  }
            },
            "prometheus" : {
            "externalUrl" : "prometheus.web.scoady.io",
            "service" : {
                "port" : "443",
                "type" : "LoadBalancer",
                "annotations": {
                    "service.beta.kubernetes.io/aws-load-balancer-backend-protocol" : "http",
                    "service.beta.kubernetes.io/aws-load-balancer-ssl-cert" : "arn:aws:acm:us-west-1:662892719773:certificate/fb18919a-b4d7-412c-969b-e7350dffe12c",
                    "service.beta.kubernetes.io/aws-load-balancer-ssl-ports" : "443",
                    "external-dns.alpha.kubernetes.io/hostname" : "prometheus.web.scoady.io",
                    "service.beta.kubernetes.io/aws-load-balancer-type" : "nlb"                 
                }
            }
            },
            "defaultRules" : {
                "rules" : {
                    "kubeScheduler" : False,
                    "kubeEtcd" : False,
                }
            },
            "kubeControllerManager" : {
                "enabled" : False,
                "service" : {
                    "enabled" : False
                },
                "serviceMonitor" : {
                    "enabled" : False
                }
            },
            "kubeEtcd": { 
                "enabled" : False,
                "service" : {
                    "enabled" : False
                },
                "serviceMonitor" : {
                    "enabled" : False
                }
            },
            "kubeScheduler" : {
                "enabled": False,
                "service" : {
                    "enabled" : False
                },
                "serviceMonitor" : {
                    "enabled" : False
                }
            }
        }
        )
    )



# Remove the .status field from CRDs
def remove_status(obj, opts):
    if obj["kind"] == "CustomResourceDefinition":
        del obj["status"]
