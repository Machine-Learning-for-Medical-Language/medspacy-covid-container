# medspacy-covid-container

To build this container, you need to create a sub-directory called umls/ that has two files from a UMLS installation, MRCONSO.RRF and MRSTY.RRF.

Once it has built, a demo REST application can be started with ./start_docker.sh, which will open a port at 8000 that listens for new documents, processes them, and sends back a JSON file with extracted concepts:

```
import requests
sent = 'The patient is suffering from knee pain and recently contracted COVID-19, she will begin taking ibuprofen.'
url='http://localhost:8000/process'
r = requests.post(url, json={'doc_text':sent})
print(r.json())
```

The script process_directory.py is not currently inside the container but can be copied in and used as a way to batch process multiple files in a directory and write out json. 

The script medspacy_utils.py has a few methods for interpreting the output of MedSpaCy that correspond to output we got from other projects, but may also give some insight into how to make use of the processed documents.
