import re

html_pattern = re.compile(r"<([a-zA-Z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)")


def is_html(text):
    return bool(html_pattern.search(text))
