import json
from pulumi import export, get_stack, Config, Output
import pulumi_aws

stack = get_stack()
config = Config()
database_name = config.require('db_name')
username = config.require("username")
password = config.require("password")

# Create a Postgres RDS DB.

subnet_ids = pulumi_aws.ec2.get_subnet_ids(vpc_id="vpc-04cf7c8f33611774f")
rds_instance = pulumi_aws.rds.Instance(
    f"{get_stack()}-rds",
    pulumi_aws.rds.InstanceArgs(
        name=f"{database_name}",
        engine="postgres",
        engine_version="13.4",
        instance_class="db.m5.large",
        allocated_storage=50,
        username=f"{username}",
        password=f"{password}"
    ),
)

# Create the RDS connection string.
# Note, because the password is already marked as secret, the secretness will
# persist downstream to any dependent users, and will mark the db_uri as a
# secret in the statefile, Outputs, and for any dependent callers.


postgres_uri = Output.all(rds_instance.endpoint).apply(
    lambda args: f"postgres://{args[0]}"
)

export("postgresEndpoint", rds_instance.endpoint)
export("postgresConnectString", postgres_uri)
export("PGDATABASE", database_name)
export("PGHOST", rds_instance.endpoint.apply(lambda s: s.split(":")[0]))

