import pulumi
import pulumi_newrelic as newrelic
from pulumi import Config,export


def create():
    config = Config()
    email_addr=config.require("email")
    slack_channel=config.require("slack")
    email_alert = newrelic.AlertChannel(f"{email_addr}-alert",
        name=f"{email_addr}-channel",
        config=newrelic.AlertChannelConfigArgs(
            include_json_attachment="true",
            recipients=f"{email_addr}",
        ),
        type="email")
    export(f"{email_addr}-channel",email_alert)

    slack_alert = newrelic.AlertChannel(f"{slack_channel}-alerts",
    name=f"{slack_channel}-slack",
     config=newrelic.AlertChannelConfigArgs(
        channel="newrelic",
        url="https://hooks.slack.com/services/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",
    ),
    type="slack")
    export(f"{slack_channel}-alerts",slack_alert)

