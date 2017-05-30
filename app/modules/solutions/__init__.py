# encoding: utf-8
"""
Solutions module
================
"""

from app.extensions.api import api_v1


def init_app(app, **kwargs):
    # pylint: disable=unused-argument,unused-variable
    """
    Init solutions module.
    """
    api_v1.add_oauth_scope('solutions:read', "Provide access to solution details")
    api_v1.add_oauth_scope('solutions:write', "Provide write access to solution details")

    # Touch underlying modules
    from . import models, resources

    api_v1.add_namespace(resources.api)
