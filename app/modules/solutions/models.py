# encoding: utf-8
"""
Solutions database models
-------------------------
"""
import enum
import json
import logging
import uuid

import sqlalchemy
from sqlalchemy_utils import Timestamp, ScalarListType

from app.extensions import db, seaweedfs
from app.modules.users.models import OwnerMixin
from app.modules.problems.models import Problem
from app.modules.programming_languages.models import ProgrammingLanguage

log = logging.getLogger(__name__)


class Solution(OwnerMixin, db.Model, Timestamp):
    """
    Solution database model.
    """
    __owner_backref_name__ = 'solutions'

    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name

    author_id = sqlalchemy.orm.synonym('creator_id')
    author = sqlalchemy.orm.synonym('creator')

    problem_id = db.Column(db.Integer, db.ForeignKey(Problem.id), nullable=False)
    problem = db.relationship(
            Problem,
            backref=db.backref('solutions', cascade='delete, delete-orphan')
        )

    programming_language_name = db.Column(
            db.String(length=20),
            db.ForeignKey(ProgrammingLanguage.name),
            nullable=False
        )
    programming_language = db.relationship(
            ProgrammingLanguage,
            backref=db.backref('solutions', cascade='delete, delete-orphan')
        )

    class TestingModes(str, enum.Enum):
        one = 'one'
        first_fail = 'first_fail'
        full = 'full'

    testing_mode = db.Column(db.Enum(TestingModes), default=TestingModes.full, nullable=False)

    class States(str, enum.Enum):
        """
        These are the states in which solution may stay.
        """
        new = 'new'
        reserved = 'reserved'
        received = 'received'
        tested = 'tested'
        rejected = 'rejected'

    state = db.Column(db.Enum(States), default=States.new, nullable=False)

    class Statuses(str, enum.Enum):
        # pylint: disable=invalid-name
        """
        These are the testing system verdicts.
        """
        OK = 'OK'

        CE = 'Compilation Error'

        # These are not real statuses, so it is better to consider using a
        # single status code for internal errors, and provide further details
        # in the report.
        NC = 'No Checker'
        CC = 'Checker Crash'
        CT = 'Checker Time Limit Exceeded'

        PE = 'Presentation Error'
        WA = 'Wrong Answer'
        RE = 'Runtime Error'
        TLE = 'Time Limit Exceeded'
        MLE = 'Memory Limit Exceeded'

        FF = 'Forbidden Function Detected'

        UE = 'Unknown Error'

    status = db.Column(ScalarListType(separator=' '), default=[], nullable=False)
    scored_points = db.Column(db.Numeric(precision=3), default=0, nullable=False)

    source_code_seaweed_id = db.Column(db.String(length=255), default='', nullable=False)
    testing_report_seaweed_id = db.Column(db.String(length=255), default='', nullable=False)

    def __init__(self, source_code=None, **kwargs):
        super(Solution, self).__init__(**kwargs)
        if source_code is not None:
            self.source_code_seaweed_id = seaweedfs.upload_file(
                stream=source_code,
                name='solution-source-code_%s.tar.gz' % uuid.uuid4()
            )

    def __repr__(self):
        return (
            "<{class_name}(" \
                "id={self.id}, "
                "programming_language={self.programming_language_name}, "
                "testing_mode={self.testing_mode}, "
                "state={self.state}, "
                "status={self.status}, "
                "scored_points={self.scored_points}"
                ")>".format(
                    class_name=self.__class__.__name__,
                    self=self
                )
        )

    @db.validates('status')
    def validate_status(self, key, status):
        # pylint: disable=unused-argument
        """
        Ensure that the list contains only the valid statuses.
        """
        if not all(each_status in self.Statuses for each_status in status):
            raise ValueError("Some of the statuses (`%r`) are not supported" % (status, ))
        return status

    @property
    def source_code(self):
        """
        Get the solution source code as a string.
        """
        assert self.source_code_seaweed_id
        if not seaweedfs.file_exists(self.source_code_seaweed_id):
            log.error("Source code is missing for solution #%d", self.id)
            return ''
        return seaweedfs.get_file(self.source_code_seaweed_id)

    @property
    def testing_report(self):
        """
        Get a testing report for the solution.

        Returns:
            dict: testing report (the dict structure follows
            :class:``schemas.TestingReportSchema``).
        """
        if not self.testing_report_seaweed_id:
            return None
        if not seaweedfs.file_exists(self.testing_report_seaweed_id):
            log.error("Testing report is missing for solution #%d", self.id)
            return None
        return json.loads(seaweedfs.get_file(self.testing_report_seaweed_id))
