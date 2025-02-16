import arguably
from adapter.outbound.aws_unit_of_work import AWSUnitOfWork
from domain.user.model import User


@arguably.command
def ping():
    print("pong")


@arguably.command
def asdf():
    unit_of_work = AWSUnitOfWork()
    with unit_of_work:
        unit_of_work.users.create(User("1", "asdf@asdf.com"))
        unit_of_work.commit()


@arguably.command
def qwer():
    unit_of_work = AWSUnitOfWork()
    with unit_of_work:
        unit_of_work.users.delete(User("1", "asdf@asdf.com"))
        unit_of_work.commit()


if __name__ == "__main__":
    arguably.run()
