from collections import defaultdict, namedtuple
from itertools import product
from operator import attrgetter

from spacy.tokens import Span, Token


SVOTriple = namedtuple("SVOTriple", ["s", "v", "o"])


def is_prepositional_nmod(nmod: Token) -> bool:
    return any(token.dep_ == "case" for token in nmod.lefts)


def expand_noun(noun: Token) -> list[Token]:
    def _expand_noun(_noun):
        _noun_phrase = [_noun]
        for token in _noun.children:
            if token.pos_ in {"NOUN", "PROPN", "ADJ"} and token.dep_ in {
                "flat:name",
                "compound",
                "nmod",
                "amod",
            }:
                if token.dep_ == "nmod" and is_prepositional_nmod(token):
                    continue
                for conjunct in token.conjuncts:
                    if conjunct.pos_ in {"NOUN", "PROPN", "ADJ"}:
                        _noun_phrase.extend(_expand_noun(conjunct))
                        for token_ in conjunct.lefts:
                            if token_.dep_ in {"cc", "punct"}:
                                _noun_phrase.append(token_)
                _noun_phrase.extend(_expand_noun(token))
        return _noun_phrase

    noun_phrase = _expand_noun(noun)
    noun_phrase.sort(key=attrgetter("i"))
    return noun_phrase


def extract_args(head_noun: Token) -> list[list[Token]]:
    arguments = [expand_noun(head_noun)]
    for conjunct in head_noun.conjuncts:
        if conjunct.pos_ in {"NOUN", "PROPN"}:
            arguments.append(expand_noun(conjunct))
    return arguments


def dist_subjs_mods_to_verb_conjs(verbs) -> None:
    for verb, details in verbs.items():
        head = verbs.get(verb.head)
        if head is not None and verb.dep_ == "conj":
            if not details.get("subjects") and head.get("subjects"):
                details["subjects"] = head["subjects"]
            if not details.get("modifiers") and head.get("modifiers"):
                details["modifiers"] = head["modifiers"]
    return None


def dist_objs_to_verb_conjs(verbs) -> None:
    for verb, details in verbs.items():
        if objects := details.get("objects"):
            for conjunct in verb.conjuncts:
                conj = verbs.get(conjunct)
                if conj is not None and conjunct.i < verb.i and not conj.get("objects"):
                    conj["objects"] = objects
    return None


def handle_xcomp_subjs(verbs) -> None:
    for verb, details in verbs.items():
        head = verbs.get(verb.head)
        if head is not None and verb.dep_ == "xcomp" and details.get("objects"):
            details["subjects"] = head.get("objects") or head["subjects"]
    return None


def extract_svo_triples(sentence: Span) -> list[SVOTriple]:
    svo_triples = []
    verbs = defaultdict(lambda: defaultdict(list))

    for token in sentence:
        head = token.head
        if token.pos_ == "VERB":
            verb = verbs[token]
            if token.dep_ in {"acl", "acl:relcl"} and head.pos_ in {"NOUN", "PROPN"}:
                verb["subjects"].extend(extract_args(head))
        elif head.pos_ == "VERB":
            head = verbs[head]
            if token.pos_ in {"NOUN", "PROPN"}:
                if token.dep_ in {"nsubj", "nsubj:pass"}:
                    head["subjects"].extend(extract_args(token))
                elif token.dep_ == "obj":
                    head["objects"].extend(extract_args(token))
            elif token.dep_ in {"advmod", "aux"}:
                head["modifiers"].append(token)

    dist_objs_to_verb_conjs(verbs)
    handle_xcomp_subjs(verbs)
    dist_subjs_mods_to_verb_conjs(verbs)

    for verb, details in verbs.items():
        subjects = details.get("subjects")
        objects = details.get("objects")
        if subjects and objects:
            vp = [verb]
            if verb_modifiers := details.get("modifiers"):
                vp.extend(verb_modifiers)
                vp.sort(key=attrgetter("i"))
            for s, o in product(subjects, objects):
                svo_triples.append(SVOTriple(s=s, v=vp, o=o))

    return svo_triples
