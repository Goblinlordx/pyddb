from assertpy import assert_that
from domain.external.exception import RollbackException, RollbackFailedException
from domain.external.transactional import (
    CommitableReversableContext,
    ReversableOperation,
    UnitOfWork,
)


class ValidTestOp(ReversableOperation):
    def up(self): ...

    def down(self): ...


class InvalidUpTestOp(ReversableOperation):
    def up(self):
        raise Exception("fail up")

    def down(self): ...


class InvalidDownTestOp(ReversableOperation):
    def up(self): ...

    def down(self):
        raise Exception("fail down")


class ExampleContext(CommitableReversableContext):
    def add(self, op: ReversableOperation):
        self._commitable_ops.append(op)


class ValidTestRepository:
    def __init__(self, context: ExampleContext):
        self._context = context

    def create(self):
        self._context.add(ValidTestOp())

    def create_fail(self):
        self._context.add(InvalidUpTestOp())

    def create_down_fail(self):
        self._context.add(InvalidDownTestOp())


class ValidUnitOfWork(UnitOfWork):
    context: ExampleContext
    valid: ValidTestRepository

    def commit(self):
        self.context.commit()

    def __enter__(self):
        self.context = ExampleContext()
        self.valid = ValidTestRepository(self.context)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context = None  # type: ignore
        self.valid = None  # type: ignore


def test_repository_should_not_raise_exception():
    unit_of_work = ValidUnitOfWork()
    with unit_of_work:
        unit_of_work.valid.create()
        unit_of_work.commit()


def test_repository_should_raise_rollback_exception():
    unit_of_work = ValidUnitOfWork()
    with unit_of_work:
        unit_of_work.valid.create_fail()

        assert_that(unit_of_work.commit).raises(RollbackException).when_called_with()


def test_repository_should_raise_rollback_failed_exception():
    unit_of_work = ValidUnitOfWork()
    with unit_of_work:
        unit_of_work.valid.create_down_fail()
        unit_of_work.valid.create_fail()

        assert_that(unit_of_work.commit).raises(
            RollbackFailedException
        ).when_called_with()
