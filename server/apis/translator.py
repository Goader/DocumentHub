from .exceptions import TranslatorException
from .utils import GET_params


class Translator:
    def __init__(self, host: str, key: str) -> None:
        self._host = host
        self._key = key

    @property
    def url(self) -> str:
        return f'https://{self._host}'

    def _url_join(self, *args):
        return '/'.join([self.url, 'v1'] + list(map(str, args)))

    def _translate(self, text: str, from_lang: str = 'en', to_lang: str = 'pl'):
        querystring = {
            'text': text,
            'from': from_lang,
            'to': to_lang
        }

        headers = {
            'x-rapidapi-host': self._host,
            'x-rapidapi-key': self._key
        }

        response = GET_params(self._url_join('translate'), headers=headers, params=querystring)

        if 'Error' in response:
            raise TranslatorException(response['Error'])

        return response['translated_text'][to_lang]

    def translate(self, text: str, from_lang: str = 'en', to_lang: str = 'pl'):
        return self._translate(text, from_lang, to_lang)
