from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
import json
import zulip

client = zulip.Client()

class InfoCollector(object):
    def collect(self):
        c = GaugeMetricFamily('zulip_server', 'Server Info', labels=['info'])
        a = GaugeMetricFamily('authentication_methods', 'Authentication Methods', labels=['auth'])
        r = json.loads(json.dumps(client.get_server_settings()))
        extract_values = ['zulip_version','zulip_feature_level', 'push_notifications_enabled','require_email_format_usernames','is_incompatible']
        for i in r:
            if i in extract_values:
              if type(r[i]) == bool:
                  value = int(r[i])
              else: value = r[i]
              c.add_metric([i], value)
        yield c