# encoding: utf-8
# pylint: disable=invalid-name
"""
The starting point of Invoke tasks for DDOTS RESTful API Server project.
"""

import logging
import os
import sys
import sysconfig

logger = logging.getLogger()
logger.setLevel(logging.INFO)
#logging.getLogger('app').setLevel(logging.DEBUG)

try:
    import colorlog
except ImportError:
    pass
else:
    formatter = colorlog.ColoredFormatter(
        (
            '%(asctime)s '
            '[%(cyan)s%(name)s%(reset)s] '
            '[%(log_color)s%(levelname)s%(reset)s] '
            '%(message_log_color)s%(message)s'
        ),
        reset=True,
        log_colors={
            'DEBUG': 'bold_cyan',
            'INFO': 'bold_green',
            'WARNING': 'bold_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_red,bg_white',
        },
        secondary_log_colors={
            'message': {
                'DEBUG': 'white',
                'INFO': 'bold_white',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_red',
            },
        },
        style='%'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

 
from invoke import Collection
from invoke.executor import Executor

from . import app

# NOTE: `namespace` or `ns` name is required!
namespace = Collection(
    app,
)

def invoke_execute(context, command_name, **kwargs):
    """
    Helper function to make invoke-tasks execution easier.
    """
    results = Executor(namespace, config=context.config).execute((command_name, kwargs))
    target_task = context.root_namespace[command_name]
    return results[target_task]

namespace.configure({
    'root_namespace': namespace,
    'invoke_execute': invoke_execute,
})
