import pulumi
import pulumi_newrelic as newrelic


def create():
    grafana_healthcheck = newrelic.synthetics.Monitor("grafana-synthetic-frontdoor-monitor",
        name="grafana-synthetic-frontdor-monitor",
        frequency=5,
        locations=[
            "AWS_US_EAST_1",
            "AWS_US_EAST_2",
        ],
        status="ENABLED",
        type="SIMPLE",
        uri="https://grafana.web.scoady.io/healthz",
        validation_string="Ok",
        verify_ssl=True)
    # Optional for type "SIMPLE" and "BROWSER"

    prometheus_healthcheck = newrelic.synthetics.Monitor("prometheus-synthetic-frontdoor-monitor",
        name="prometheus-synthetic-frontdoor-monitor",
        frequency=5,
        locations=[
            "AWS_US_EAST_1",
            "AWS_US_EAST_2",
        ],
        status="ENABLED",
        type="SIMPLE",
        uri="https://prometheus.web.scoady.io/-/healthy",
        validation_string="Prometheus is Healthy.",
        verify_ssl=True)
    # Optional for type "SIMPLE" and "BROWSER"
