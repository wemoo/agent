from wemoo_agent.network.request import http_post
from wemoo_agent.system.os_info import system
from wemoo_agent.config.config import config


def login_or_register_host():
    url = config.server + '/api/hosts'
    response = http_post(url, data=system)
    if response:
        return True

    return False
