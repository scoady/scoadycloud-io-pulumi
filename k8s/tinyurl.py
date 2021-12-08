import pulumi
import pulumi_kubernetes as kubernetes
from pulumi import Config,export


def deploy():
    config=Config()
    acm_cert_arn=config.require("acm_cert_arn")
    region=config.require("region")
    app_tinyurl_deployment = kubernetes.apps.v1.Deployment("appTinyurlDeployment",
        api_version="apps/v1",
        kind="Deployment",
        metadata=kubernetes.meta.v1.ObjectMetaArgs(
            annotations={
                "kompose.cmd": "kompose convert",
                "kompose.version": "1.24.0 (4a2a0458)",
                "prometheus.io/scrape": "true",
            },
            labels={
                "io.kompose.service": "tinyurl",
            },
            name="tinyurl",
            namespace="app",
        ),
        spec=kubernetes.apps.v1.DeploymentSpecArgs(
            replicas=1,
            selector=kubernetes.meta.v1.LabelSelectorArgs(
                match_labels={
                    "io.kompose.service": "tinyurl",
                },
            ),
            strategy=kubernetes.apps.v1.DeploymentStrategyArgs(
                type="Recreate",
            ),
            template=kubernetes.core.v1.PodTemplateSpecArgs(
                metadata=kubernetes.meta.v1.ObjectMetaArgs(
                    annotations={
                        "kompose.cmd": "kompose convert",
                        "kompose.version": "1.24.0 (4a2a0458)",
                    },
                    labels={
                        "io.kompose.service": "tinyurl",
                    },
                ),
                spec=kubernetes.core.v1.PodSpecArgs(
                    containers=[
                        kubernetes.core.v1.ContainerArgs(
                            name="nginx-requests-exporter",
                            image="markuslindenberg/nginx_request_exporter",
                            ports=[
                                kubernetes.core.v1.ContainerPortArgs(
                                    name="metrics",
                                    container_port=9147,
                                    protocol="TCP",
                                ),
                                kubernetes.core.v1.ContainerPortArgs(
                                    name="udp-syslog",
                                    container_port=9514,
                                    protocol="UDP",
                                ),
                            ],
                            resources=kubernetes.core.v1.ResourceRequirementsArgs(),
                        ),
                        kubernetes.core.v1.ContainerArgs(
                            name="nginx-exporter",
                            image="nginx/nginx-prometheus-exporter",
                            args=["-nginx.scrape-uri=http://localhost/nginx_status"],
                            ports=[kubernetes.core.v1.ContainerPortArgs(
                                name="nginx-ex-port",
                                container_port=9113,
                                protocol="TCP",
                            )],
                            image_pull_policy="Always",
                            resources=kubernetes.core.v1.ResourceRequirementsArgs(),
                        ),
                        kubernetes.core.v1.ContainerArgs(
                            name="nginx",
                            image="nginx",
                            ports=[kubernetes.core.v1.ContainerPortArgs(
                                container_port=80,
                                protocol="TCP",
                                name="http",
                            )],
                            resources=kubernetes.core.v1.ResourceRequirementsArgs(),
                            volume_mounts=[
                                {
                                    "name": "nginx-cache-volume",
                                    "mount_path": "/srv/nginx/",
                                },
                                {
                                    "name": "nginx-config-volume",
                                    "mount_path": "/etc/nginx/nginx.conf",
                                    "sub_path": "nginx.conf",
                                },
                            ],
                        ),
                        kubernetes.core.v1.ContainerArgs(
                            image="662892719773.dkr.ecr.us-west-1.amazonaws.com/tinyurl:100",
                            name="tinyurl",
                            ports=[kubernetes.core.v1.ContainerPortArgs(
                                container_port=3000,
                            )],
                            env=[
                                kubernetes.core.v1.EnvVarArgs(
                                    name="PORT",
                                    value="3000",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="APP_ENV",
                                    value="dev",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="POSTGRES_USER",
                                    value="postgres",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="POSTGRES_PASSWORD",
                                    value="Pa6kBHRZCM",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="POSTGRES_DB",
                                    value="tinyurl",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="POSTGRES_HOST",
                                    value="postgres-helm-postgresql.app.svc.cluster.local",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="DATABASE_URL",
                                    value="postgres://postgres:password@postgres-helm-postgresql.app.svc.cluster.local:5432/tinyurl",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="REDIS_URL",
                                    value="redis://redis-helm-master.app.svc.cluster.local:6379/0",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="APP_ALLOW_DUPE_URL",
                                    value="1",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="APP_CHECK_URL_REACH",
                                    value="0",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="APP_ADMIN_TOKEN",
                                    value="qazwsxedcrfvtgbyhnujmikolp",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="GOOGLE_CLIENT_ID",
                                    value="x",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="GOOGLE_CLIENT_SECRET",
                                    value="x",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="MICROSOFT_TENANT_ID",
                                    value="x",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="MICROSOFT_CLIENT_ID",
                                    value="x",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="MICROSOFT_CLIENT_SECRET",
                                    value="x",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="YAHOO_CLIENT_ID",
                                    value="x",
                                ),
                                kubernetes.core.v1.EnvVarArgs(
                                    name="YAHOO_CLIENT_SECRET",
                                    value="x",
                                ),
                            ],
                            resources=kubernetes.core.v1.ResourceRequirementsArgs(
                                limits={
                                    "cpu": "400m",
                                    "memory": "256Mi",
                                },
                                requests={
                                    "cpu": "300m",
                                    "memory": "256Mi",
                                },
                            ),
                        ),
                    ],
                    volumes=[
                        kubernetes.core.v1.VolumeArgs(
                            name="nginx-cache-volume",
                            empty_dir={},
                        ),
                        kubernetes.core.v1.VolumeArgs(
                            name="nginx-config-volume",
                            config_map={
                                "name": "nginx-conf",
                            },
                        ),
                    ],
                    restart_policy="Always",
                ),
            ),
        ))
    app_nginx_conf_config_map = kubernetes.core.v1.ConfigMap("appNginx_confConfigMap",
        api_version="v1",
        kind="ConfigMap",
        metadata=kubernetes.meta.v1.ObjectMetaArgs(
            name="nginx-conf",
            namespace="app",
        ),
        data={
            "nginx.conf": """
        user  nginx;
        worker_processes  1;
        events {
            worker_connections  1024;
        }
        error_log  /var/log/nginx/error_log.log warn;

        pid        /var/run/nginx.pid;
        http {
                proxy_cache_path /srv/nginx/ levels=1:2 keys_zone=nginx_cache:10m max_size=10g inactive=60m use_temp_path=off;
                add_header X-Cache-Status $upstream_cache_status;
                log_format  main  '$remote_addr|$http_x_forwarded_for||$remote_user '
                                '[$time_local]|"$request"|'
                                '$status $body_bytes_sent|"$http_referer"|'
                                '"$http_user_agent"|"$request_time"|"$upstream_cache_status"';
                log_format prom 'time:$request_time status=$status host="$host" method="$request_method" uri="$uri" upstream="$upstream_addr"  upstream_cache_status="$upstream_cache_status"';
                keepalive_timeout  65;
                server {
                        gzip         on;
                        listen       80;
                    # server_name  localhost;

                        location /nginx_status {
                            stub_status;
                            access_log /var/log/nginx/status.access.log main;
                        }

                        location / {
                            #cache 200,301,302
                            #cache POST,GET,HEAD requests
                            #We can cache PUT /api/urls in an effort to not overwhelm
                            #application server
                            proxy_cache_valid 200 301 302;
                            proxy_cache_methods GET HEAD;
                            proxy_cache_key "$uri|$request_body";
                            proxy_cache_revalidate on;
                            proxy_ignore_headers Cache-Control;
                            proxy_cache nginx_cache;
                            proxy_pass  http://localhost:3000/;
                            access_log /var/log/nginx/tinyurl_access_log.log main;
                            access_log syslog:server=127.0.0.1:9514 prom;

                        }
        }
        }
    """,
        })
    app_nginx_metrics_service = kubernetes.core.v1.Service("appNginx_metricsService",
        api_version="v1",
        kind="Service",
        metadata=kubernetes.meta.v1.ObjectMetaArgs(
            labels={
                "io.kompose.service": "tinyurl",
            },
            annotations={
                "prometheus.io/scrape": "true",
                "alpha.monitoring.coreos.com/non-namespaced": "true",
            },
            name="nginx-metrics",
            namespace="app",
        ),
        spec=kubernetes.core.v1.ServiceSpecArgs(
            ports=[
                kubernetes.core.v1.ServicePortArgs(
                    name="nginx-ex-port",
                    port=9113,
                    target_port="nginx-ex-port",
                    protocol="TCP",
                ),
                kubernetes.core.v1.ServicePortArgs(
                    name="metrics",
                    port=9147,
                    target_port="metrics",
                    protocol="TCP",
                ),
            ],
            selector={
                "io.kompose.service": "tinyurl",
            },
        ))
    app_tinyurl_service = kubernetes.core.v1.Service("appTinyurlService",
        api_version="v1",
        kind="Service",
        metadata=kubernetes.meta.v1.ObjectMetaArgs(
            name="tinyurl",
            namespace="app",
            annotations={
                "service.beta.kubernetes.io/aws-load-balancer-backend-protocol": "http",
                "service.beta.kubernetes.io/aws-load-balancer-ssl-cert": f"{acm_cert_arn}",
                "service.beta.kubernetes.io/aws-load-balancer-ssl-ports": "https",
                "external-dns.alpha.kubernetes.io/hostname": f"tinyurl-{region}.web.scoady.io",
                "service.beta.kubernetes.io/aws-load-balancer-type": "nlb",
            },
        ),
        spec=kubernetes.core.v1.ServiceSpecArgs(
            selector={
                "io.kompose.service": "tinyurl",
            },
            ports=[
                kubernetes.core.v1.ServicePortArgs(
                    name="http",
                    port=80,
                    target_port=80,
                ),
                kubernetes.core.v1.ServicePortArgs(
                    name="https",
                    port=443,
                    target_port=80,
                ),
            ],
            type="LoadBalancer",
        ))

