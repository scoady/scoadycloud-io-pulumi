import pulumi
import pulumi_newrelic as newrelic
from pulumi import Config

def create():
    app = newrelic.get_entity(name="tinyurl-web-monitor",
        ignore_case=True,
        domain="SYNTH"
    )
    config=Config()
    foo_alert_policy = newrelic.AlertPolicy("fooAlertPolicy")
    foo_alert_condition = newrelic.AlertCondition("fooAlertCondition",
        policy_id=1744243,
        type="apm_app_metric",
        entities=[app.application_id],
        metric="user_defined",
        runbook_url="https://www.example.com",
        condition_scope="application",
        terms=[newrelic.AlertConditionTermArgs(
            duration=5,
            operator="abpve",
            priority="critical",
            threshold=1,
            time_function="all",
        )])
