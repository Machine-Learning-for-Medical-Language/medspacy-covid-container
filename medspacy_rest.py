from os import getenv

from fastapi import FastAPI
from pydantic import BaseModel

import medspacy
from medspacy.util import DEFAULT_PIPENAMES
from medspacy_utils import doc2json

app = FastAPI()

class Document(BaseModel):
    doc_text: str

@app.on_event("startup")
async def startup_event():
    quickumls_path_str = 'QUICKUMLS_PATH'
    quickumls_path = getenv(quickumls_path_str)
    if quickumls_path is None:
        sys.stderr.write('Error: No value for %s.\nPlease set environment variable otherwise useless default index will be used.\n' % (quickumls_path_str))
        sys.exit(-1)

    medspacy_pipes = DEFAULT_PIPENAMES.copy()

    if 'quickumls' not in medspacy_pipes: 
        medspacy_pipes.add('quickumls')
    
    app.nlp=medspacy.load(enable=medspacy_pipes, quickumls_path=quickumls_path)

@app.post("/process")
def process(doc: Document):
    doc = app.nlp(doc.doc_text)
    return doc2json(doc)

