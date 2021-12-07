import pulumi
import pulumi_newrelic as newrelic
from pulumi import Config,export

def create():
    config=Config()
    synthetic_checks=config.require_object('checks')
    for synthetic_check in synthetic_checks:
        check = newrelic.synthetics.Monitor(f"{synthetic_check['name']}",
            name=f"{synthetic_check['name']}-monitor",
            frequency=5,
            locations=[
                "AWS_US_EAST_1",
                "AWS_US_EAST_2",
            ],
            status="ENABLED",
            type="SIMPLE",
            uri=f"{synthetic_check['endpoint']}",
            validation_string=f"{synthetic_check['validation_string']}",
            verify_ssl=True)
        export(f"{synthetic_check['name']}",check)

