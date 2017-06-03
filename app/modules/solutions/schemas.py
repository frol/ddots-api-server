# encoding: utf-8
"""
Serialization schemas for Team resources RESTful API
----------------------------------------------------
"""

from flask_marshmallow import base_fields, base_fields
from flask_restplus_patched import ModelSchema, Schema
from marshmallow import MarshalResult

from app.modules.problems.schemas import BaseProblemSchema
from app.modules.programming_languages.schemas import (
    BaseProgrammingLanguageSchema,
    DetailedProgrammingLanguageSchema
)
from app.modules.users.schemas import BaseUserSchema

from .models import Solution


class TestingSolutionSchema(ModelSchema):
    """
    Solution schema includes the fields that are exposed to the testing servers.
    """

    programming_language = base_fields.Nested(DetailedProgrammingLanguageSchema)

    class Meta:
        model = Solution
        include_fk = True
        fields = (
                Solution.id.key,
                Solution.problem_id.key,
                Solution.programming_language.key,
                Solution.testing_mode.key,
            )


class BaseSolutionSchema(ModelSchema):
    """
    Base solution schema exposes only the most general fields.
    """

    author = base_fields.Nested(BaseUserSchema)
    problem = base_fields.Nested(BaseProblemSchema)
    programming_language = base_fields.Nested(BaseProgrammingLanguageSchema)
    scored_points = base_fields.Decimal(places=3, as_string=True)
    status = base_fields.List(base_fields.String())

    class Meta:
        model = Solution
        fields = (
                Solution.id.key,
                Solution.author.key,
                Solution.problem.key,
                Solution.programming_language.key,
                Solution.created.key,
                Solution.state.key,
                Solution.status.key,
                Solution.scored_points.key,
            )


class SolutionTestingReportTestSchema(Schema):
    status = base_fields.String(required=True)
    execution_time = base_fields.Float(required=True)
    memory_peak = base_fields.Float(required=True)
    extra = base_fields.Dict()


class SolutionTestingReportSchema(Schema):
    status = base_fields.String()
    message = base_fields.String()
    tests = base_fields.Nested(SolutionTestingReportTestSchema, many=True)


class DetailedSolutionSchema(BaseSolutionSchema):
    """
    Detailed solution schema exposes all useful fields.
    """
    testing_report = base_fields.Nested(SolutionTestingReportSchema)

    class Meta(BaseSolutionSchema.Meta):
        fields = BaseSolutionSchema.Meta.fields + (
            Solution.testing_mode.key,
            Solution.updated.key,
            Solution.testing_report.fget.__name__,
        )


class SolutionSourceCodeSchema(base_fields.Raw):
    pass
