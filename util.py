import datetime
from operator import itemgetter
from itertools import groupby

def timestamp_to_str(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

def get_attr(obj, prop):
    if isinstance(obj, dict):
        return obj[prop]

    return getattr(obj, prop)
        
def sum_list(objs, prop, default=0):
    if not objs:
        return default
    return sum(get_attr(obj, prop) for obj in objs)
    
def distinct_list(arr, prop):
    seen = set()
    result = []
    for obj in arr:
        val = get_attr(obj, prop)
        if val not in seen:
            result.append(obj)
            seen.add(val)
            
    return result
    
def group_list(arr, prop):
    result = {}
    sorted_data = sorted(arr, key=itemgetter(prop))
    for key, value in groupby(sorted_data, key=itemgetter(prop)):
        result[key] = list(value)
    return result
    