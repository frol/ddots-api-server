# encoding: utf-8
"""
API extension
=============
"""

from copy import deepcopy

from flask import Blueprint, current_app

from .api import Api
from .namespace import Namespace
from .http_exceptions import abort


api_v1 = Api( # pylint: disable=invalid-name
    version='1.x.y',
    title="DDOTS RESTful API Server",
    description=(
        "## Explore the demo server\n\n"
        "I suggest you start with signing up a new user. To do so, use `POST /users/` endpoint "
        "with `recaptcha_key=\"secret_key\"`.\n\n"
        "You will need to know the API Client ID to authenticate, so here it is: "
        "`documentation`. Sometimes (e.g. for token refreshing) you might need API "
        "Client Secret: `KQ()SWK)SQK)QWSKQW(SKQ)S(QWSQW(SJ*HQ&HQW*SQ*^SSQWSGQSG`.\n\n"
        "There are also two built-in users:\n"
        "* `root` (administrator with all permissions) with password `q`\n"
        "* `user` (regular user) with password `w`\n"
    ),
)


def serve_swaggerui_assets(path):
    """
    Swagger-UI assets serving route.
    """
    if not current_app.debug:
        import warnings
        warnings.warn(
            "/swaggerui/ is recommended to be served by public-facing server (e.g. NGINX)"
        )
    from flask import send_from_directory
    return send_from_directory('../static/', path)


def init_app(app, **kwargs):
    # pylint: disable=unused-argument
    """
    API extension initialization point.
    """
    app.route('/swaggerui/<path:path>')(serve_swaggerui_assets)

    api_v1.version = app.config['VERSION']
    # Prevent config variable modification with runtime changes
    api_v1.authorizations = deepcopy(app.config['AUTHORIZATIONS'])
