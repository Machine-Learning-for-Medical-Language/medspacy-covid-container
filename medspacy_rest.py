from os import getenv
import sys

from fastapi import FastAPI
from pydantic import BaseModel

import medspacy
from medspacy.util import DEFAULT_PIPENAMES
from medspacy_utils import doc2json
from quickumls.spacy_component import SpacyQuickUMLS
import cov_bsv

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

    nlp = cov_bsv.load()
    quickumls_component = SpacyQuickUMLS(nlp, quickumls_path)
    nlp.add_pipe(quickumls_component)
    app.nlp = nlp

@app.post("/process")
def process(doc: Document):
    doc = app.nlp(doc.doc_text)
    return doc2entlist(doc)

