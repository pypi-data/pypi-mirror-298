from AnyQt.QtWidgets import QFormLayout

from Orange.widgets import gui
from Orange.widgets import settings
from orangecontrib.text.corpus import Corpus
from orangecontrib.text.vectorization import SimhashVectorizer
from orangecontrib.text.widgets.utils import owbasevectorizer
from orangecontrib.text.i18n_config import *


def __(key):
    return i18n.t('text.owsimhash.' + key)


class OWSimhash(owbasevectorizer.OWBaseVectorizer):
    name = __("name")
    description = __("desc")
    icon = 'icons/Simhash.svg'
    priority = 310
    keywords = "similarity hashing, simhash"

    Method = SimhashVectorizer

    f = settings.Setting(64)
    shingle_len = settings.Setting(10)

    def create_configuration_layout(self):
        layout = QFormLayout()

        spin = gui.spin(self, self, "f", minv=8, maxv=SimhashVectorizer.max_f, step=8)
        spin.editingFinished.connect(self.f_spin_changed)
        layout.addRow(__("row_simhash_size"), spin)

        spin = gui.spin(self, self, 'shingle_len', minv=1, maxv=100)
        spin.editingFinished.connect(self.on_change)
        layout.addRow(__("row_shingle_length"), spin)
        return layout

    def init_method(self):
        return self.Method(shingle_len=self.shingle_len, f=self.f)

    def f_spin_changed(self):
        # simhash needs f value to be multiple of 8, correct if it is not
        self.f = 8 * round(self.f / 8)
        self.on_change()


if __name__ == '__main__':
    from orangewidget.utils.widgetpreview import WidgetPreview

    WidgetPreview(OWSimhash).run(Corpus.from_file("book-excerpts"))
