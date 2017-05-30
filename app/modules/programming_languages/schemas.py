# encoding: utf-8
"""
Serialization schemas for Team resources RESTful API
----------------------------------------------------
"""

from flask_restplus_patched import ModelSchema

from .models import ProgrammingLanguage


class BaseProgrammingLanguageSchema(ModelSchema):

    class Meta:
        model = ProgrammingLanguage
        fields = (
                ProgrammingLanguage.name.key,
                ProgrammingLanguage.title.key,
                ProgrammingLanguage.version.key,
            )


class DetailedProgrammingLanguageSchema(BaseProgrammingLanguageSchema):

    class Meta(BaseProgrammingLanguageSchema.Meta):
        fields = BaseProgrammingLanguageSchema.Meta.fields + (
                ProgrammingLanguage.compiler_docker_image_name.key,
                ProgrammingLanguage.executor_docker_image_name.key,
            )
