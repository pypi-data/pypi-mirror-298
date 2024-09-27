import json
import zulip
from prometheus_client.core import CounterMetricFamily

client = zulip.Client()

class UserCollector(object):
    def collect(self):
        r = json.loads(json.dumps(client.get_members()))
        yield CounterMetricFamily('zulip_user', 'Total user', value=(len(r['members'])))
        count_dict = {}
        for i in r['members']:
            for k, v in i.items():
                if v == True:
                    count_dict[k] = count_dict.get(k, 0) + 1
        yield CounterMetricFamily('zulip_user_bots', 'Total Bot accounts', value=(count_dict.get('is_bot',0)))
        yield CounterMetricFamily('zulip_user_admins', 'Total Admins accounts', value=(count_dict.get('is_admin',0)))
        yield CounterMetricFamily('zulip_user_guests', 'Total Guests accounts', value=(count_dict.get('is_guest',0)))
        yield CounterMetricFamily('zulip_user_active', 'Total Active accounts', value=(count_dict.get('is_active',0)))
        yield CounterMetricFamily('zulip_user_owners', 'Total Owners accounts', value=(count_dict.get('is_owner',0)))
