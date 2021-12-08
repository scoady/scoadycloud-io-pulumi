import pulumi
import pulumi_newrelic as newrelic
import synthetic_tests,alertchannel,alertcondition


synthetic_tests.create()
# Optional for type "SIMPLE" and "BROWSER"
alertchannel.create()

