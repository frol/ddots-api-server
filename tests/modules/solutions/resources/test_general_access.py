# pylint: disable=missing-docstring
import pytest


@pytest.mark.parametrize('http_method,http_path', (
    ('OPTIONS', '/api/v1/solutions/'),
    ('GET', '/api/v1/solutions/'),
    ('POST', '/api/v1/solutions/'),
    ('OPTIONS', '/api/v1/solutions/latest-new'),
    ('PATCH', '/api/v1/solutions/latest-new'),
    ('OPTIONS', '/api/v1/solutions/1'),
    ('GET', '/api/v1/solutions/1'),
    ('PATCH', '/api/v1/solutions/1'),
    ('DELETE', '/api/v1/solutions/1'),
    ('OPTIONS', '/api/v1/solutions/1/source-code'),
    ('GET', '/api/v1/solutions/1/source-code'),
    ('OPTIONS', '/api/v1/solutions/1/testing-report'),
    ('POST', '/api/v1/solutions/1/testing-report'),
))
def test_unauthorized_access(http_method, http_path, flask_app_client):
    response = flask_app_client.open(method=http_method, path=http_path)
    assert response.status_code == 401
