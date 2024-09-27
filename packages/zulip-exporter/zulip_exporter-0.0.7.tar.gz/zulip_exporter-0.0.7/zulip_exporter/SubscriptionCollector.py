import json
import zulip
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

client = zulip.Client()

class SubscriptionCollector(object):
    def collect(self):
        r = json.loads(json.dumps(client.get_subscriptions()))
        yield CounterMetricFamily('zulip_stream', 'Total Streams', value=(len(r['subscriptions'])))
        for x in r['subscriptions']:
          for k, v in x.items():
            t = type(v)
            if k != "name":
                if t == int or t == bool:
                  metrictemp = GaugeMetricFamily(f'zulip_stream_{k}', f'{k}', labels=["stream"])
                  metrictemp.add_metric([x['name']], int(v))
                  yield metrictemp
