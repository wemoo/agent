from wemoo_agent.network.request import http_post
from wemoo_agent.system.os_info import os_uuid
from wemoo_agent.system.os_info import hostname
from wemoo_agent.config.config import config


def login_or_register_host():
    url = config.server + '/api/hosts'
    response = http_post(url, data={'uuid': os_uuid(), 'hostname': hostname()})
    if response:
        return True

    return False
