import pulumi
from pulumi import Config
import pulumi
import pulumi_aws as aws

## EKS Cluster
config = Config()
csr_cn=config.require("certificate_cn")


cert = aws.acm.Certificate(f"*.{csr_cn}",
    domain_name=f"*.{csr_cn}",
    tags={
        "cn": f"{csr_cn}",
    },
    validation_method="DNS")
