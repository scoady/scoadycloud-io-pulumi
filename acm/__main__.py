import pulumi
from pulumi import Config,export
import pulumi
import pulumi_aws as aws

## EKS Cluster
config = Config()
domains=config.require_object("certificates")


for domain in domains:
    cert = aws.acm.Certificate(f"{domain}",
        domain_name=f"{domain}",
        tags={
            "cn": f"{domain}".strip("*")
        },
        validation_method="DNS")
    certDetails={
        "cn" : cert.domain_name,
        "id" : cert.id
    }
    export(f"{domain}-cert",certDetails)
