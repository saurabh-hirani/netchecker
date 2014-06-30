import os
import time
import re
import requests

from bs4 import BeautifulSoup
from prettytable import PrettyTable

from netchecker.base_provider import BaseProvider
import netchecker.utils as utils

class NetProvider(BaseProvider):

    class Plan(BaseProvider.ProviderAttr):
        def __init__(self):
            super(NetProvider.Plan, self).__init__()
            self.plan_name = None
            self.speed = None

        def __str__(self):
            return ''

    class Usage(BaseProvider.ProviderAttr):
        def __init__(self):
            super(NetProvider.Usage, self).__init__()
            self._plan = NetProvider.Plan()
            self.data_limit = None
            self.data_used = None
            self.data_remaining = None
            self.days_left = None
            self.table_headers = [
                'Date', 
                'Data Limit (GB)', 
                'Data Used (GB)', 
                'Data remaining (GB)', 
                'Days Left'
            ]
            self.table_keys = [
                'date', 
                'data_limit', 
                'data_used', 
                'data_remaining', 
                'days_left'
            ]

        @property
        def plan(self):
            return self._plan

    def __init__(self):
        super(NetProvider, self).__init__()
        self._main_url = 'http://www.airtel.in/smartbyte-s/page.html'
        self.extract_keywords = {
            'data_limit': 'High speed data limit',
            'data_remaining': 'Balance quota',
            'days_left': 'No. of days left in the current bill cycle'
        }
        self._usage = NetProvider.Usage()

    @staticmethod
    def _extract_number(num_str):
        return float(num_str.replace('GB', ''))

    @staticmethod
    def _extract_key_value(kv_str):
        if kv_str is not None:
            return kv_str.replace(u'\xa0', u'').split(':')[1].strip()

    def cleanse_usage_data(self, _usage = None):
        if _usage is None:
            _usage = self._usage
        _usage.days_left = int(_usage.days_left)
        _usage.data_remaining = float(_usage.data_remaining.replace('GB', ''))
        _usage.data_limit = float(_usage.data_limit.replace('GB', ''))
        _usage.data_used = _usage.data_limit - _usage.data_remaining
        return _usage

    def extract_usage_data(self, _usage_html = None):
        if _usage_html is None:
            _usage_html = self._usage_html
        soup = BeautifulSoup(_usage_html)
        for fname, fdesc in self.extract_keywords.iteritems():
            setattr(self._usage, fname, self._extract_key_value(soup.find(text=re.compile(fdesc))))
        self._usage.calculated = True
        return self._usage

    def get_usage_html(self):
        if self._usage_html is None and os.path.exists(self.usage_file):
            with open(self.usage_file) as f:
                self._usage_html = f.read()
                return self._usage_html
        r = requests.get(self._main_url)
        soup = BeautifulSoup(r.text)
        _usage_url = soup.find('iframe').attrs['src']
        r = requests.get(_usage_url)
        self._usage_html = r.text
        with open(self.usage_file, 'w') as f:
            f.write(self._usage_html)
        return self._usage_html
