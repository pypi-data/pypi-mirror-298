from spacy.tokens import Doc, Token


def merge_tokens_into_text(tokens: list[Token], lower: bool = False) -> str:
    text = "".join(token.text_with_ws for token in tokens).rstrip()
    return text.lower() if lower else text


def collect_svo_triples(doc: Doc, lower: bool = False) -> list[tuple[str, str, str]]:
    svo_triples = []
    for sentence in doc.sents:
        for s, v, o in sentence._.svo_triples:
            s = merge_tokens_into_text(s, lower)
            v = merge_tokens_into_text(v, lower)
            o = merge_tokens_into_text(o, lower)
            svo_triples.append((s, v, o))
    return svo_triples
