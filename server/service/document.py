from uuid import UUID, uuid4
from pathlib import Path
from typing import List


class Document:
    def __init__(self, name: str, content: str, language: str, tags: List[str] = None) -> None:
        if tags is None:
            tags = []

        self._id: UUID = uuid4()  # maybe change this to the id ElasticSearch uses

        name, extension = name.rsplit('.', maxsplit=1)

        # name: <original-name>-<tags>.<extension>
        self._name: str = name + '-' * (len(tags) > 0) + "-".join(tags) + '.' + extension
        self._content: str = content  # maybe this should be kept in the ElasticSearch

        self._language: str = language

        self._filename: str = f'{name}-{self.id}.{extension}'

    @property
    def id(self) -> str:
        return str(self._id)

    @property
    def name(self) -> str:
        return self._name

    @property
    def content(self) -> str:
        return self._content    

    @property
    def language(self) -> str:
        return self._language

    @property
    def filename(self) -> str:
        return self._filename
