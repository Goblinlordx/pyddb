from pydantic import BaseModel


class UserCreateCommand(BaseModel):
    email: str


class UserCreateCommandResult(BaseModel):
    id: str


class UserDeleteCommand(BaseModel):
    id: str


class UserDeleteCommandResult(BaseModel): ...
