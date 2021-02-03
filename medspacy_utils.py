
import json
import medspacy

def doc2entlist(doc):
    ents = []
    for ent in doc.ents:
        if ent._.semtypes == -1:
            ent._.semtypes = {"COVID"}

        ent_dict = {'begin': ent.start_char,
                    'end': ent.end_char,
                    'polarity': -1 if ent._.is_negated else 1,
                    'text': str(ent),
                    'semtypes': list(ent._.semtypes),
                    'cui': ent.label_,
        }
        ents.append(ent_dict)
    
    return ents

def doc2json(doc):
    return json.dumps(doc2entlist(doc))
