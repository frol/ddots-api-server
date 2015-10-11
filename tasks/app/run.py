# encoding: utf-8
"""
Application execution related tasks for Invoke.
"""

from invoke import ctask as task

from . import dependencies, db


@task(
    default=True,
    pre=(dependencies.install, db.upgrade, )
)
def run(context, host='127.0.0.1', port=5000, debug=True):
    """
    Run DDOTS RESTful API Server.
    """
    from app import app
    app.run(host=host, port=port, debug=debug)
