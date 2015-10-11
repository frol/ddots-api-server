# encoding: utf-8
"""
Application environment related tasks for Invoke.
"""

from invoke import ctask as task

from . import dependencies, db


@task(
    pre=(dependencies.install, db.upgrade, )
)
def enter(context):
    """
    Enter into IPython notebook shell with an initialized app.
    """
    import pprint

    from werkzeug import script
    import flask

    import app

    def shell_context():
        context = dict(pprint=pprint.pprint)
        context.update(vars(flask))
        context.update(vars(app))
        return context

    with app.app.app_context():
        script.make_shell(shell_context, use_ipython=True)()
