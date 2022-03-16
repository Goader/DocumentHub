import requests


def content_type(type_: str = 'application/json'):
    return {
        'content-type': type_
    }

def GET(url: str, headers: dict = content_type(), data: dict = {}):
    return requests.get(url, headers=headers, json=data).json()


def POST(url: str, headers: dict = content_type(), data: dict = {}):
    return requests.post(url, headers=headers, json=data).json()


def PUT(url: str, headers: dict = content_type(), data: dict = {}):
    return requests.put(url, headers=headers, json=data).json()


def DELETE(url: str, headers: dict = content_type(), data: dict = {}):
    return requests.delete(url, headers=headers, json=data).json()


def PUT_binary(url: str, headers: dict = content_type('application/pdf'), data: bytes = b''):
    return requests.put(url, headers=headers, data=data)


def GET_params(url: str, headers: dict = content_type(), params: dict = {}):
    return requests.get(url, headers=headers, params=params).json()
