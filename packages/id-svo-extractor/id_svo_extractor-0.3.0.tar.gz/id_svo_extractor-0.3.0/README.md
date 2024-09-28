![(id, svo, extractor)](https://i.imgur.com/FqUBo68.png)

# id-svo-extractor

**id-svo-extractor** is a heuristic tool designed to extract SVO (Subject-Verb-Object) triples from Indonesian text. It uses Stanza's state-of-the-art Indonesian language pipeline for NLP.

## Requirements

To use **id-svo-extractor**, you will need Python v3.10 or higher and the following Python package:
- [spacy-stanza](https://github.com/explosion/spacy-stanza) v1.0.4

You must also download Stanza's Indonesian models for `tokenize`, `mwt`, `pos`, `lemma`, and `depparse` processors before initializing the pipeline.

## Installation

Install the package directly from PyPI:

```sh
pip install id-svo-extractor
```

## Usage

Here's a basic example to get you started.

```python
from id_svo_extractor import create_pipeline
from id_svo_extractor.utils import collect_svo_triples
from stanza import download


# Download Stanza's Indonesian models for tokenize, mwt, pos, lemma, and depparse processors.
# This step is mandatory before initializing the NLP pipeline.
download("id", processors="tokenize,mwt,pos,lemma,depparse")

# Initialize the NLP pipeline.
nlp = create_pipeline()

doc = nlp("Niko dan Okin mendesain brosur promosi dan mencetak poster iklan.")

for sentence in doc.sents:
    # Extracted triples for each sentence are stored in `svo_triples` custom attribute.
    print(sentence._.svo_triples)
    # Output:
    # [ SVOTriple(s=[Niko], v=[mendesain], o=[brosur, promosi]),
    #   SVOTriple(s=[Okin], v=[mendesain], o=[brosur, promosi]),
    #   SVOTriple(s=[Niko], v=[mencetak], o=[poster, iklan]),
    #   SVOTriple(s=[Okin], v=[mencetak], o=[poster, iklan]) ]

print(collect_svo_triples(doc))
# Output:
# [ ('Niko', 'mendesain', 'brosur promosi'),
#   ('Okin', 'mendesain', 'brosur promosi'),
#   ('Niko', 'mencetak', 'poster iklan'),
#   ('Okin', 'mencetak', 'poster iklan') ]
```

## License

This project is licensed under the Apache License 2.0.