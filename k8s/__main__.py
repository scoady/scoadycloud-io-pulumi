import kube_prometheus
from pulumi import Config



config=Config()
deploy_prometheus=config.require_bool("deploy_prometheus")

if deploy_prometheus:
    kube_prometheus.deploy()
