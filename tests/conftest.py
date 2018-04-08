import pytest
import ujson
from flask import url_for

from flask_builder import create_app, create_db, drop_db, create_tables, init_app, init_mail

APP_NAME = 'ig'


@pytest.fixture(scope='module')
def app(request):
    """Session-wide test `Flask` application."""
    # Create DB
    # config = import_string(get_config_name())
    # dsn = config.SQLALCHEMY_DATABASE_URI
    # dsn = dsn[:dsn.rfind('/')] + '/notifier'  # Change DB-name
    # drop_db(dsn)
    # create_db(dsn)

    # # Create app
    # settings_override = {
    #     'TESTING': True,
    #     'SQLALCHEMY_DATABASE_URI': dsn
    # }
    app = create_app(name=APP_NAME)
    init_app(app)
    dsn = app.config['SQLALCHEMY_DATABASE_URI']
    drop_db(dsn)
    create_db(dsn)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    create_tables(app)  # Only after context was pushed

    # Add test client
    app.client = app.test_client()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def session(app, request):
    """Creates a new database session for a test."""
    connection = app.db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = app.db.create_scoped_session(options=options)

    app.db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='module')
def client(app):
    class Client(object):
        json_header = 'application/json'

        def _get_url(self, endpoint, **values):
            return url_for(endpoint=endpoint, **values)

        def _get_data(self, resp, check_status=None):
            if check_status:
                assert resp.status_code == check_status
            data = resp.data
            if resp.content_type == 'application/json':
                data = ujson.loads(resp.data)
            return data

        def send(self, endpoint, method, data=None, check_status=200, content_type=None, **values):
            kwargs = {}
            url = self._get_url(endpoint=endpoint, **values)
            func = getattr(app.client, method)
            if data:
                kwargs['data'] = data
            if content_type:
                kwargs['content_type'] = content_type
            resp = func(url, **kwargs)
            return self._get_data(resp, check_status=check_status)

        def get(self, **kwargs):
            return self.send(method='get', **kwargs)

        def delete(self, **kwargs):
            return self.send(method='delete', **kwargs)

        def post(self, content_type=None, data=None, **kwargs):
            content_type = content_type or self.json_header
            if content_type == self.json_header:
                data = ujson.dumps(data)
            return self.send(method='post', data=data, content_type=content_type, **kwargs)

        def put(self, content_type=None, data=None, **kwargs):
            content_type = content_type or self.json_header
            if content_type == self.json_header:
                data = ujson.dumps(data)
            return self.send(method='put', data=data, content_type=content_type, **kwargs)

    return Client()


@pytest.fixture(scope='session')
def empty_list_resp():
    return dict(results=[], total=0)



