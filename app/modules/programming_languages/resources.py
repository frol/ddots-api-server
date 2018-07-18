# encoding: utf-8
# pylint: disable=bad-continuation
"""
RESTful API ProgrammingLanguages resources
-------------------------------
"""
from flask_restplus._http import HTTPStatus
from flask_restplus_patched import Resource

from app.extensions import db
from app.extensions.api import Namespace
from app.extensions.api.parameters import PaginationParameters
from app.modules.users import permissions

from . import parameters, schemas
from .models import ProgrammingLanguage


api = Namespace('programming-languages', description="Programming Languages")


@api.route('/')
@api.login_required(oauth_scopes=['programming_languages:read'])
class ProgrammingLanguages(Resource):
    """
    Manipulations with programming_languages.
    """

    @api.parameters(PaginationParameters())
    @api.response(schemas.BaseProgrammingLanguageSchema(many=True))
    def get(self, args):
        """
        List of programming languages.

        Returns a list of programming languages starting from ``offset`` limited by ``limit``
        parameter.
        """
        return ProgrammingLanguage.query.offset(args['offset']).limit(args['limit'])

    @api.login_required(oauth_scopes=['programming_languages:write'])
    @api.parameters(parameters.CreateProgrammingLanguageParameters())
    @api.response(schemas.DetailedProgrammingLanguageSchema())
    @api.response(code=HTTPStatus.CONFLICT)
    def post(self, args):
        """
        Upload a new programming language.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to create a new programming language"
            ):
            programming_language = ProgrammingLanguage(**args)
            db.session.add(programming_language)
        return programming_language


@api.route('/<programming_language_name>')
@api.login_required(oauth_scopes=['programming_languages:read'])
@api.response(
    code=HTTPStatus.NOT_FOUND,
    description="Programming language not found.",
)
@api.resolve_object_by_model(
    ProgrammingLanguage,
    'programming_language',
    'programming_language_name'
)
class ProgrammingLanguageByName(Resource):
    """
    Manipulations with a specific programming language.
    """

    @api.permission_required(permissions.AdminRolePermission())
    @api.response(schemas.DetailedProgrammingLanguageSchema())
    def get(self, programming_language):
        """
        Get programming language details by ID.
        """
        return programming_language

    @api.login_required(oauth_scopes=['programming_languages:write'])
    @api.permission_required(permissions.AdminRolePermission())
    @api.permission_required(permissions.WriteAccessPermission())
    @api.parameters(parameters.PatchProgrammingLanguageDetailsParameters())
    @api.response(schemas.DetailedProgrammingLanguageSchema())
    @api.response(code=HTTPStatus.CONFLICT)
    def patch(self, args, programming_language):
        """
        Patch programming language details by name.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to update programming language details."
            ):
            parameters.PatchProgrammingLanguageDetailsParameters.perform_patch(
                args,
                obj=programming_language
            )
            db.session.merge(programming_language)
        return programming_language

    @api.login_required(oauth_scopes=['programming_languages:write'])
    @api.permission_required(permissions.AdminRolePermission())
    @api.permission_required(permissions.WriteAccessPermission())
    @api.response(code=HTTPStatus.CONFLICT)
    @api.response(code=HTTPStatus.NO_CONTENT)
    def delete(self, programming_language):
        """
        Delete a programming language by ID.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to delete the programming language."
            ):
            db.session.delete(programming_language)
        return None
