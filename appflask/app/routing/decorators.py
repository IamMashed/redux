import time
from functools import wraps
import gzip
from io import BytesIO

from flask import g, request, abort
from flask_login import current_user
from .errors import forbidden, not_found
from ..database.models.user import Permission
from ..utils.constants import County


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = g.get('current_user', None) or current_user
            if not user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


class Domain:
    REDUX = 1
    PTRC = 2
    BETA = 4
    BETA_REDUX = 8

    REDUX_NAME = 'reduxinternal.redux.tax'
    PTRC_NAME = 'ptrcinternal.redux.tax'
    BETA_NAME = 'betacma.alandarev.com'
    BETA_REDUX_NAME = 'beta.redux.tax'
    LOCALHOST_NAME = '127.0.0.1:5000'

    @classmethod
    def get_allowed_counties(cls, domain):
        """
        Get allowed counties by request domain name
        """
        if domain == cls.PTRC_NAME:
            return County.get_counties()
        # if domain == cls.LOCALHOST_NAME:
        #     return [County.NASSAU, County.SUFFOLK]
        return County.get_counties()


domain_permissions = {
    Domain.REDUX_NAME: Domain.REDUX,
    Domain.PTRC_NAME: Domain.PTRC,
    Domain.BETA_NAME: Domain.BETA,
    Domain.BETA_REDUX_NAME: Domain.BETA_REDUX
}


def domains_allowed(*args):
    domain_permission = sum(args)

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # could be three types of domains
            # reduxinternal, ptrcinternal and betacma
            domain = request.headers['Host']
            permission = domain_permissions.get(domain)
            if domain == '127.0.0.1:5000' or domain == 'localhost:5000':
                pass
            elif not permission or not permission & domain_permission == permission:
                # return not_found('requested url is not found')
                return abort(404)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def gzipped(f):
    """
    GZIPs large responses
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request
        if ('Accept-Encoding' not in request.headers) or ('gzip' not in request.headers['Accept-Encoding']):
            return f(*args, **kwargs)

        response = f(*args, **kwargs)

        gzip_buffer = BytesIO()
        gzip_file = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=gzip_buffer)
        gzip_file.write(response.get_data())
        gzip_file.close()

        response.set_data(gzip_buffer.getvalue())
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = len(response.get_data())

        return response

    return decorated_function


def prop_id_allowed(f):
    """
    Check the county of property id and disallow if from florida for certain domains
    """
    from .services import PropertyService

    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_domain = request.headers['Host']
        allowed_counties = Domain.get_allowed_counties(request_domain)
        property_id = kwargs.get('property_id')
        subject = PropertyService.get_property(property_id)
        if subject.county not in allowed_counties:
            return not_found('Requested property id does not exist')
        return f(*args, **kwargs)

    return decorated_function


def timeit(func):
    """
    Decorator function for the method execution timing
    """

    def wrapper_timeit(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print('%r  %2.2f ms' % (func.__name__.upper(), (end_time - start_time) * 1000))
        return result

    return wrapper_timeit
