import re
import inspect
from functools import update_wrapper

from flask import Response, request
from voluptuous import Invalid
import ujson
from flask_sqlalchemy import Model
from sqlalchemy.sql.schema import Table
from werkzeug import find_modules, import_string


def ujsonify(**data):
    return Response(ujson.dumps(data), mimetype='application/json')


def get_url_map(app):
    url_map = dict()
    p = re.compile(r'(<[\w]+)|(>)')

    for u in app.url_map.iter_rules():
        route = p.sub('', u.rule)

        if '.' not in u.endpoint:
            url_map[u.endpoint] = route
            continue

        mod, name = u.endpoint.split('.')
        if not url_map.get(mod):
            url_map[mod] = {}
        url_map[mod][name] = route

    return url_map


def get_consts_map():
    from app.templates.constants import HELP

    return dict(
        TEMPLATES=dict(HELP=HELP)
    )


def dataschema(schema):
    def decorator(f):
        def new_func(*args, **kwargs):
            try:
                request_values = request.get_json()
                if not request_values:
                    request_values = request.values.to_dict(flat=False)
                    for k, v in request_values.items():
                        if len(v) == 1:
                            request_values[k] = v[0]
                kwargs.update(schema(request_values))
            except Invalid as e:
                raise ApiException('Invalid data: %s (path: %s)' %
                                   (e.msg, '.'.join(map(str, e.path))))
            return f(*args, **kwargs)
        return update_wrapper(new_func, f)
    return decorator


class ApiException(Exception):
    def __init__(self, message, status=400):
        self.message = message
        self.status = status

    def to_result(self):
        return ujsonify(message=self.message), self.status


def find_models_and_tables():
    models_dict = {}
    for module_name in find_modules('app', include_packages=True):
        models_module = import_string('%s.models' % module_name, silent=True)
        if models_module:
            for name, item in models_module.__dict__.items():
                if (inspect.isclass(item) and Model in inspect.getmro(item)) \
                   or item.__class__ is Table:
                    models_dict[name] = item
    return models_dict

def setattrs(obj, **kwargs):
    """ Setting multiple object attributes at once """

    attrs = (a for a in dir(obj) if not a.startswith('_'))
    for attr in attrs:
        if attr in kwargs:
            setattr(obj, attr, kwargs[attr])
