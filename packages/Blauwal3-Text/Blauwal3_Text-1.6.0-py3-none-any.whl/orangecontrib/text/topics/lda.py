from numpy import float64
from gensim import models

from .topics import GensimWrapper
from orangecontrib.text.i18n_config import *


def __(key):
    return i18n.t('text.common.' + key)

class LdaWrapper(GensimWrapper):
    name = __("lda_wrapper")
    Model = models.LdaModel

    def __init__(self, **kwargs):
        # with 200 iterations on pass (default) is usually not enough for all
        # documents to converge - with 5 it converged in all my cases
        super().__init__(random_state=0, **kwargs, dtype=float64, iterations=200, passes=5)
