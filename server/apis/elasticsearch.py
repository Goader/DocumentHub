from ..service.document import Document
from .utils import GET, POST, PUT, DELETE


class ElasticSearch:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

        self._configure()

    @property
    def url(self):
        return f'http://{self._host}:{self._port}'

    def _url_join(self, *args):
            return '/'.join([self.url] + list(map(str, args)))

    def _configure(self, index_name: str = 'hub', analyzer_name: str = 'default'):
        self._index_name = index_name
        self._analyzer_name = analyzer_name

        # creating index  -  https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html
        PUT(self._url_join(index_name))    

        # defining analyzer  -  https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html
        POST(self._url_join(index_name, '/_close'))
        data =  {'analysis': {'analyzer': {
            analyzer_name: {
                'type': 'custom',
                'tokenizer': 'standard',
                'char_filter': ['html_strip'],
                'filter': []
            }
        }}}
        
        PUT(self._url_join(index_name, '/_settings'), data=data)
        
        analyzer_query = {'properties': {
            'text': {
                'type': 'text',
                'analyzer': analyzer_name
            }
        }}
        
        PUT(self._url_join(index_name, '/_mappings'), data=analyzer_query)
        
        POST(self._url_join(index_name, '/_open'))

    def _upload_data(self, document: Document):
        # uploading document  -  https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html
        query = {
            'text': document.content,
            'analyzer': self._analyzer_name
        }
        PUT(self._url_join(self._index_name, '_create', document.id), data=query)

    def _search(self, search_message: str):
        query = {'query': {
            'match': {
                'text': {
                    'query': ' AND '.join(search_message.split(' ')),
                    'analyzer': self._analyzer_name
                }
            }
        }}
        return GET(self._url_join(self._index_name, '_search'), data=query)


    def add(self, document: Document) -> None:
        self._upload_data(document)

    def search(self, query: str) -> Document:
        result = self._search(query)

        hits = [hit['_id'] for hit in result['hits']['hits']]

        return hits
