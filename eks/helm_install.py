from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s
import os


def deploy_newrelic_agent():
    config = Config()
    newrelic_px_api_key=config.require("newrelic_px_api_key")
    newrelic_px_deploy_key=config.require("newrelic_px_deploy_key")
    newrelic_license=config.require("newrelic_license")
    newrelic_logging_key=config.require("newrelic_logging_key")
    aws_access_key=config.require("aws_access_key")
    aws_secret_key=config.require("aws_secret_key")
    custom_crds=config.require_object("custom_crds")
    newrelic_cluster_name=config.require("cluster_name")

    for custom_crd in custom_crds:
        crds = k8s.yaml.ConfigFile(
            f"{custom_crd}",
            file=f"{custom_crd}",
            transformations=[remove_status]
        )

    ebs_csi_driver = Chart(
        "aws-ebs-csi-driver",
        ChartOpts(
            namespace="kube-system",
            chart="aws-ebs-csi-driver",
            version="2.4.0",
            fetch_opts=FetchOpts(
                repo="https://kubernetes-sigs.github.io/aws-ebs-csi-driver"
            )
        )
    )
    newrelic_agent = Chart(
        "newrelic-nri-bundle",
        ChartOpts(
            namespace="newrelic",
            chart="nri-bundle",
            version="3.2.9",
            fetch_opts=FetchOpts(
                repo="https://helm-charts.newrelic.com/",
            ),
            values={
                "global" : {
                    "licenseKey" : f"{newrelic_license}",
                    "cluster": f"{newrelic_cluster_name}",
                    "lowDataMode": "true",
                },
                "newrelic-infrastructure": {
                    "privileged" : "true"
                },
                "ksm" : {
                    "enabled" : "true"
                },
                "prometheus": {
                    "enabled" : "true"
                },
                "kubeEvents" : {
                    "enabled" : "true"
                },
                "logging": {
                    "enabled" : "true"
                },
                "newrelic-pixie" : {
                    "enabled" : "false",
                    "apiKey" : f"{newrelic_px_api_key}" ## encrypted secret 
                },
                "pixie-chart" : {
                    "enabled" : "false",
                    "deployKey" : f"{newrelic_px_deploy_key}", ## encrypted secret
                    "clusterName" : f"{newrelic_cluster_name}"
                }
            }
        ),
    )

    newrelic_logging_agent = Chart(
        "newrelic-logging",
        ChartOpts(
            namespace="newrelic",
            chart="newrelic-logging",
            version="1.10.4",
            fetch_opts=FetchOpts(
                repo="https://helm-charts.newrelic.com/",
            ),
            values={
                "licenseKey" : f"{newrelic_logging_key}"
            }
        )
    )

    ebs_storageclass = k8s.yaml.ConfigFile(
        "ebs-sc-storageclass",
        file="./storageclass/ebs_sc_storageclass.yaml"
    )

    external_dns_deployment = Chart(
        "external-dns",
        ChartOpts(
            chart="external-dns",
            version="5.5.0",
            fetch_opts=FetchOpts(
                repo="https://charts.bitnami.com/bitnami"
            ),
            values = {
                "aws" : {
                    "credentials" : {
                        "accessKey" : f"{aws_access_key}",
                        "secretKey" : f"{aws_secret_key}"
                    },
                    "preferCNAME" : "true"
                },
                "rbac" : {
                    "create" : "true"
                },
                "policy" : "upsert-only",
                "txtPrefix": "autogen"
            }
        )
    )

# Remove the .status field from CRDs
def remove_status(obj, opts):
    if obj["kind"] == "CustomResourceDefinition":
        obj.pop("status",None)
