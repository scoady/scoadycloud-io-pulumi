import pulumi
import pulumi_kubernetes as kubernetes


def deploy_dns():
    external_dns_deployment = kubernetes.apps.v1.Deployment("external_dnsDeployment",
        api_version="apps/v1",
        kind="Deployment",
        metadata=kubernetes.meta.v1.ObjectMetaArgs(
            name="external-dns",
        ),
        spec=kubernetes.apps.v1.DeploymentSpecArgs(
            strategy=kubernetes.apps.v1.DeploymentStrategyArgs(
                type="Recreate",
            ),
            selector=kubernetes.meta.v1.LabelSelectorArgs(
                match_labels={
                    "app": "external-dns",
                },
            ),
            template=kubernetes.core.v1.PodTemplateSpecArgs(
                metadata=kubernetes.meta.v1.ObjectMetaArgs(
                    labels={
                        "app": "external-dns",
                    },
                    annotations={
                        "iam.amazonaws.com/role": "arn:aws:iam::662892719773:policy/EBS_CSI_DRIVER",
                    },
                ),
                spec=kubernetes.core.v1.PodSpecArgs(
                    containers=[kubernetes.core.v1.ContainerArgs(
                        name="external-dns",
                        image="k8s.gcr.io/external-dns/external-dns:v0.7.6",
                        args=[
                            "--source=service",
                            "--source=ingress",
                            "--provider=aws",
                            "--policy=upsert-only",
                            "--aws-zone-type=public",
                            "--registry=txt",
                            "--txt-owner-id=Z01930422MQG2NM2HLW7",
                        ],
                    )],
                ),
            ),
        ))


