import kube_prometheus,postgres,redis,kafka,nginx,tinyurl
from pulumi import Config




config=Config()
deploy_prometheus=config.require_bool("deploy_prometheus")
deploy_postgres=config.require_bool("deploy_postgres")
deploy_redis=config.require_bool("deploy_redis")
deploy_kafka=config.require_bool("deploy_kafka")
deploy_nginx=config.require_bool("deploy_nginx")
deploy_tinyurl=config.require_bool("deploy_tinyurl")

if deploy_prometheus:
    kube_prometheus.deploy()

if deploy_postgres:
    postgres.deploy()

if deploy_redis:
    redis.deploy()

if deploy_kafka:
    kafka.deploy()

if deploy_nginx:
    nginx.deploy()

if deploy_tinyurl:
    tinyurl.deploy()
