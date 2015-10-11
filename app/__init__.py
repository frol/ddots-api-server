# encoding: utf-8
# pylint: disable=invalid-name
"""
DDOTS RESTful API Server application.
"""
import os

from flask import Flask, Blueprint
from flask.ext.restplus import Api, Resource, fields

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % (
    os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "ddots.db"
    )
)

class MigrateConfig(object):
    def __init__(self, database, directory='migrations', **kwargs):
        self.db = database
        self.directory = directory
        self.configure_args = kwargs

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(
    api_v1,
    version='1.0',
    title="DDOTS API",
    description="Dockerized Distributed Olympiad Testing System API",
)
app.register_blueprint(api_v1)

api_errors_definitions = {
    404: api.model(
        'error_404',
        {
            'message': fields.String(required=True),
        }
    ),
}

def mount_modules():
    from flask.ext.sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    app.extensions['migrate'] = MigrateConfig(db)

    #from . import auth
    #auth.models.db.init_app(app)
    #auth.views.oauth.init_app(app)
    #app.register_blueprint(auth.views.auth_blueprint)
    
    from . import users
    users.models.db.init_app(app)
    
    from . import problems
    #problems.models.db.init_app(app)


mount_modules()
