from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s
import pulumi,helm_utils
from pulumi import ResourceOptions


def deploy():
    print('hello')
    nginx_deploy = Chart(
    "nginx-helm",
    ChartOpts(
        namespace="app",
        repo="nginx-stable",
        version="0.11.3",
        chart="nginx-ingress",
        transformations=[helm_utils.remove_status],
        fetch_opts=FetchOpts(
            repo = "https://helm.nginx.com/stable"
        ),
        values={
            "controller": {
                "service" : {
                    "annotations" : {
                        "service.beta.kubernetes.io/aws-load-balancer-ssl-cert" :  "arn:aws:acm:us-east-1:662892719773:certificate/b2fda0a4-f564-42a3-b5d5-a7c33369ee68",
                        "service.beta.kubernetes.io/aws-load-balancer-backend-protocol" : "http",
                        "service.beta.kubernetes.io/aws-load-balancer-ssl-ports" : "https",
                        "service.beta.kubernetes.io/aws-load-balancer-ssl-negotiation-policy": "ELBSecurityPolicy-TLS-1-2-2017-01",
                        "external-dns.alpha.kubernetes.io/hostname": "nginx.web.scoady.io,tinyurl.web.scoady.io"
                    }
                },
                "publishService" : {
                    "enabled" : True
                }
            }    
        
        }
    ))
