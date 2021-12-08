from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config
import pulumi_kubernetes as k8s
import os,base64
from pulumi_kubernetes.core.v1 import ContainerArgs, ContainerPortArgs, PodSpecArgs, PodTemplateSpecArgs, VolumeArgs,ConfigMapVolumeSourceArgs
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs


def deploy_newrelic_agent():
    config = Config()
    newrelic_px_api_key=config.require("newrelic_px_api_key")
    newrelic_px_deploy_key=config.require("newrelic_px_deploy_key")
    newrelic_license=config.require("newrelic_license")
    newrelic_logging_key=config.require("newrelic_logging_key")
    aws_access_key=config.require("aws_access_key")
    aws_secret_key=config.require("aws_secret_key")
    custom_crds=config.get_object("custom_crds")
    newrelic_cluster_name=config.require("cluster_name")
    deploy_s3_operator=config.require("s3_operator")
    install_newrelic=config.get('install_newrelic')

    if custom_crds is not None: 
        for custom_crd in custom_crds:
            crds = k8s.yaml.ConfigFile(
                f"{custom_crd}",
                file=f"{custom_crd}",
                transformations=[remove_status]
            )
    s3_provisioner = k8s.yaml.ConfigFile(
        "s3-provisioner",
        file="https://raw.githubusercontent.com/ctrox/csi-s3/master/deploy/kubernetes/provisioner.yaml"
    )
    s3_attacher = k8s.yaml.ConfigFile(
        "s3-attacher",
        file="https://raw.githubusercontent.com/ctrox/csi-s3/master/deploy/kubernetes/attacher.yaml"
    )
    csi_s3 = k8s.yaml.ConfigFile(
        "csi-s3",
        file="https://raw.githubusercontent.com/ctrox/csi-s3/master/deploy/kubernetes/csi-s3.yaml"
    )
    s3_storageclass_csi = k8s.yaml.ConfigFile(
        "s3-storageclass-csi",
        file="https://raw.githubusercontent.com/ctrox/csi-s3/master/deploy/kubernetes/examples/storageclass.yaml"
    )


    ebs_csi_driver = Release(
        "aws-ebs-csi-driver",
            name="aws-ebs-csi-driver",
            namespace="kube-system",
            chart="aws-ebs-csi-driver",
            version="2.4.0",
            repository_opts=RepositoryOptsArgs(
                repo="https://kubernetes-sigs.github.io/aws-ebs-csi-driver"
            ),
            cleanup_on_fail=True,
            create_namespace=True,
            disable_crd_hooks=False,
            disable_webhooks=False,
            disable_openapi_validation=True,
            recreate_pods=True,
            reset_values=True,
            atomic=True,
            verify=False,
            keyring="",
            values={}
    )
    if install_newrelic is not None:
        newrelic_agent = Release(
            "newrelic-nri-bundle",
                dependency_update=True,
                name="newrelic-nri-bundle",
                namespace="newrelic",
                chart="nri-bundle",
                version="3.2.9",
                repository_opts=RepositoryOptsArgs(
                    repo="https://helm-charts.newrelic.com/",
                ),
                cleanup_on_fail=True,
                create_namespace=True,
                disable_crd_hooks=False,
                disable_webhooks=False,
                recreate_pods=True,
                reset_values=True,
                skip_crds=True,
                verify=False,
                atomic=True,
                keyring="",
		        timeout=600,
                disable_openapi_validation=True,
                values={
                    "global" : {
                        "licenseKey" : f"{newrelic_license}",
                        "cluster": f"{newrelic_cluster_name}",
                        "lowDataMode": True,
                    },
                    "newrelic-infrastructure": {
                        "privileged" : True,
                    },
                    "ksm" : {
                        "enabled" : True,
                    },
                    "prometheus": {
                        "enabled" : True,
                        "scrape_endpoints" : True,
                        "scrape_services" : False,
                    },
                    "kubeEvents" : {
                        "enabled" : True,
                    },
                    "logging": {
                        "enabled" : True,
                    },
                    "newrelic-pixie" : {
                        "enabled" : True,
                        "apiKey" : f"{newrelic_px_api_key}" ## encrypted secret 
                    },
                    "pixie-chart" : {
                        "enabled" : True,
                        "deployKey" : f"{newrelic_px_deploy_key}", ## encrypted secret
                        "clusterName" : f"{newrelic_cluster_name}"
                    }
                }
        )

        newrelic_logging_agent = Release(
            "newrelic-logging",
                dependency_update=True,
                name="newrelic-logging",
                namespace="newrelic",
                chart="newrelic-logging",
                version="1.10.4",
                disable_openapi_validation=True,
                skip_crds=True,
                verify=False,
                reset_values=True,
                keyring="",
                atomic=True,
		timeout=600,
                repository_opts=RepositoryOptsArgs(
                    repo="https://helm-charts.newrelic.com/",
                ),
                values={
                    "licenseKey" : f"{newrelic_logging_key}"
                }
        )

    ebs_storageclass = k8s.yaml.ConfigFile(
        "ebs-sc-storageclass",
        file="./storageclass/ebs_sc_storageclass.yaml"
    )

    external_dns_deployment = Release(
        "external-dns",
            dependency_update=True,
            chart="external-dns",
            name="external-dns",
            version="5.5.0",
            verify=False,
            reset_values=True,
            keyring="",
            repository_opts=RepositoryOptsArgs(
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







# Remove the .status field from CRDs
def remove_status(obj, opts):
    if obj["kind"] == "CustomResourceDefinition":
        obj.pop("status",None)
