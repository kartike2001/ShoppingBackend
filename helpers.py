import random
import string


def escape_sql(value):
    if isinstance(value, str):
        value = value.replace("'", "''")
        value = value.replace(";", " ")
        value = value.replace("-", "_")
        value = value.replace("\\", "/")
    return value


def escape_html(value):
    if isinstance(value, str):
        value = value.replace("<", "&lt;")
        value = value.replace(">", "&gt;")
        value = value.replace("&", "&amp;")
        value = value.replace('"', "&quot;")
        value = value.replace("'", "&#x27;")
        value = value.replace("/", "&#x2F;")
    return value


def generate_token():
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=200))
    return token
