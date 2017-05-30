# encoding: utf-8
"""
Programming Languages module
============================
"""

from app.extensions.api import api_v1


def init_app(app, **kwargs):
    # pylint: disable=unused-argument,unused-variable
    """
    Init programming languages module.
    """
    api_v1.add_oauth_scope(
        'programming_languages:read',
        "Provide access to programming language details"
    )
    api_v1.add_oauth_scope(
        'programming_languages:write',
        "Provide write access to programming language details"
    )

    # Touch underlying modules
    from . import models, resources

    api_v1.add_namespace(resources.api)
