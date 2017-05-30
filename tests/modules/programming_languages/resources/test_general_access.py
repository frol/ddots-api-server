# pylint: disable=missing-docstring
import pytest


@pytest.mark.parametrize('http_method,http_path', (
    ('GET', '/api/v1/programming-languages/'),
    ('POST', '/api/v1/programming-languages/'),
    ('GET', '/api/v1/programming-languages/pascal'),
    ('PATCH', '/api/v1/programming-languages/pascal'),
    ('DELETE', '/api/v1/programming-languages/pascal'),
))
def test_unauthorized_access(http_method, http_path, flask_app_client):
    response = flask_app_client.open(method=http_method, path=http_path)
    assert response.status_code == 401
