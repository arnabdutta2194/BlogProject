import datetime
from itertools import count
import re
from django.utils.html import strip_tags

def count_words(html_string):
    # html_string = """
    # <h1>Title</h1>
    # """
    word_string = strip_tags(html_string)
    count = len(re.findall(r'\w',word_string))
    return count

def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = (int(count)/200)
    read_time_sec = read_time_min * 60
    read_time =str(datetime.timedelta(seconds=read_time_sec))
    return read_time