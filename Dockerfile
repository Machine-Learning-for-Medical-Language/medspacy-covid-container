# currently tested with 3.8
FROM python:3.8

WORKDIR /usr/src/app

RUN mkdir /umls
COPY umls/ /umls/

RUN mkdir /quickumls

# Install QuickUMLS and MedSpaCy
RUN pip install medspacy cov_bsv
RUN pip install six

RUN git clone https://github.com/Georgetown-IR-Lab/QuickUMLS.git
RUN cd QuickUMLS && python setup.py install

RUN python -m quickumls.install /umls /quickumls
ENV QUICKUMLS_PATH=/quickumls

COPY medspacy_rest.py .
COPY medspacy_utils.py .

RUN pip install uvicorn fastapi

CMD [ "uvicorn", "medspacy_rest:app", "--host", "0.0.0.0"]
