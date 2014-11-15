# -*- coding: utf-8 -*-

from lxml.etree import parse, XMLParser, XPathEvalError
from StringIO import StringIO
from datetime import datetime
import requests


XPATH_IDS = {
    'fullname': 'NAME',
    'number': 'NUMBER',
    'status': 'STATUS',
    'rate_plan': 'RATE_PLAN',
    'balance': 'BALANCE',
    'update_datetime': 'DATE',
    'packs': 'GET_PACKS_AND_DISCOUNTS_INFO',
    'pack': 'PACK',
    'pack_name': 'DISCOUNT/PLAN_NAME',
    'activate_date': 'DISCOUNT/ACTIVATE_DATE',
    'close_date': 'DISCOUNT/CLOSE_DATE',
    'volume_total': 'DISCOUNT/VOLUME_TOTAL',
    'volume_availaible': 'DISCOUNT/VOLUME_AVAILABLE',
}


def _get_value(parent, name, type_result='list'):
    result = None
    _xpath = XPATH_IDS.get(name, '')
    try:
        _result = parent.xpath(_xpath)
        if((type_result == 'text') and (len(_result) == 1)):
            result = _result[0].text
        elif((type_result == 'first_in_list') and (isinstance(_result, list)) and (len(_result) >= 1)):
            result = _result[0]
        else:
            result = _result
    except XPathEvalError:
        result = False
    except AttributeError:
        result = parent.xpath(_xpath)
    finally:
        return result


def sizeof_fmt(num):
    if(num):
        num = float(num)
        for x in ['KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.2f %s" % (num, x)
            num /= 1024.0


def get_volume_consumption(total, availaible):
    result = ''
    if(total and availaible):
        result = float(total) - float(availaible)
    return result


class MegafonInfo(object):

    def __init__(self, name, settings):
        super(MegafonInfo, self).__init__()
        self.name = name
        self.settings = settings

    def get_xml(self):
        url = self.settings.get_megafon_robots_url_with_acc(self.name)
        response = requests.get(url)
        self.xml = response.content

    def parse_xml(self):
        result = {
            'fullname': '',
            'number': '',
            'status': False,
            'rate_plan': '',
            'balance': '',
            'update_datetime': datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            'pack_name': '',
            'activate_date': '',
            'close_date': '',
            'volume_total': '',
            'volume_availaible': '',
            'volume_consumption': '',
        }
        if(self.xml):
            parser = XMLParser()
            root = parse(StringIO(self.xml), parser)
            if(root):
                result.update({
                    'fullname': _get_value(root, 'fullname', 'text'),
                    'number': "+7{0}".format(_get_value(root, 'number', 'text')),
                    'status': _get_value(root, 'status', 'text'),
                    'rate_plan': _get_value(root, 'rate_plan', 'text'),
                    'balance': _get_value(root, 'balance', 'text'),
                    'update_datetime': _get_value(root, 'update_datetime', 'text'),
                })
                packs = _get_value(root, 'packs', 'first_in_list')
                if(packs is not None):
                    pack = _get_value(packs, 'pack', 'first_in_list')
                    if(pack is not None):
                        result.update({
                            'pack_name': _get_value(pack, 'pack_name', 'text'),
                            'activate_date': _get_value(pack, 'activate_date', 'text'),
                            'close_date': _get_value(pack, 'close_date', 'text'),
                            'volume_total': sizeof_fmt(_get_value(pack, 'volume_total', 'text')),
                            'volume_availaible': sizeof_fmt(_get_value(pack, 'volume_availaible', 'text')),
                            'volume_consumption': sizeof_fmt(
                                get_volume_consumption(
                                    _get_value(pack, 'volume_total', 'text'),
                                    _get_value(pack, 'volume_availaible', 'text')
                                )
                            ),
                        })
        return result

    def get_info(self):
        self.get_xml()
        info = self.parse_xml()
        return info
