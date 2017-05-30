# encoding: utf-8
import pytest


@pytest.yield_fixture()
def problem(db, regular_user):
    from app.modules.problems.models import Problem

    problem = Problem(title="Problem 1", tests_seaweed_id='5,1010101010', creator=regular_user)
    with db.session.begin():
        db.session.add(problem)

    yield problem

    # Cleanup
    with db.session.begin():
        db.session.delete(problem)


@pytest.yield_fixture()
def programming_language_c(db):
    from app.modules.programming_languages.models import ProgrammingLanguage

    programming_language_c = ProgrammingLanguage(
        name='c',
        title="C",
        compiler_docker_image_name='compiler',
        executor_docker_image_name='compiler',
    )
    with db.session.begin():
        db.session.add(programming_language_c)

    yield programming_language_c

    # Cleanup
    with db.session.begin():
        db.session.delete(programming_language_c)


@pytest.yield_fixture()
def solution(db, regular_user, problem, programming_language_c):
    from app.modules.solutions.models import Solution

    solution = Solution(
        author=regular_user,
        problem=problem,
        programming_language=programming_language_c,
        source_code_seaweed_id='3,1010101010'
    )
    with db.session.begin():
        db.session.add(solution)

    yield solution

    # Cleanup
    with db.session.begin():
        db.session.delete(solution)
