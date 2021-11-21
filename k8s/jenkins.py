from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s



def deploy(): 
    config=Config()
    jenkins_helm = Chart(
    "jenkins",
    ChartOpts(
        namespace="",
        chart="jenkins",
        version="3.8.8",
        fetch_opts=FetchOpts(
            repo="https://charts.jenkins.io"
        ),
        values = {   
            "controller" : {
                "ingress" : {
                    "enabled" : "true",
                    "apiVersion" : "networking.k8s.io/v1beta1",
                    "hostname" : "jenkins.web.scoady.io"
                },
                "serviceType" : "LoadBalancer",
                "servicePort" : "443",
                "serviceAnnotations" : {
                    "service.beta.kubernetes.io/aws-load-balancer-type" : "nlb",
                    "external-dns.alpha.kubernetes.io/hostname" : "jenkins.web.scoady.io",
                    "service.beta.kubernetes.io/aws-load-balancer-ssl-cert" : "arn:aws:acm:us-west-1:662892719773:certificate/fb18919a-b4d7-412c-969b-e7350dffe12c",
                    "service.beta.kubernetes.io/aws-load-balancer-ssl-ports" : "443"
                },
                "extraPorts" : [{
                    "name" : "master",
                    "port" : "8080"
                }],
                "serviceLabels" : {
                    "expose" : "true",
                    "test": "key"
                },
                "jenkinsUrl" : "https://jenkins.web.scoady.io",
                "jenkinsAdminEmail" : "scoady@scoady.io",
                "JSaC" : {
                    "securityRealm" : {
                        "local" : {
                            "allowsSignup" : "false",
                            "enableCaptcha" : "false",
                            "users" : [{
                                "id" : "scoady",
                                "name" : "scoady",
                                "password" : "Sc2016csc!"
                            }]
                        }
                    }
                }
            },
            
        }
    )
)
