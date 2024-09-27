from spacy.tokens import Doc, Token


def merge_tokens_into_text(tokens: list[Token]) -> str:
    text = "".join(token.text_with_ws for token in tokens)
    return text.rstrip()


def collect_svo_triples(doc: Doc) -> list[tuple[str, str, str]]:
    svo_triples = []
    for sentence in doc.sents:
        for s, v, o in sentence._.svo_triples:
            s = merge_tokens_into_text(s)
            v = merge_tokens_into_text(v)
            o = merge_tokens_into_text(o)
            svo_triples.append((s, v, o))
    return svo_triples
