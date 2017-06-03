# encoding: utf-8
# pylint: disable=missing-docstring
"""
This file contains initialization data for development usage only.

You can execute this code via ``invoke app.db.init_development_data``
"""
from app.extensions import db, api

from app.modules.users.models import User
from app.modules.auth.models import OAuth2Client
from app.modules.programming_languages.models import ProgrammingLanguage


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

def init_programming_languages():
    with db.session.begin():
        db.session.add_all((
            ProgrammingLanguage(
                name='02',
                title="C / GCC",
                compiler_docker_image_name='ddots-compiler-gcc',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='18',
                title="C (C11) / GCC",
                compiler_docker_image_name='ddots-compiler-gcc11',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='03',
                title="C++ / GCC",
                compiler_docker_image_name='ddots-compiler-gxx',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='19',
                title="C++ (C++11) / GCC",
                compiler_docker_image_name='ddots-compiler-gxx11',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='20',
                title="C++ (C++14) / GCC",
                compiler_docker_image_name='ddots-compiler-gxx14',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='30',
                title="C++ (C++17) / GCC",
                compiler_docker_image_name='ddots-compiler-gxx17',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='04',
                title="Pascal (16-bit) / FreePascal",
                compiler_docker_image_name='ddots-compiler-fpc',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='39',
                title="Delphi / FreePascal",
                compiler_docker_image_name='ddots-compiler-fpc-delphi',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='16',
                title="Go",
                compiler_docker_image_name='ddots-compiler-go',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='21',
                title="Haskell",
                compiler_docker_image_name='ddots-compiler-haskell',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='22',
                title="Nim",
                compiler_docker_image_name='ddots-compiler-nim',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='23',
                title="Rust",
                compiler_docker_image_name='ddots-compiler-rust',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='14',
                title="C# / Mono",
                compiler_docker_image_name='ddots-compiler-mono',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='29',
                title="Visual Basic / Mono",
                compiler_docker_image_name='ddots-compiler-mono-basic',
                executor_docker_image_name='ddots-runner-binary',
            ),
            ProgrammingLanguage(
                name='13',
                title="Java 7 / OpenJDK",
                compiler_docker_image_name='ddots-compiler-openjdk7',
                executor_docker_image_name='ddots-runner-openjdk7',
            ),
            ProgrammingLanguage(
                name='17',
                title="Java 8 / Oracle JDK",
                compiler_docker_image_name='ddots-compiler-oraclejdk8',
                executor_docker_image_name='ddots-runner-oraclejdk8',
            ),
            ProgrammingLanguage(
                name='11',
                title="Python 2 / CPython 2",
                compiler_docker_image_name='ddots-compiler-python2',
                executor_docker_image_name='ddots-runner-python2',
            ),
            ProgrammingLanguage(
                name='12',
                title="Python 3 / CPython 3",
                compiler_docker_image_name='ddots-compiler-python3',
                executor_docker_image_name='ddots-runner-python3',
            ),
            ProgrammingLanguage(
                name='28',
                title="Python 3 + extra libs / CPython 3",
                compiler_docker_image_name='ddots-compiler-python-machinelearning',
                executor_docker_image_name='ddots-runner-python-machinelearning',
            ),
            ProgrammingLanguage(
                name='15',
                title="Ruby",
                compiler_docker_image_name='ddots-compiler-ruby',
                executor_docker_image_name='ddots-runner-ruby',
            ),
            ProgrammingLanguage(
                name='25',
                title="PHP",
                compiler_docker_image_name='ddots-compiler-php',
                executor_docker_image_name='ddots-runner-php',
            ),
            ProgrammingLanguage(
                name='27',
                title="Bash",
                compiler_docker_image_name='ddots-compiler-bash',
                executor_docker_image_name='ddots-runner-bash',
            ),
            ProgrammingLanguage(
                name='31',
                title="JavaScript / Node.js",
                compiler_docker_image_name='ddots-compiler-javascript',
                executor_docker_image_name='ddots-runner-javascript',
            ),
        ))

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
    init_programming_languages()
