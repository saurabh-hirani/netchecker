import netchecker.utils as utils
import os
import sys
from abc import ABCMeta, abstractmethod

class BaseProvider(object):

    class ProviderAttr(object):
        def __init__(self):
            self.date = utils.get_date()
            self.table_headers = []
            self.table_keys = []
            self.calculated = False

        def __str__(self):
            if self.calculated is True:
                return utils.print_obj(self, self.table_headers, self.table_keys)
            return None

    __metaclass__ = ABCMeta

    def __init__(self):
        module_file = sys.modules[self.__module__].__file__
        self.base_dir = os.path.join(os.path.abspath(os.path.dirname(module_file)))
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.usage_file = os.path.join(self.data_dir, utils.get_date())
        self._usage_html = None
        self._usage = None

    @abstractmethod
    def get_usage_html(self):
        """
        Get the HTML page from which we are going to extract usage data
        """
        pass

    @abstractmethod
    def extract_usage_data(self):
        """
        Extract usage data key value pairs as they are present in usage_html
        """
        pass

    @abstractmethod
    def cleanse_usage_data(self):
        """
        Cleanse the data extracted by extract_usage_data - this is shown to the user
        """
        pass

    def _get_usage(self):
        """
        Called internally by usage property
        """
        return self.cleanse_usage_data(self.extract_usage_data(self.get_usage_html()))

    @property
    def usage(self):
        """
        Report the usage done as per the data available with the provider
        """
        if self._usage.calculated:
            with open(self.usage_file, 'a') as f:
                pass
        else:
            self._get_usage()
        return self._usage
