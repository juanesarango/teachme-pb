# parse_qs
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

# json
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json

# httplib2
from lib import httplib2

# socks
try:
    from lib.httplib2 import socks
    from httplib2.socks import (
        PROXY_TYPE_HTTP,
        PROXY_TYPE_SOCKS4,
        PROXY_TYPE_SOCKS5
    )
except ImportError:
    from lib.httplib2 import socks
    from lib.httplib2.socks import (
        PROXY_TYPE_HTTP,
        PROXY_TYPE_SOCKS4,
        PROXY_TYPE_SOCKS5
    )
