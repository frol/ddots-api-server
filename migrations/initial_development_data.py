# encoding: utf-8
# pylint: disable=missing-docstring
"""
This file contains initialization data for development usage only.

You can execute this code via ``invoke app.db.init_development_data``
"""
from app.extensions import db, api

from app.modules.users.models import User
from app.modules.auth.models import OAuth2Client


def init_users():
    root_user = User(
        username='root',
        email='root@localhost',
        password='q',
        is_active=True,
        is_regular_user=True,
        is_admin=True
    )
    docs_user = User(
        username='documentation',
        email='documentation@localhost',
        password='w',
        is_active=False
    )
    regular_user = User(
        username='user',
        email='user@localhost',
        password='w',
        is_active=True,
        is_regular_user=True
    )
    internal_user = User(
        username='internal',
        email='internal@localhost',
        password='q',
        is_active=True,
        is_internal=True
    )
    with db.session.begin():
        db.session.add_all([
            internal_user,
            root_user,
            docs_user,
            regular_user,
        ])
    return root_user, docs_user, regular_user, internal_user

def init_auth(user_instance, client_id, client_secret):
    # TODO: OpenAPI documentation has to have OAuth2 Implicit Flow instead
    # of Resource Owner Password Credentials Flow
    oauth2_client = OAuth2Client(
        client_id=client_id,
        client_secret=client_secret,
        user_id=user_instance.id,
        redirect_uris=[],
        default_scopes=api.api_v1.authorizations['oauth2_password']['scopes']
    )
    with db.session.begin():
        db.session.add(oauth2_client)
    return oauth2_client

def init():
    # Automatically update `default_scopes` for `documentation` and `internal` OAuth2 Client,
    # as it is nice to have an ability to evaluate all available API calls.
    with db.session.begin():
        OAuth2Client.query.filter(
            (OAuth2Client.client_id == 'documentation') | (OAuth2Client.client_id == 'internal'),
        ).update({
            OAuth2Client.default_scopes: api.api_v1.authorizations['oauth2_password']['scopes'],
        })

    assert User.query.count() == 0, \
        "Database is not empty. You should not re-apply fixtures! Aborted."

    root_user, docs_user, regular_user, internal_user = init_users()  # pylint: disable=unused-variable
    init_auth(
        docs_user,
        client_id='documentation',
        client_secret='KQ()SWK)SQK)QWSKQW(SKQ)S(QWSQW(SJ*HQ&HQW*SQ*^SSQWSGQSG'
    )
    init_auth(
        internal_user,
        client_id='internal',
        client_secret='Dc5NmZmMjIzODVlZDAwNjQxNmE1NDNkMmYxNjI4N2MwY2E0NjhiMzN'
    )
