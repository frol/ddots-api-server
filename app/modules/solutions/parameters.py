# encoding: utf-8
"""
Input arguments (Parameters) for Solution resources RESTful API
---------------------------------------------------------------
"""

from flask_marshmallow import base_fields
from flask_restplus_patched import Parameters, PostFormParameters, PatchJSONParameters
from marshmallow import validates, ValidationError

from app.modules.problems.models import Problem
from app.modules.programming_languages.models import ProgrammingLanguage
from . import schemas
from .models import Solution


class UploadSolutionParameters(PostFormParameters):

    problem_id = base_fields.Integer(required=True)
    source_code = base_fields.String(desciption="Plain text solution source code.", required=True)

    class Meta:
        model = Solution
        include_fk = True
        fields = (
            Solution.problem_id.key,
            Solution.programming_language_name.key,
            Solution.testing_mode.key,
            'source_code',
        )

    @validates(Solution.problem_id.key)
    def validate_problem_id(self, problem_id):
        # pylint: disable=unused-argument
        problem = Problem.query.filter(Problem.id == problem_id).first()
        if problem is None:
            raise ValidationError(
                "There is no problem with ID '%s'" % problem_id,
                fields=[Solution.problem_id.key]
            )

    @validates(Solution.programming_language_name.key)
    def validate_programming_language_name(self, programming_language_name):
        # pylint: disable=unused-argument
        programming_language = ProgrammingLanguage.query.filter(
            ProgrammingLanguage.name == programming_language_name
        ).first()
        if programming_language is None:
            raise ValidationError(
                "There is no programming language '%s'" % programming_language_name,
                fields=[Solution.programming_language_name.key]
            )


class PatchSolutionDetailsParameters(PatchJSONParameters):
    # pylint: disable=abstract-method,missing-docstring
    OPERATION_CHOICES = (
        PatchJSONParameters.OP_ADD,
        PatchJSONParameters.OP_REPLACE,
    )

    PATH_CHOICES = tuple(
        '/%s' % field for field in (
            Solution.state.key,
            Solution.status.key,
            Solution.scored_points.key,
            'testing_report',
        )
    )


class CreateSolutionTestingReportParameters(
        Parameters,
        schemas.SolutionTestingReportSchema
    ):
    pass
