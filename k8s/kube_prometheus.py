from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts,Release
from pulumi import Config
import pulumi_kubernetes as k8s
import pulumi
from pulumi import ResourceOptions
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs




def deploy(): 
    config=Config()
    region=config.require("region")
    acm_cert_arn=config.require("acm_cert_arn")
    use_pulumi_release=config.require_bool("use_pulumi_release")

    if use_pulumi_release:
        print('do thing')
        prom_release = Release(
            "prometheus-release",
            namespace="monitoring",
            chart="kube-prometheus-stack",
            version="20.0.1",
            repository_opts=RepositoryOptsArgs(
                repo="https://prometheus-community.github.io/helm-charts"
            ),
            cleanup_on_fail=True,
            create_namespace=True,
            disable_crd_hooks=False,
            disable_webhooks=False,
            force_update=False,
            recreate_pods=True,
            reuse_values=True,
            values={
                "grafana" : {
                    "service" : {
                        "enabled" : True,
                        "port" : "443",
                        "type" : "LoadBalancer",
                        "annotations": {
                            "service.beta.kubernetes.io/aws-load-balancer-backend-protocol" : "http",
                            "service.beta.kubernetes.io/aws-load-balancer-ssl-cert" : f"{acm_cert_arn}",
                            "service.beta.kubernetes.io/aws-load-balancer-ssl-ports" : "443",
                            "external-dns.alpha.kubernetes.io/hostname" : f"grafana-{region}.web.scoady.io",
                            "service.beta.kubernetes.io/aws-load-balancer-type" : "nlb"                 
                        }
                    }
                },
                "prometheus" : {
                    "prometheusSpec" : {
                        "storageSpec" : {
                            "volumeClaimTemplate" : {
                                "spec" : {
                                    "storageClassName" : "ebs-sc",
                                    "accessModes" : ["ReadWriteOnce"],
                                    "resources" : {
                                        "requests" : {
                                            "storage" : "150Gi"
                                        }
                                    },
                                }
                            }
                        },
                        "prometheusExternalLabelName" : f"prometheus-{region}-cluster"
                    },
                    "thanos": {
                        "image": "quay.io/thanos/thanos:v0.23.1",
                        "objectStorageConfig": {
                            "name": "thanos-objstore-config",
                            "key": "thanos.yaml",
                        },
                    "externalLabels": { 
                        "cluster": "thanos-operator-test",
                    }
                    },
                    "thanosService" : {
                        "enabled" : True
                    },
                    "externalLabels" : {
                        "cluster_name" : f"prometheus-{region}-cluster"
                    },
                    "replicaExternalLabelName" : {
                        "replica_cluster_name" : f"prometheus-{region}-cluster"
                    },
                    "externalUrl" : "prometheus-us-east-1.web.scoady.io",
                    "service" : {
                        "port" : "443",
                        "type" : "LoadBalancer",
                        "annotations": {
                            "service.beta.kubernetes.io/aws-load-balancer-backend-protocol" : "http",
                            "service.beta.kubernetes.io/aws-load-balancer-ssl-cert" : f"{acm_cert_arn}",
                            "service.beta.kubernetes.io/aws-load-balancer-ssl-ports" : "443",
                            "external-dns.alpha.kubernetes.io/hostname" : f"prometheus-{region}.web.scoady.io",
                            "service.beta.kubernetes.io/aws-load-balancer-type" : "nlb"                 
                        }
                }},
                "global" : {
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
    else:
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
                "global" : {
                            "prometheusExternalLabelName" : f"prometheus-{region}-cluster"
                    },
                "grafana" : {
                    "service" : {
                        "enabled" : True,
                        "port" : "443",
                        "type" : "LoadBalancer",
                        "annotations": {
                            "service.beta.kubernetes.io/aws-load-balancer-backend-protocol" : "http",
                            "service.beta.kubernetes.io/aws-load-balancer-ssl-cert" : f"{acm_cert_arn}",
                            "service.beta.kubernetes.io/aws-load-balancer-ssl-ports" : "443",
                            "external-dns.alpha.kubernetes.io/hostname" : f"grafana-{region}.web.scoady.io",
                            "service.beta.kubernetes.io/aws-load-balancer-type" : "nlb"                 
                        }
                    }
                },
                "prometheus" : {
                        "prometheusSpec": {
                            "storageSpec" : {
                                "volumeClaimTemplate" : {
                                    "spec" : {
                                        "storageClassName" : "csi-s3",
                                        "accessModes" : ["ReadWriteOnce"],
                                        "resources" : {
                                            "requests" : {
                                                "storage" : "50Gi"
                                            }
                                        },
                                        "selector" : {},
                                    }
                                }
                            },
                            "prometheusExternalLabelName" : f"prometheus-{region}-cluster"
                    },        
                    "thanos": {
                        "image": "quay.io/thanos/thanos",
                        "version": "v0.23.0",
                        "objectStorageConfig": {
                            "name": "thanos",
                            "key": "object-store.yaml",
                        },
                    "externalLabels": { 
                        "cluster": "thanos-operator-test",
                    }
                    },
                    "thanosService" : {
                        "enabled" : True
                    },
                    "externalLabels" : {
                        "cluster_name" : f"prometheus-{region}-cluster"
                    },
                    "replicaExternalLabelName" : {
                        "replica_cluster_name" : f"prometheus-{region}-cluster"
                    },
                    "externalUrl" : "prometheus.web.scoady.io",
                    "service" : {
                        "port" : "443",
                        "type" : "LoadBalancer",
                        "annotations": {
                            "service.beta.kubernetes.io/aws-load-balancer-backend-protocol" : "http",
                            "service.beta.kubernetes.io/aws-load-balancer-ssl-cert" : f"{acm_cert_arn}",
                            "service.beta.kubernetes.io/aws-load-balancer-ssl-ports" : "443",
                            "external-dns.alpha.kubernetes.io/hostname" : f"prometheus-{region}.web.scoady.io",
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


