from dataclasses import dataclass


@dataclass
class Index:
    name: str
    pk: str
    sk: str


class SingleTableIndexManager:
    def __init__(
        self,
    ) -> None: ...
