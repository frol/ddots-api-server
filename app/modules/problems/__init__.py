# encoding: utf-8
"""
Problems module
===============
"""

from app.extensions.api import api_v1


def init_app(app, **kwargs):
    # pylint: disable=unused-argument,unused-variable
    """
    Init problems module.
    """
    api_v1.add_oauth_scope('problems:read', "Provide access to problem details")
    api_v1.add_oauth_scope('problems:write', "Provide write access to problem details")

    # Touch underlying modules
    from . import models, resources

    api_v1.add_namespace(resources.api)
