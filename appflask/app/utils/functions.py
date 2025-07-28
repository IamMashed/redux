from decimal import Decimal
import urllib.parse

from flask import current_app
from orjson import dumps  # Faster than native json


def jsonify(*args, **kwargs):
    """
    Quicker version of JSONify that does not do pretty printing
    Source: https://stackoverflow.com/questions/37931927/why-is-flasks-jsonify-method-slow
    """

    def default(obj):
        """
        Define default serialization behavior for the unsupported types
        """

        # handle unsupported 'Decimal' type
        if isinstance(obj, Decimal):
            return str(obj)

        #  Specify that a type was not handled by default, raise an exception such as TypeError.
        raise TypeError

    if args and kwargs:
        raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs

    return current_app.response_class(
        dumps(data, default=default) + bytes('\n', 'utf-8'),
        mimetype=current_app.config['JSONIFY_MIMETYPE']
    )


def make_url(base_url, *res, **params):
    url = base_url
    for r in res:
        url = '{}/{}'.format(url, r)
    if params:
        url = '{}?{}'.format(url, urllib.parse.urlencode(params))
    return url
