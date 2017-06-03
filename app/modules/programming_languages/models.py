# encoding: utf-8
"""
Programming Languages database models
-------------------------------------
"""
from app.extensions import db


class ProgrammingLanguage(db.Model):
    """
    Programming Language database model.
    """
    __tablename__ = 'programming_language'

    name = db.Column(db.String(length=20), primary_key=True)
    title = db.Column(db.String(length=50), nullable=False)
    version = db.Column(db.String(length=20), default='', nullable=False)
    compiler_docker_image_name = db.Column(db.String(length=255), nullable=False)
    executor_docker_image_name = db.Column(db.String(length=255), nullable=False)
