# -*- coding: utf-8 -*-

# import urllib2
import json
import traceback
import requests

from urllib.request import urlopen


class Request(object):
    def __init__(self):
        pass


def http_get(url, headers={}):
    try:
        response = requests.get(url, headers=headers)
        return response
    except Exception as inst:
        print('GET FAIL')
        print(type(inst))
        print(inst.args)
        print(inst)
        traceback.print_exc()
    return None


def http_long_poling(self, url):
    pass


def http_patch(url, data, headers={}):
    try:
        response = requests.patch(url, data=json.dumps(data), headers=headers)
        return response
    except Exception as inst:
        print('PATCH FAIL')
        print(type(inst))
        print(inst.args)
        print(inst)
        traceback.print_exc()
    return None


def http_post(url, data, headers={}):
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response
    except Exception as inst:
        print('POST FAIL')
        print(type(inst))
        print(inst.args)
        print(inst)
        traceback.print_exc()
    return None
