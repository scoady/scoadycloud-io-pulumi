from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts
from pulumi import Config


def deploy_newrelic_agent():
    config = Config()
    newrelic_px_api_key=config.require("newrelic_px_api_key")
    newrelic_px_deploy_key=config.require("newrelic_px_deploy_key")
    newrelic_license=config.require("newrelic_license")
    newrelic_logging_key=config.require("newrelic_logging_key")
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
                    "cluster": "scoadycloud-io-prod",
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
                    "enabled" : "true",
                    "apiKey" : f"{newrelic_px_api_key}" ## encrypted secret 
                },
                "pixie-chart" : {
                    "enabled" : "true",
                    "deployKey" : f"{newrelic_px_deploy_key}", ## encrypted secret
                    "clusterName" : "scoadycloud-io-prod"
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
