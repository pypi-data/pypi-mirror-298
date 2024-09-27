# Zulip prometheus exporter

This is based on the work by [brokenpip3](https://github.com/brokenpip3) in [zulip-exporter](https://github.com/brokenpip3/zulip-exporter)

## Installation

`pip3 install zulip-exporter`

Or

`pipx install git+https://github.com/Digitalist-Open-Cloud/Zulip-Exporter.git`

Or use the docker image (prefered)

### Environment variable

|     Environment Variable     | Description                                                    | Default   | Required |
|:----------------------------:|----------------------------------------------------------------|-----------|:--------:|
|         `ZULIP_EMAIL`        | Zulip email from zuliprc                                       |           |    ✅    |
|        `ZULIP_API_KEY`       | Zulip api-key from zuliprc                                     |           |    ✅    |
|          `ZULIP_SITE`        | URL where your Zulip server is located                         |           |    ✅    |
|            `PORT`            | Http port to listen on                                         |  `9863`   |    ❌    |
|            `SLEEP`           | Time to wait in seconds between metric grabbing cycles        |  `120`    |    ❌    |


## Usage

To use the Zulip exporter, you first need to set the environment variables.

When just start the exporter, like:

```sh
zulip-exporter
```

Or run with docker image, like:

```sh
docker run --rm -p 9863:9863 -e ZULIP_SITE=https://my.zulip.site -e ZULIP_API_KEY=secretAPIkey -e ZULIP_EMAIL=user@myzulip.com  docker.io/digitalist/zulip-exporter
```


## Docker compose example

```yaml
  zulip-exporter:
    container_name: zulip-exporter
    restart: unless-stopped
    image: quay.io/brokenpip3/zulip-exporter:0.0.1
    labels:
      io.prometheus.scrape: true
      io.prometheus.port: 9863
      io.prometheus.path: /metrics
    env_file:
      - .env-zulip
    ports:
      - "9863"
```

## Kubernetes

see [example](./kubernetes)

## Metrics

- Server info: `zulip_server`

- Users info: `zulip_user_*`

- Streams info: `zulip_stream_*`

## Prometheus rules examples

see [rules examples](./kubernetes/zulip-rules.yaml)

## Grafana dashboard

![image](./grafana/example.png)

see [example dashboard](./grafana/dashboard.json)

## Development

### Setup

- poetry install
- poetry run python3 zulip-exporter

### Publish

- poetry install
- poetry build
- poetry publish
