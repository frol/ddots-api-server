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
                name='c89-gcc',
                title="C (C99) / GCC",
                compiler_docker_image_name='ddots-compiler-c89-gcc',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='c11-gcc',
                title="C (C11) / GCC",
                compiler_docker_image_name='ddots-compiler-c11-gcc',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='cxx03-gcc',
                title="C++ (C++03) / GCC",
                compiler_docker_image_name='ddots-compiler-cxx03-gcc',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='cxx11-gcc',
                title="C++ (C++11) / GCC",
                compiler_docker_image_name='ddots-compiler-cxx11-gcc',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='cxx14-gcc',
                title="C++ (C++14) / GCC",
                compiler_docker_image_name='ddots-compiler-cxx14-gcc',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='cxx17-gcc',
                title="C++ (C++17) / GCC",
                compiler_docker_image_name='ddots-compiler-cxx17-gcc',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='pascal-fpc',
                title="Pascal (16-bit) / FreePascal",
                compiler_docker_image_name='ddots-compiler-pascal-fpc',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='delphi-fpc',
                title="Delphi / FreePascal",
                compiler_docker_image_name='ddots-compiler-delphi-fpc',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='go',
                title="Go",
                compiler_docker_image_name='ddots-compiler-go',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='haskell',
                title="Haskell",
                compiler_docker_image_name='ddots-compiler-haskell',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='nim',
                title="Nim",
                compiler_docker_image_name='ddots-compiler-nim',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='rust',
                title="Rust",
                compiler_docker_image_name='ddots-compiler-rust',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='csharp-mono',
                title="C# / Mono",
                compiler_docker_image_name='ddots-compiler-csharp-mono',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='visual-basic-mono',
                title="Visual Basic / Mono",
                compiler_docker_image_name='ddots-compiler-visual-basic-mono',
                executor_docker_image_name='ddots-executor-binary',
            ),
            ProgrammingLanguage(
                name='java7-openjdk',
                title="Java 7 / OpenJDK",
                compiler_docker_image_name='ddots-compiler-java7-openjdk',
                executor_docker_image_name='ddots-executor-java7-openjdk',
            ),
            ProgrammingLanguage(
                name='java8-oraclejdk',
                title="Java 8 / Oracle JDK",
                compiler_docker_image_name='ddots-compiler-java8-oraclejdk',
                executor_docker_image_name='ddots-executor-java8-oraclejdk',
            ),
            ProgrammingLanguage(
                name='python2',
                title="Python 2 / CPython 2",
                compiler_docker_image_name='ddots-compiler-python2',
                executor_docker_image_name='ddots-executor-python2',
            ),
            ProgrammingLanguage(
                name='python3',
                title="Python 3 / CPython 3",
                compiler_docker_image_name='ddots-compiler-python3',
                executor_docker_image_name='ddots-executor-python3',
            ),
            ProgrammingLanguage(
                name='python3-extended',
                title="Python 3 + extra libs / CPython 3",
                compiler_docker_image_name='ddots-compiler-python3-extended',
                executor_docker_image_name='ddots-executor-python3-extended',
            ),
            ProgrammingLanguage(
                name='ruby',
                title="Ruby",
                compiler_docker_image_name='ddots-compiler-ruby',
                executor_docker_image_name='ddots-executor-ruby',
            ),
            ProgrammingLanguage(
                name='php',
                title="PHP",
                compiler_docker_image_name='ddots-compiler-php',
                executor_docker_image_name='ddots-executor-php',
            ),
            ProgrammingLanguage(
                name='bash',
                title="Bash",
                compiler_docker_image_name='ddots-compiler-bash',
                executor_docker_image_name='ddots-executor-bash',
            ),
            ProgrammingLanguage(
                name='javascript-nodejs',
                title="JavaScript / Node.js",
                compiler_docker_image_name='ddots-compiler-javascript-nodejs',
                executor_docker_image_name='ddots-executor-javascript-nodejs',
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
