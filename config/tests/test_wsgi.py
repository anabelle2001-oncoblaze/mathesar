import pytest

from config.wsgi import strip_base_path


def _get_path_info_seen_by_app(base_path, path_info):
    seen = {}

    def app(environ, start_response):
        seen['path_info'] = environ['PATH_INFO']

    strip_base_path(app, base_path)({'PATH_INFO': path_info}, None)
    return seen['path_info']


@pytest.mark.parametrize('path_info,expected_path_info', [
    ('/mathesar/', '/'),
    ('/mathesar', '/'),
    ('/mathesar/db/1/', '/db/1/'),
    ('/mathesar/static/icons/favicon.ico', '/static/icons/favicon.ico'),
    # Paths which have already had the base path removed by the reverse proxy
    ('/', '/'),
    ('/db/1/', '/db/1/'),
    # Paths which only look like they start with the base path
    ('/mathesarx/', '/mathesarx/'),
])
def test_strip_base_path(path_info, expected_path_info):
    assert _get_path_info_seen_by_app('/mathesar', path_info) == expected_path_info
