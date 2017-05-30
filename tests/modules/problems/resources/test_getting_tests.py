import mock
import pytest

from app.extensions import seaweedfs


@pytest.mark.parametrize('auth_scopes', (
    ('problems:read', ),
    ('problems:read', 'problems:write', ),
))
def test_getting_problem_tests_archive_by_authorized_user(
        flask_app_client,
        internal_user,
        problem,
        auth_scopes
):
    with flask_app_client.login(internal_user, auth_scopes=auth_scopes), \
            mock.patch.object(seaweedfs, 'file_exists'), \
            mock.patch.object(seaweedfs, 'get_file', return_value=b'fake') as mocked_get_file:
        response = flask_app_client.get('/api/v1/problems/1/tests.tar.gz')
        assert mocked_get_file.called

    assert response.status_code == 200
    assert response.content_type == 'application/gzip'
    assert response.data == b'fake'
