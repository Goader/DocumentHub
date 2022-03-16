from typing import List, Dict
from uuid import UUID
import os

from .document import Document
from ..apis import ElasticSearch
from ..apis import Translator
from ..apis import Tika


class DocumentHub:
    def __init__(self) -> None:
        self._documents: Dict[UUID, Document] = dict()

        elastic_host = os.environ['ELASTICSEARCH_HOST']
        elastic_port = os.environ['ELASTICSEARCH_PORT']

        tika_host = os.environ['TIKA_HOST']
        tika_port = os.environ['TIKA_PORT']

        translator_host = os.environ['TRANSLATOR_HOST']
        translator_key = os.environ['TRANSLATOR_KEY']

        self._elastic: ElasticSearch = ElasticSearch(elastic_host, int(elastic_port))
        self._translator: Translator = Translator(translator_host, translator_key)
        self._tika: Tika = Tika(tika_host, int(tika_port))

    @property
    def tika(self) -> Tika:
        return self._tika

    @property
    def translator(self) -> Translator:
        return self._translator

    def add_document(self, document: Document):
        self._documents[document.id] = document
        self._elastic.add(document)

    def get_document(self, id: str, lang: str = None):
        original = self._documents.get(id, None)
        if lang is None:
            return original
        
        translated = self._translator.translate(original.content, from_lang=original.language, to_lang=lang)
        document = Document(original.name, translated, lang, tags=[lang])

        return document

    def search_document(self, query: str) -> List[Document]:
        ids = self._elastic.search(query)
        # 'if' in the list comprehension is a safeguard for the documents that have been added to ElasticSearch index before the server started
        # TODO make sure the ElasticSearch and server have the same data, for example, by holding it only on the ElasticSearch node
        return [self._documents[guid] for guid in ids if guid in self._documents]
