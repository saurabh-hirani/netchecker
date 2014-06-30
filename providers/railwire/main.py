import os
import requests

from bs4 import BeautifulSoup
from prettytable import PrettyTable
from datetime import datetime, timedelta
from collections import OrderedDict

from netchecker.base_provider import BaseProvider
import netchecker.utils as utils
import netchecker.providers.railwire.auth as railwire_auth

class NetProvider(BaseProvider):

    class Plan(BaseProvider.ProviderAttr):
        def __init__(self):
            self.name = None
            self.data_limit = None
            self.speed = None
            self.table_headers = ['Plan name', 'Time (Days)', 'Data Limit (GB)', 'Speed (Mbps)']
            self.table_keys = ['name', 'time', 'data_limit', 'speed']
            self.calculated = False

    class Usage(BaseProvider.ProviderAttr):
        def __init__(self):
            super(NetProvider.Usage, self).__init__()
            self._plan = NetProvider.Plan()
            self.details = None
            self.data_limit = None
            self.total_download = None
            self.total_upload = None
            self.total_time = None
            self.table_headers = [
                'Date', 
                'Data Limit (GB)', 
                'Total Download (GB)', 
                'Total Upload (GB)', 
                'Total Time'
            ]
            self.table_keys = [
                'date', 
                'data_limit', 
                'total_download', 
                'total_upload', 
                'total_time'
            ]
            self.calculated = False

        @property
        def plan(self):
            return self._plan

    def __init__(self):
        super(NetProvider, self).__init__()
        self._main_url = 'http://billing.railwire.co.in/dologin.php'
        self._usage = NetProvider.Usage()

    def _get_plan(self):
        _page_info = self._page_info
        if _page_info is None:
            _page_info = self._build_page_info()

        for row in _page_info['usage_summary'].find_all('tr')[2:]:
            if len(row('td')) > 1:
                resource, allocated = row('td')[0:2]
                setattr(self._usage._plan, resource.string.replace(' ', '_').lower(), allocated.string)

        self._usage._plan.name = str(self._page_info['registration'].find_all('tr')[4]('td')[1].string)
        self._usage._plan.data_limit = float(self._usage._plan.data_transfer.replace('MB', '')) / 1024
        self._usage._plan.speed = float(self._usage._plan.package_speed.replace('kbps', '')) / 1024
        self._usage._plan.time = int(self._usage._plan.time.replace('Days', ''))

        delattr(self._usage._plan, 'data_transfer')
        delattr(self._usage._plan, 'package_speed')

        self._usage._plan.calculated = True
        return self._usage._plan

    def cleanse_usage_data(self, _usage = None):
        if _usage is None:
            _usage = self._usage

        total_download = 0
        total_upload = 0
        total_time = 0 

        for session_details in _usage.details:
            for k, v in session_details.iteritems():
                if k == 'duration':
                    hours, mins, sec = [int(x) for x in v.split(':')]
                    total_time += hours * 3600 + mins * 60 + sec
                elif k == 'download_data':
                    total_download += float(v)
                elif k == 'upload_data':
                    total_upload += float(v)

        sec = timedelta(seconds = total_time)
        d = datetime(1, 1, 1) + sec
        total_time = "%d days + %d:%d:%d" % (d.day-1, d.hour, d.minute, d.second)

        self._get_plan()
        self._usage.data_limit = float(self._usage._plan.data_limit)
        self._usage.total_upload = float('%.2f' % (total_upload / 1024))
        self._usage.total_download = float('%.2f' % (total_download / 1024))
        self._usage.total_time = total_time
        self._usage.calculated = True
        return self._usage

    def _build_page_info(self, _usage_html = None):
        """
        Railwire's usage page contains information about lot of other sections.
        This method stores each section in self._page_info
        """
        if _usage_html is None:
            _usage_html = self._usage_html
        soup = BeautifulSoup(_usage_html)

        info_sections = [None, 'package', 'registration', 'usage_summary', None, 'session_details']
        page_info = {}
        for table_type, table_data in zip(info_sections, soup.find_all('table')):
            if table_type is None:
                continue
            page_info[table_type] = table_data
        self._page_info = page_info
        return self._page_info

    def extract_usage_data(self, _usage_html = None):
        if _usage_html is None:
            _usage_html = self._usage_html
        self._build_page_info()
        all_session_details = []
        session_cols = ['sl.no', 'ip', 'start_time', 'end_time', 'duration', 'upload_data', 'download_data', 'total_data']
        for row in self._page_info['session_details'].find_all('tr')[1:]:
            session_details = OrderedDict()
            for colname, td in zip(session_cols, row('td')):
                session_details[colname] = td.string
            all_session_details.append(session_details)
        self._usage.details = all_session_details

    def get_usage_html(self):
        if self._usage_html is None and os.path.exists(self.usage_file):
                with open(self.usage_file) as f:
                    self._usage_html = f.read()
                    return self._usage_html
        payload = {
            'operator_user': railwire_auth.USERNAME,
            'operator_pass': railwire_auth.PASSWORD
        }
        sess = requests.Session()
        sess.post('http://billing.railwire.co.in/dologin.php', data=payload)
        r = sess.get('http://billing.railwire.co.in/slogin-datausage-mybilling.php')
        self._usage_html = r.content
        with open(self.usage_file, 'w') as f:
            f.write(self._usage_html)
        return self._usage_html
