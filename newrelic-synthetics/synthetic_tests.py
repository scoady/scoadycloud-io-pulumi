import pulumi
import pulumi_newrelic as newrelic


def create():
    us_east_hc = newrelic.synthetics.Monitor("tinyurl-us-east-1-frontdoor-monitor",
        name="tinyurl-us-east-1-synthetic-frontdor-monitor",
        frequency=5,
        locations=[
            "AWS_US_EAST_1",
            "AWS_US_EAST_2",
        ],
        status="ENABLED",
        type="SIMPLE",
        uri="https://tinyurl-us-west-1.web.scoady.io/healthz",
        validation_string="Ok",
        verify_ssl=True)
    # Optional for type "SIMPLE" and "BROWSER"

    us_west_hc = newrelic.synthetics.Monitor("tinyurl-us-west-1-synthetic-frontdoor-monitor",
        name="tinyurl-us-west-1-synthetic-frontdoor-monitor",
        frequency=5,
        locations=[
            "AWS_US_EAST_1",
            "AWS_US_EAST_2",
        ],
        status="ENABLED",
        type="SIMPLE",
        uri="https://tinyurl-us-west-1.web.scoady.io/-/healthy",
        validation_string="Ok",
        verify_ssl=True)
    # Optional for type "SIMPLE" and "BROWSER"
