# encoding: utf-8
"""
This module contains common RequestParser arguments.
"""

from flask.ext.restful import inputs
from flask.ext.restplus import reqparse


OFFSET_ARGUMENT = reqparse.Argument(
    name='offset',
    type=inputs.natural,
    default=0,
    help="Offset the list of returned results by this amount. Default is zero.",
)

LIMIT_ARGUMENT = reqparse.Argument(
    name='limit',
    type=inputs.int_range(1, 100),
    default=20,
    help="Number of items to retrieve. Default is 20, maximum is 100.",
)
