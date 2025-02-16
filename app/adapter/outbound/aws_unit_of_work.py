from adapter.outbound.dynamodb.dynamodb_context import DynamoDBContext
from adapter.outbound.dynamodb.repositories import DynamoDBUserRepository
from domain.external.transactional import UnitOfWork
from mypy_boto3_dynamodb import DynamoDBClient


class AWSUnitOfWork(UnitOfWork):
    _dynamo_context: DynamoDBContext

    def __init__(self, dynamo_client: DynamoDBClient, table_name: str):
        self.dynamo_client = dynamo_client
        self.table_name = table_name

    def commit(self):
        self._dynamo_context.commit()

    def __enter__(self):
        self._dynamo_context = DynamoDBContext(self.dynamo_client, self.table_name)
        self.users = DynamoDBUserRepository(self._dynamo_context)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context = None  # type: ignore
        self.users = None  # type: ignore
