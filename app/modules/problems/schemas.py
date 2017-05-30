# encoding: utf-8
"""
Serialization schemas for Problem resources RESTful API
-------------------------------------------------------
"""

from flask_marshmallow import base_fields
from flask_restplus_patched import ModelSchema

from .models import Problem


class BaseProblemSchema(ModelSchema):
    """
    Base problem schema exposes only the most general fields.
    """

    class Meta:
        # pylint: disable=missing-docstring
        model = Problem
        fields = (
            Problem.id.key,
            Problem.title.key,
        )
        dump_only = (
            Problem.id.key,
        )


class DetailedProblemSchema(BaseProblemSchema):
    """
    Detailed problem schema exposes all useful fields.
    """

    class Meta(BaseProblemSchema.Meta):
        fields = BaseProblemSchema.Meta.fields + (
            Problem.description.key,
            Problem.created.key,
            Problem.updated.key,
        )


class ProblemTestsArchiveSchema(base_fields.Raw):
    pass
