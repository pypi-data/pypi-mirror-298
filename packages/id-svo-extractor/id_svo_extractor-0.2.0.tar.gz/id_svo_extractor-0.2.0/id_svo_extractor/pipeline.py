from spacy import Language, prefer_gpu
from spacy.tokens import Span
from spacy_stanza import load_pipeline

from id_svo_extractor.svo_extractor import extract_svo_triples


LANG = "id"


def create_pipeline(
    package: str = "default",
    processors: str | dict = "tokenize,mwt,pos,lemma,depparse",
    use_gpu: bool = True,
    download_method="reuse_resources",
    **kwargs,
) -> Language:
    if "depparse" not in processors:
        raise ValueError(
            "The 'depparse' processor is required and was not found in the provided 'processors' argument."
        )

    if use_gpu:
        prefer_gpu()

    nlp = load_pipeline(
        name=LANG,
        lang=LANG,
        package=package,
        processors=processors,
        use_gpu=use_gpu,
        download_method=download_method,
        **kwargs,
    )

    Span.set_extension("svo_triples", getter=extract_svo_triples, force=True)

    return nlp
