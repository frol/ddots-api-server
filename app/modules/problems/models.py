# encoding: utf-8
"""
Problem database models
-----------------------
"""
import uuid

from sqlalchemy_utils import Timestamp

from app.extensions import db, seaweedfs
from app.modules.users.models import OwnerMixin


class Problem(OwnerMixin, db.Model, Timestamp):
    """
    Problem database model.
    """
    __owner_backref_name__ = 'problems'

    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text, default='', nullable=False)

    tests_seaweed_id = db.Column(db.String(length=255), default='', nullable=False)

    def __init__(self, tests_archive=None, **kwargs):
        super(Problem, self).__init__(**kwargs)
        if tests_archive is not None:
            if tests_archive.filename[-7:] != '.tar.gz':
                raise ValueError("Tests archive is not .tar.gz")
            self.tests_seaweed_id = seaweedfs.upload_file(
                stream=tests_archive,
                name='problem-tests_%s.tar.gz' % uuid.uuid4()
            )

    def __repr__(self):
        return (
            "<{class_name}("\
                "id={self.id}, "
                "title=\"{self.title}\""
                ")>".format(
                    class_name=self.__class__.__name__,
                    self=self
                )
        )

    @db.validates('title')
    def validate_title(self, key, title):  # pylint: disable=unused-argument,no-self-use
        if len(title) < 1:
            raise ValueError("Title has to be at least 1 character long.")
        return title

    @property
    def tests_archive(self):
        """
        Provides a .tar.gz tests archive for the problem.
        """
        if not self.tests_seaweed_id:
            return None
        assert seaweedfs.file_exists(self.tests_seaweed_id), (
            "Tests archive for problem %d is missing" % self.id
        )
        return seaweedfs.get_file(self.tests_seaweed_id)
