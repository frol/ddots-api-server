# encoding: utf-8
# pylint: disable=bad-continuation
"""
RESTful API Solutions resources
-------------------------------
"""
from datetime import datetime
import logging

from flask import Response
from flask_login import current_user
from flask_restplus._http import HTTPStatus
from flask_restplus_patched import Resource

from app.extensions import db, seaweedfs
from app.extensions.api import Namespace
from app.extensions.api.parameters import PaginationParameters
from app.modules.users import permissions

from . import parameters, schemas
from .models import Solution


log = logging.getLogger(__name__)  # pylint: disable=invalid-name
api = Namespace('solutions', description="Solutions")  # pylint: disable=invalid-name


@api.route('/')
@api.login_required(oauth_scopes=['solutions:read'])
class Solutions(Resource):
    """
    Manipulations with solutions.
    """

    @api.parameters(PaginationParameters())
    @api.response(schemas.BaseSolutionSchema(many=True))
    def get(self, args):
        """
        List of solutions.

        Returns a list of solutions starting from ``offset`` limited by ``limit``
        parameter.
        """
        return Solution.query.offset(args['offset']).limit(args['limit'])

    @api.login_required(oauth_scopes=['solutions:write'])
    @api.parameters(parameters.UploadSolutionParameters())
    @api.response(schemas.DetailedSolutionSchema())
    @api.response(code=HTTPStatus.CONFLICT)
    @api.doc(id='send_solution')
    def post(self, args):
        """
        Upload a new solution.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to create a new solution"
            ):
            solution = Solution(author=current_user, **args)
            db.session.add(solution)
        return solution


@api.route('/latest-new')
@api.login_required(oauth_scopes=['solutions:write'])
class SolutionForTesting(Resource):
    """
    Fetch a solution for testing.
    """

    @api.response(schemas.TestingSolutionSchema())
    def patch(self):
        """
        Fetch a solution for testing.

        Return a solution and reserve it for testing.
        """
        while 1:
            solution = Solution.query.filter(Solution.state == Solution.States.new).first()
            if solution is None:
                raise api.abort(404, message="There is no new solutions.")

            if Solution.query\
                    .filter(Solution.state == Solution.States.new)\
                    .filter(Solution.id == solution.id)\
                    .update(
                        {
                            'state': Solution.States.reserved,
                            'updated': datetime.utcnow(),
                        },
                        synchronize_session=False
                    ) == 1:
                break
        return solution


@api.route('/<int:solution_id>')
@api.login_required(oauth_scopes=['solutions:read'])
@api.response(
    code=HTTPStatus.NOT_FOUND,
    description="Solution not found.",
)
@api.resolve_object_by_model(Solution, 'solution')
class SolutionByID(Resource):
    """
    Manipulations with a specific solution.
    """

    @api.permission_required(
        permissions.OwnerRolePermission,
        kwargs_on_request=lambda kwargs: {'obj': kwargs['solution']}
    )
    @api.response(schemas.DetailedSolutionSchema())
    def get(self, solution):
        """
        Get solution details by ID.
        """
        return solution

    @api.login_required(oauth_scopes=['solutions:write'])
    @api.permission_required(
        permissions.OwnerRolePermission,
        kwargs_on_request=lambda kwargs: {'obj': kwargs['solution']}
    )
    @api.permission_required(permissions.WriteAccessPermission())
    @api.parameters(parameters.PatchSolutionDetailsParameters())
    @api.response(schemas.DetailedSolutionSchema())
    @api.response(code=HTTPStatus.CONFLICT)
    def patch(self, args, solution):
        """
        Patch solution details by ID.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to update solution details."
            ):
            parameters.PatchSolutionDetailsParameters.perform_patch(args, obj=solution)
            db.session.merge(solution)
        return solution

    @api.login_required(oauth_scopes=['solutions:write'])
    @api.permission_required(
        permissions.OwnerRolePermission,
        kwargs_on_request=lambda kwargs: {'obj': kwargs['Solution']}
    )
    @api.permission_required(permissions.WriteAccessPermission())
    @api.response(code=HTTPStatus.CONFLICT)
    @api.response(code=HTTPStatus.NO_CONTENT)
    def delete(self, solution):
        """
        Delete a solution by ID.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to delete the solution."
            ):
            db.session.delete(solution)
        return None


@api.route('/<int:solution_id>/source-code')
@api.login_required(oauth_scopes=['solutions:read'])
@api.response(
    code=HTTPStatus.NOT_FOUND,
    description="Solution not found.",
)
@api.resolve_object_by_model(Solution, 'solution')
class SolutionSourceCodeByID(Resource):
    """
    Manipulations with source code of a specific solution.
    """

    @api.permission_required(
        permissions.OwnerRolePermission,
        kwargs_on_request=lambda kwargs: {'obj': kwargs['solution']}
    )
    @api.response(schemas.SolutionSourceCodeSchema())
    def get(self, solution):
        """
        Get solution source code by ID.
        """
        return Response(solution.source_code, mimetype='plain/text')


@api.route('/<int:solution_id>/testing-report')
@api.login_required(oauth_scopes=['solutions:read'])
@api.response(
    code=HTTPStatus.NOT_FOUND,
    description="Solution not found.",
)
@api.resolve_object_by_model(Solution, 'solution')
class SolutionTestingReportByID(Resource):
    """
    Manipulations with a report of a specific solution.
    """

    @api.login_required(oauth_scopes=['solutions:write'])
    @api.permission_required(
        permissions.OwnerRolePermission,
        kwargs_on_request=lambda kwargs: {'obj': kwargs['solution']}
    )
    @api.parameters(parameters.CreateSolutionTestingReportParameters(), locations=('json',))
    @api.response(schemas.BaseSolutionSchema())
    @api.response(code=HTTPStatus.CONFLICT)
    def post(self, args, solution):
        """
        Send a testing report for the solution.
        """
        if Solution.query\
                .filter(Solution.state == Solution.States.received)\
                .filter(Solution.id == solution.id)\
                .update({
                    'state': Solution.States.tested,
                    'updated': datetime.utcnow(),
                }) != 1:
            api.abort(HTTPStatus.NOT_FOUND)
        try:
            with api.commit_or_abort(
                    db.session,
                    default_error_message="Failed to save the testing report"
                ):
                solution.testing_report_seaweed_id = seaweedfs.upload_file(
                        stream=schemas.SolutionTestingReportSchema().dumps(args).data,
                        name="solution_%d-testing_report.json" % solution.id
                    )
                db.session.merge(solution)
        except Exception:
            log.exception(
                    "Something went wrong during testing report saving... Solution: %r",
                    solution
                )
            Solution.query\
                .filter(Solution.id == solution.id)\
                .update({
                    'state': Solution.States.new,
                    'updated': datetime.utcnow(),
                })
            raise
        return solution
