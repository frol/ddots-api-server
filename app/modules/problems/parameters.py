# encoding: utf-8
"""
Input arguments (Parameters) for Problem resources RESTful API
--------------------------------------------------------------
"""

from flask_marshmallow import base_fields
from flask_restplus_patched import PostFormParameters, PatchJSONParameters

from . import schemas
from .models import Problem


class CreateProblemParameters(PostFormParameters, schemas.BaseProblemSchema):
    # pylint: disable=missing-docstring

    tests_archive = base_fields.Field(
        description="`.tar.gz` archive with Problem.xml and related files.",
        type='file',
        location='files',
        required=True
    )

    class Meta(schemas.BaseProblemSchema.Meta):
        fields = (
            Problem.title.key,
            Problem.description.key,
            'tests_archive',
        )
        # This is not supported yet: https://github.com/marshmallow-code/marshmallow/issues/344
        required = (
            Problem.title.key,
        )


class PatchProblemDetailsParameters(PatchJSONParameters):
    # pylint: disable=abstract-method,missing-docstring
    OPERATION_CHOICES = (
        PatchJSONParameters.OP_REPLACE,
    )

    PATH_CHOICES = tuple(
        '/%s' % field for field in (
            Problem.title.key,
        )
    )
