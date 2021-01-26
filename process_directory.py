import sys
from os import listdir, getenv
from os.path import isfile, join

import spacy
import medspacy
from medspacy.util import DEFAULT_PIPENAMES
from medspacy_utils import doc2json

def main(args):
    if len(args) < 2:
        sys.stderr.write('Required argument(s): <input directory> <output directory>\n')
        sys.exit(-1)

    quickumls_path_str = 'QUICKUMLS_PATH'
    quickumls_path = getenv(quickumls_path_str)
    if quickumls_path is None:
        sys.stderr.write('Error: No value for %s.\nPlease set environment variable otherwise useless default index will be used.\n' % (quickumls_path_str))
        sys.exit(-1)

    txt_files = [f for f in listdir(args[0]) if isfile(join(args[0], f)) and f.endswith('.txt')]
    
    medspacy_pipes = DEFAULT_PIPENAMES.copy()

    if 'quickumls' not in medspacy_pipes: 
        medspacy_pipes.add('quickumls')
    
    nlp=medspacy.load(enable=medspacy_pipes, quickumls_path=quickumls_path)

    for fn in txt_files:
        with open(join(args[0], fn)) as f:
            text = f.read()
            doc = nlp(text)
            
            with open(join(args[1], fn + ".json"), 'wt') as fout:
                fout.write(doc2json(doc))


    
if __name__ == '__main__':
    main(sys.argv[1:])
