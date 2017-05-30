# pylint: disable=missing-docstring
import pytest


@pytest.mark.parametrize('http_method,http_path', (
    ('GET', '/api/v1/problems/'),
    ('POST', '/api/v1/problems/'),
    ('GET', '/api/v1/problems/1'),
    ('PATCH', '/api/v1/problems/1'),
    ('DELETE', '/api/v1/problems/1'),
    ('GET', '/api/v1/problems/1/tests.tar.gz'),
))
def test_unauthorized_access(http_method, http_path, flask_app_client):
    response = flask_app_client.open(method=http_method, path=http_path)
    assert response.status_code == 401
