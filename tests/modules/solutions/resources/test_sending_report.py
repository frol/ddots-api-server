import json
import mock

from app.extensions import seaweedfs


def test_sending_testing_report(flask_app_client, db, internal_user, solution):
    with db.session.begin():
        solution.state = solution.States.received

    with flask_app_client.login(internal_user, auth_scopes=('solutions:write',)), \
            mock.patch.object(seaweedfs, 'upload_file', return_value='5,1') as mocked_upload_file:
        response = flask_app_client.post(
            '/api/v1/solutions/%d/testing-report' % solution.id,
            data=json.dumps({
                'tests': [
                    {'status': 'OK', 'execution_time': 11111111, 'memory_peak': 350},
                    {'status': 'OK', 'execution_time': 99999999, 'memory_peak': 100},
                ]
            })
        )
        assert mocked_upload_file.called

    assert response.status_code == 200
    assert set(response.json.keys()) >= {'id', 'author', 'problem', 'programming_language'}
