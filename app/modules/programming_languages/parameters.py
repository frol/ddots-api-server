# encoding: utf-8
"""
Input arguments (Parameters) for Programming Languages resources RESTful API
----------------------------------------------------------------------------
"""

from flask_restplus_patched import PostFormParameters, PatchJSONParameters

from .models import ProgrammingLanguage


class CreateProgrammingLanguageParameters(PostFormParameters):

    class Meta:
        model = ProgrammingLanguage
        fields = (
            ProgrammingLanguage.name.key,
            ProgrammingLanguage.title.key,
            ProgrammingLanguage.version.key,
            ProgrammingLanguage.compiler_docker_image_name.key,
            ProgrammingLanguage.executor_docker_image_name.key,
        )


class PatchProgrammingLanguageDetailsParameters(PatchJSONParameters):
    # pylint: disable=abstract-method,missing-docstring
    OPERATION_CHOICES = (
        PatchJSONParameters.OP_REPLACE,
    )

    PATH_CHOICES = tuple(
        '/%s' % field for field in (
            ProgrammingLanguage.title.key,
            ProgrammingLanguage.version.key,
            ProgrammingLanguage.compiler_docker_image_name.key,
            ProgrammingLanguage.executor_docker_image_name.key,
        )
    )
