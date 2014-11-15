# -*- coding: utf-8 -*-
from utils.yaml_utils import YamlObject
from os.path import dirname
from os.path import join as join_dirs


class config(object):
    DEBUG = True


class settings(object):
    megafon_accounts = {}
    megafon_robots_url = 'https://kavkazsg.megafon.ru/ROBOTS/SC_TRAY_INFO?X_Username={username}&X_Password={password}'
    base_url = 'managment_modem'

    def __init__(self):
        super(settings, self).__init__()
        acoounts_obj = YamlObject(join_dirs(dirname(__file__), 'accounts.yaml'))
        self.megafon_accounts = acoounts_obj.deserialize()

    def get_megafon_robots_url_with_acc(self, account_name=None):
        result = None
        if(account_name and account_name in self.megafon_accounts):
            account = self.megafon_accounts[account_name]
            result = self.megafon_robots_url.format(
                username=account['username'],
                password=account['password']
            )
        else:
            result = False
        return result
