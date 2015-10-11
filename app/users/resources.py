# encoding: utf-8
"""
Users API resources
"""
import six

#from flask.ext.oauthlib.provider import OAuth2Provider
from flask.ext.restplus import Resource, fields
from sqlalchemy import exc as sqlalchemy_exceptions

from app import api, api_errors_definitions
from app._common import reqparse as common_reqparse

from .models import db, User

namespace = api.namespace('users', description="Users")
#oauth = OAuth2Provider()


BASE_USER_DEFINITION = api.model('base_user', {
    User.id.key: fields.Integer(required=True, description="ID"),
    User.username.key: fields.String(required=True, description="Username"),
    #User.first_name.key: fields.String(required=True, description="First name"),
    #User.last_name.key: fields.String(required=True, description="Last name"),
})

DETAILED_USER_DEFINITION = api.inherit('detailed_user', BASE_USER_DEFINITION, {
    User.email.key: fields.String(required=True, description="E-mail"),
})


@namespace.route('/')
class Users(Resource):
    """
    Manipulations with users.
    """
    _list_parser = api.parser()
    _list_parser.add_argument(common_reqparse.OFFSET_ARGUMENT)
    _list_parser.add_argument(common_reqparse.LIMIT_ARGUMENT)
    # TODO: Add sorting

    @api.doc(parser=_list_parser)
    @api.marshal_list_with(BASE_USER_DEFINITION)
    #@oauth.require_oauth()
    def get(self):
        """
        List of users.

        Returns a list of users starting from ``offset`` limited by ``limit``
        parameter.
        """
        args = self._list_parser.parse_args()
        return User.query.all()[args.offset: args.offset + args.limit]

    _new_user_parser = api.parser()
    _new_user_parser.add_argument('username', location='form', required=True)
    _new_user_parser.add_argument('email', location='form', required=True)
    _new_user_parser.add_argument('recaptcha_key', location='form', required=True)

    @api.doc(parser=_new_user_parser)
    @api.marshal_with(DETAILED_USER_DEFINITION)
    def post(self):
        """
        Create a new user.
        """
        args = self._new_user_parser.parse_args()
        recaptcha_key = args.pop('recaptcha_key')
        if recaptcha_key != 'secret_key':
            api.abort(403, "CAPTCHA key is incorrect")
        new_user = User(**args)
        db.session.add(new_user)
        try:
            db.session.commit()
        except sqlalchemy_exceptions.IntegrityError:
            db.session.rollback()
            api.abort(409, "Error was raised while creating a new user.")
        return new_user


@namespace.route('/<int:user_id>')
@api.doc(
    params={
        'user_id': 'The User ID',
    },
    responses={
        404: ("User not found", api_errors_definitions[404]),
    },
)
class UserByID(Resource):
    """
    Manipulations with a specific user.
    """

    @api.marshal_with(DETAILED_USER_DEFINITION)
    def get(self, user_id):
        """
        Find a user by ID.
        """
        return User.query.get_or_404(user_id)
