import unicodedata as ud
import numpy as np
from elasticsearch_dsl import analysis
from elasticsearch_dsl.connections import connections
from spacy.lang.el.stop_words import STOP_WORDS

connections.create_connection()

spacy_sw = np.array(list(STOP_WORDS))


def remove_accent(spacy_sw):
    no_accent_spacy_sw = []
    d = {ord('\N{COMBINING ACUTE ACCENT}'): None}
    [no_accent_spacy_sw.append(ud.normalize('NFD', sw).replace('ς', 'σ').translate(d)) for sw in spacy_sw]

    return no_accent_spacy_sw


greek_analyzer = analysis.analyzer("greek_analyzer",
                                   type="custom",
                                   tokenizer="standard",
                                   filter=[
                                       analysis.token_filter("greek_lowercase", type="lowercase", language="greek"),
                                       analysis.token_filter('greek_stop', type="stop", stopwords="_greek_"),
                                       analysis.token_filter('greek_stemmer', type="stemmer", language="greek"),
                                       analysis.token_filter('spacy_sw', type="stop", stopwords=remove_accent(spacy_sw))
                                   ],
                                   )
