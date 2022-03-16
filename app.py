from pathlib import Path
from typing import Optional
import os

from fastapi import FastAPI
from fastapi import Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.responses import RedirectResponse, FileResponse
import uvicorn
from dotenv import load_dotenv

from server.service import DocumentHub
from server.service.document import Document
from server.apis.exceptions import ServiceException


load_dotenv('.env')


app = FastAPI(
    title='DocumentsHub',
    version='1.0',
    description='Special hub for your documents allowing to search, translate and so on...'
)

api_directory = Path(__file__).parent
repository = api_directory / 'repository'
os.makedirs(repository, exist_ok=True)

hub = DocumentHub()
tika = hub.tika


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/')
@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/search')
async def search(request: Request):
    form = await request.form()
    query = form['search']

    try:
        documents = hub.search_document(query)
    except ServiceException as ex:
        return {'error': str(ex)}

    return templates.TemplateResponse('results.html', 
        {
            'request': request, 
            'results': [
                {
                    'id': document.id,
                    'name': document.name,
                    'prompt': document.content[:70]
                } for document in documents
            ]
        }
    )


@app.post('/upload')
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    # TODO there is an alternative to use tika as a detector for pdf

    try:
        if file.filename.endswith('.pdf'):
            text = tika.extract(contents)
        else:
            text = contents.decode('utf-8')

        document = Document(file.filename, text, tika.detect_language(text))
        hub.add_document(document)
    except ServiceException as ex:
        return {'error': str(ex)}


    with open(repository / document.filename, 'wb') as f:
        f.write(contents)

    return RedirectResponse('/', status_code=303)


@app.get('/download/{document_id}')
async def download(document_id: str, lang: Optional[str] = None):
    try:
        document = hub.get_document(document_id, lang=lang)
    except ServiceException as ex:
        return {'error': str(ex)}

    if document is None:
        return {'error': 'no such document, it could have been deleted by the server'}

    if lang is None:
        return FileResponse(repository / document.filename, media_type='application/octet-stream', filename=document.name)

    with open(repository / document.filename, 'wb') as f:
        f.write(document.content.encode('utf-8'))

    return FileResponse(repository / document.filename, media_type='application/octet-stream', filename=document.name)


if __name__ == '__main__':
    uvicorn.run(app=app, port=9876)
