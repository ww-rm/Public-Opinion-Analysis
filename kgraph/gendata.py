import pandas as pd
import spacy
from spacy.matcher import Matcher
from tqdm import tqdm

KG_NLP = spacy.load('en_core_web_sm')


def get_entities(sent):
    ent1 = ""
    ent2 = ""
    prv_tok_dep = ""
    prv_tok_text = ""
    prefix = ""
    modifier = ""

    for tok in KG_NLP(sent):
        if tok.dep_ != "punct":
            if tok.dep_ == "compound":
                prefix = tok.text
                if prv_tok_dep == "compound":
                    prefix = prv_tok_text + " " + tok.text

            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                if prv_tok_dep == "compound":
                    modifier = prv_tok_text + " " + tok.text

            if tok.dep_.find("subj") == True:
                ent1 = modifier + " " + prefix + " " + tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = ""

            if tok.dep_.find("obj") == True:
                ent2 = modifier + " " + prefix + " " + tok.text

            prv_tok_dep = tok.dep_
            prv_tok_text = tok.text

    return [ent1.strip(), ent2.strip()]


def gen_source_target(sents) -> tuple:
    """
    Returns:
        (source, target)
    """
    entity_pairs = []
    for i in tqdm(sents):
        entity_pairs.append(get_entities(i))
    source = [i[0] for i in entity_pairs]
    target = [i[1] for i in entity_pairs]
    return (source, target)


def get_relation(sent):
    doc = KG_NLP(sent)
    matcher = Matcher(KG_NLP.vocab)

    pattern = [{'DEP': 'ROOT'}, {'DEP': 'prep', 'OP': "?"}, {'DEP': 'agent', 'OP': "?"}, {'POS': 'ADJ', 'OP': "?"}]
    matcher.add("matching_1", [pattern])

    matches = matcher(doc)
    if len(matches) <= 0:
        return ""

    k = len(matches) - 1
    span = doc[matches[k][1]:matches[k][2]]
    return(span.text)


def gen_relations(sents) -> list:
    return [get_relation(i) for i in tqdm(sents)]


def gen_kg(sents: list) -> pd.DataFrame:
    """
    Args:
        sents: A list of sentences

    Returns:
        pd.DataFrame: (source, target, relations)
    """
    source, target = gen_source_target(sents)
    relations = gen_relations(sents)
    result = {'source': [], 'target': [], 'edge': []}
    for s, t, r in zip(source, target, relations):
        if s and t and r:
            result['source'].append(s)
            result['target'].append(t)
            result['edge'].append(r)

    kg_df = pd.DataFrame(result)
    return kg_df
