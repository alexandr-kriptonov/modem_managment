# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
from config import settings as _settings
from utils.xml_utils import MegafonInfo

settings = _settings()
base_url = settings.base_url


def get_url(url):
    return '/{base_url}/{url}'.format(base_url=base_url, url=url)


class custom_Blueprint(Blueprint):

    def route(self, rule, **options):
        rule = get_url(rule)
        return super(custom_Blueprint, self).route(rule, **options)

_pages = \
    custom_Blueprint(
        '_pages', __name__,
        template_folder='templates'
    )


@_pages.route('', defaults={'page': ''})
@_pages.route('<page>')
def show(page):
    try:
        return render_template('{0}.html'.format(page))
    except TemplateNotFound:
        return render_template('404.html'), 404


@_pages.route('index')
def index():
    name_accounts = []
    for name in settings.megafon_accounts:
        name_accounts.append(name)
    return render_template('index.html', name_accounts=name_accounts, base_url=base_url)


@_pages.route('load_megafon_table/name=<string:name>')
def load_megafon_table(name):
    if(settings.megafon_accounts.get(name, False)):
        info = MegafonInfo(name, settings).get_info()
        used_options = settings.megafon_accounts[name]['used_options']
    else:
        info = {}
        used_options = []
    return render_template('megafon_table.html', info=info, used_options=used_options)
