# Zulip prom exporter

## Usage

- Start exporter


### Environment variable

|     Environment Variable     | Description                                                    | Default   | Required |
|:----------------------------:|----------------------------------------------------------------|-----------|:--------:|
|         `ZULIP_EMAIL`        | Zulip email from zuliprc                                       |           |    ✅    |
|        `ZULIP_API_KEY`       | Zulip api-key from zuliprc                                     |           |    ✅    |
|          `ZULIP_SITE`        | URL where your Zulip server is located                         |           |    ✅    |
|            `PORT`            | Http port to listen on                                         |  `9863`   |    ❌    |
|            `SLEEP`           | Time to wait in seconds beetween metric grabbing cycles        |  `120`    |    ❌    |

## Docker compose example

```
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
