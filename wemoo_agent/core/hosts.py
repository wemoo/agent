from simplejson import loads
from simplejson import dump

from wemoo_agent.network.request import http_post
from wemoo_agent.system.os_info import system
from wemoo_agent.config.config import config


def login_or_register_host():
    url = config.server + '/api/hosts'
    response = http_post(url, data=system)

    if response:
        json = response.json()
        if json.get('success'):
            host_id = json['content']['id']
            update_host_config(host_id)
            return True

    return False


def update_host_config(host_identity):
    config.host_identity = host_identity
    json = config.to_dict()
    with open(config.config_path, 'w') as outfile:
        dump(json, outfile, sort_keys=True, indent=4 * ' ')
