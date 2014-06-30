import datetime
from prettytable import PrettyTable

def get_date():
    return str(datetime.date.today())

def conv_header_to_keys(headers):
    return [x.replace(' ', '_').lower() for x in headers]

def print_obj(obj, headers, attrs):
    pt = PrettyTable(field_names=headers)
    values = [getattr(obj, attr) for attr in attrs]
    pt.add_row(values)
    return str(pt)
