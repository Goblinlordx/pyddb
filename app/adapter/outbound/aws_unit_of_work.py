from adapter.outbound.dynamodb.dynamodb_context import DynamoDBContext
from adapter.outbound.dynamodb.repositories import DynamoDBUserRepository
from domain.external.transactional import UnitOfWork


class AWSUnitOfWork(UnitOfWork):
    _ddb_context: DynamoDBContext

    def commit(self):
        self._ddb_context.commit()

    def __enter__(self):
        self._ddb_context = DynamoDBContext()
        self.users = DynamoDBUserRepository(self._ddb_context)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context = None  # type: ignore
        self.users = None  # type: ignore
