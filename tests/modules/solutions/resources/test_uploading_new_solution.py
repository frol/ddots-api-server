import mock
import pytest

from app.extensions import seaweedfs


def test_uploading_new_solution_to_not_existing_problem(flask_app_client, regular_user):
    with flask_app_client.login(regular_user, auth_scopes=('solutions:write',)), \
            mock.patch.object(seaweedfs, 'upload_file', return_value='5,2') as mocked_upload_file:
        response = flask_app_client.post(
            '/api/v1/solutions/',
            data={
                'problem_id': 0,
                'programming_language_name': 'non-existing-language',
                'source_code': 'int main() {}'
            }
        )
        assert not mocked_upload_file.called

    assert response.status_code == 422
    assert response.content_type == 'application/json'
    assert set(response.json.keys()) >= {'status', 'message'}


def test_uploading_new_solution(flask_app_client, regular_user, problem, programming_language_c):
    with flask_app_client.login(regular_user, auth_scopes=('solutions:write',)), \
            mock.patch.object(seaweedfs, 'upload_file', return_value='5,2') as mocked_upload_file:
        response = flask_app_client.post(
            '/api/v1/solutions/',
            data={
                'problem_id': problem.id,
                'programming_language_name': programming_language_c.name,
                'source_code': 'int main() {}'
            }
        )
        assert mocked_upload_file.called

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert set(response.json.keys()) >= {'id', 'problem', 'programming_language', 'author', 'state'}
    assert response.json['state'] == 'new'
