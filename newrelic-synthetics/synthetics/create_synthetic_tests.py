import pulumi
import pulumi_newrelic as newrelic


def create():
    foo = newrelic.synthetics.Monitor("scoady-test-monitor",
        name="scoady-test-monitor",
        frequency=5,
        locations=[
            "AWS_US_EAST_1",
            "AWS_US_EAST_2",
        ],
        status="ENABLED",
        type="SIMPLE",
        uri="https://nginx.web.scoady.io",
        validation_string="Welcome to nginx!",
        verify_ssl=True)
    # Optional for type "SIMPLE" and "BROWSER"
