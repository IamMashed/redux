from flask import jsonify
import sys


class ValidationError(ValueError):
    pass


class ServerError(ValueError):
    pass


class NotFoundError(ValueError):
    pass


def bad_request(message, error_type='bad_request'):
    response = jsonify({'error': error_type, 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def not_found(message):
    response = jsonify({'error': 'not_found', 'message': message})
    response.status_code = 404
    return response


def multiple_found(message):
    response = jsonify({'error': 'multiple_found', 'message': message})
    response.status_code = 500
    return response


def server_error(message):
    response = jsonify({'error': 'server_error', 'message': message})
    response.status_code = 500
    import traceback
    traceback.print_exc(file=sys.stdout)

    return response


def validation_error(message):
    response = jsonify({'error': 'validation error', 'message': message})
    response.status_code = 400
    return response
