# encoding: utf-8
# pylint: disable=bad-continuation
"""
RESTful API Problem resources
-----------------------------
"""

import logging

from flask import Response
from flask_login import current_user
from flask_restplus._http import HTTPStatus
from flask_restplus_patched import Resource

from app.extensions import db
from app.extensions.api import Namespace, abort
from app.extensions.api.parameters import PaginationParameters
from app.modules.users import permissions
from app.modules.users.models import User


from . import parameters, schemas
from .models import Problem


log = logging.getLogger(__name__)  # pylint: disable=invalid-name
api = Namespace('problems', description="Problems")  # pylint: disable=invalid-name


@api.route('/')
@api.login_required(oauth_scopes=['problems:read'])
class Problems(Resource):
    """
    Manipulations with problems.
    """

    @api.parameters(PaginationParameters())
    @api.response(schemas.BaseProblemSchema(many=True))
    def get(self, args):
        """
        List of problems.

        Returns a list of problems starting from ``offset`` limited by ``limit``
        parameter.
        """
        return Problem.query.offset(args['offset']).limit(args['limit'])

    @api.login_required(oauth_scopes=['problems:write'])
    @api.parameters(parameters.CreateProblemParameters())
    @api.response(schemas.DetailedProblemSchema())
    @api.response(code=HTTPStatus.CONFLICT)
    @api.doc(id='create_problem')
    def post(self, args):
        """
        Create a new problem.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to create a new problem"
            ):
            problem = Problem(creator=current_user, **args)
            db.session.add(problem)
        return problem


@api.route('/<int:problem_id>')
@api.login_required(oauth_scopes=['problems:read'])
@api.response(
    code=HTTPStatus.NOT_FOUND,
    description="Problem not found.",
)
@api.resolve_object_by_model(Problem, 'problem')
class ProblemByID(Resource):
    """
    Manipulations with a specific problem.
    """

    @api.permission_required(
        permissions.OwnerRolePermission,
        kwargs_on_request=lambda kwargs: {'obj': kwargs['problem']}
    )
    @api.response(schemas.DetailedProblemSchema())
    def get(self, problem):
        """
        Get problem details by ID.
        """
        return problem

    @api.login_required(oauth_scopes=['problems:write'])
    @api.permission_required(
        permissions.OwnerRolePermission,
        kwargs_on_request=lambda kwargs: {'obj': kwargs['problem']}
    )
    @api.permission_required(permissions.WriteAccessPermission())
    @api.parameters(parameters.PatchProblemDetailsParameters())
    @api.response(schemas.DetailedProblemSchema())
    @api.response(code=HTTPStatus.CONFLICT)
    def patch(self, args, problem):
        """
        Patch problem details by ID.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to update problem details."
            ):
            parameters.PatchProblemDetailsParameters.perform_patch(args, obj=problem)
            db.session.merge(problem)
        return problem

    @api.login_required(oauth_scopes=['problems:write'])
    @api.permission_required(
        permissions.OwnerRolePermission,
        kwargs_on_request=lambda kwargs: {'obj': kwargs['problem']}
    )
    @api.permission_required(permissions.WriteAccessPermission())
    @api.response(code=HTTPStatus.CONFLICT)
    @api.response(code=HTTPStatus.NO_CONTENT)
    def delete(self, problem):
        """
        Delete a problem by ID.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to delete the problem."
            ):
            db.session.delete(problem)
        return None


@api.route('/<int:problem_id>/tests.tar.gz')
@api.login_required(oauth_scopes=['problems:read'])
@api.response(
    code=HTTPStatus.NOT_FOUND,
    description="Problem not found.",
)
@api.resolve_object_by_model(Problem, 'problem')
class ProblemTestsArchiveByID(Resource):
    """
    Manipulations with tests archive for a specific problem.
    """

    @api.permission_required(
        permissions.OwnerRolePermission,
        kwargs_on_request=lambda kwargs: {'obj': kwargs['problem']}
    )
    @api.response(schemas.ProblemTestsArchiveSchema())
    def get(self, problem):
        """
        Get problem tests archive by ID.
        """
        return Response(problem.tests_archive, mimetype='application/gzip')
