# encoding: utf-8
from decimal import Decimal
import json

import pytest


@pytest.mark.parametrize('auth_scopes', (
    None,
    ('solutions:write', ),
))
def test_getting_list_of_solutions_by_unauthorized_user_must_fail(
        flask_app_client,
        regular_user,
        auth_scopes
):
    with flask_app_client.login(regular_user, auth_scopes=auth_scopes):
        response = flask_app_client.get('/api/v1/solutions/')

    assert response.status_code == 401
    assert response.content_type == 'application/json'
    assert set(response.json.keys()) >= {'status', 'message'}


@pytest.mark.parametrize('auth_scopes', (
    ('solutions:read', ),
    ('solutions:read', 'solutions:write', ),
))
def test_getting_list_of_solutions_by_authorized_user(
        flask_app_client,
        regular_user,
        solution,
        auth_scopes
):
    with flask_app_client.login(regular_user, auth_scopes=auth_scopes):
        response = flask_app_client.get('/api/v1/solutions/')

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert isinstance(response.json, list)
    assert set(response.json[0].keys()) >= {
        'id',
        'author',
        'problem',
        'programming_language',
        'created',
        'state',
        'status',
        'scored_points'
    }
    if response.json[0]['id'] == solution.id:
        assert isinstance(response.json[0]['scored_points'], str)
        assert Decimal(response.json[0]['scored_points']) == solution.scored_points


def test_getting_a_new_solution_for_testing(flask_app_client, regular_user, solution):
    with flask_app_client.login(regular_user, auth_scopes=('solutions:write',)):
        response = flask_app_client.patch(
            '/api/v1/solutions/latest-new',
            data=json.dumps([{'op': 'replace', 'path': '/state', 'value': 'reserved'}])
        )

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert isinstance(response.json, dict)
    assert set(response.json.keys()) >= {
        'id',
        'problem_id',
        'programming_language',
        'testing_mode',
    }
    assert response.json['id'] == solution.id
    assert response.json['problem_id'] == solution.problem_id
    assert set(response.json['programming_language'].keys()) >= {
        'name',
        'title',
        'compiler_docker_image_name',
        'executor_docker_image_name'
    }
    assert response.json['testing_mode'] == solution.testing_mode

    with flask_app_client.login(regular_user, auth_scopes=('solutions:write',)):
        response = flask_app_client.patch(
            '/api/v1/solutions/latest-new',
            data=json.dumps([{'op': 'replace', 'path': '/state', 'value': 'reserved'}])
        )
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    assert set(response.json.keys()) >= {'message'}
