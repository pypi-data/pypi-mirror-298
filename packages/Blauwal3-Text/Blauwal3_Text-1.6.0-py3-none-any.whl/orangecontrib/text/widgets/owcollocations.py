from collections import namedtuple
import numpy as np

from Orange.widgets.widget import OWWidget
from Orange.widgets.gui import BarRatioTableModel
from Orange.data import Domain, StringVariable, ContinuousVariable, Table
from AnyQt.QtCore import Qt, pyqtSignal as Signal
from AnyQt.QtWidgets import QTableView, QItemDelegate

from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk import BigramCollocationFinder, TrigramCollocationFinder

from orangecontrib.text import Corpus
from orangewidget import settings, gui
from orangewidget.utils.signals import Input, Output
from orangewidget.utils.widgetpreview import WidgetPreview
from orangecontrib.text.i18n_config import *

def __(key):
    return i18n.t('text.owcollocations.' + key)

NGRAM_TYPES = [BigramCollocationFinder, TrigramCollocationFinder]

ScoreMeta = namedtuple("score_meta", ["name", "scorer"])

bi_measures = BigramAssocMeasures()
tri_measures = TrigramAssocMeasures()

SCORING_METHODS = [
    ScoreMeta(__("method.pointwise_mutual_information"), [bi_measures.pmi, tri_measures.pmi]),
    ScoreMeta(__("method.chi_square"), [bi_measures.chi_sq, tri_measures.chi_sq]),
    ScoreMeta(__("method.dice"), [bi_measures.dice]),
    ScoreMeta(__("method.fisher"), [bi_measures.fisher]),
    ScoreMeta(__("method.jaccard"), [bi_measures.jaccard, tri_measures.jaccard]),
    ScoreMeta(__("method.likelihood_ratio"), [bi_measures.likelihood_ratio, tri_measures.likelihood_ratio]),
    ScoreMeta(__("method.mi_like"), [bi_measures.mi_like, tri_measures.mi_like]),
    ScoreMeta(__("method.phi_square"), [bi_measures.phi_sq]),
    ScoreMeta(__("method.poisson_stirling"), [bi_measures.poisson_stirling, tri_measures.poisson_stirling]),
    ScoreMeta(__("method.raw_frequency"), [bi_measures.raw_freq, tri_measures.raw_freq]),
    ScoreMeta(__("method.students_t"), [bi_measures.student_t, tri_measures.student_t])
]


VARNAME_COL, NVAL_COL = range(2)


class TableView(QTableView):
    manualSelection = Signal()

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent,
                         selectionBehavior=QTableView.SelectRows,
                         selectionMode=QTableView.ExtendedSelection,
                         sortingEnabled=True,
                         showGrid=True,
                         cornerButtonEnabled=False,
                         alternatingRowColors=False,
                         **kwargs)
        # setItemDelegate(ForColumn) doesn't take ownership of delegates
        self._bar_delegate = gui.ColoredBarItemDelegate(self)
        self._del0, self._del1 = QItemDelegate(), QItemDelegate()
        self.setItemDelegate(self._bar_delegate)
        self.setItemDelegateForColumn(VARNAME_COL, self._del0)
        self.setItemDelegateForColumn(NVAL_COL, self._del1)

        header = self.horizontalHeader()
        header.setSectionResizeMode(header.Fixed)
        header.setFixedHeight(24)
        header.setDefaultSectionSize(80)
        header.setTextElideMode(Qt.ElideMiddle)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.manualSelection.emit()


class OWCollocations(OWWidget):
    name = __("name")
    description = __("desc")
    keywords = "collocations, pmi"
    icon = "icons/Collocations.svg"

    class Inputs:
        corpus = Input("Corpus", Corpus)

    class Outputs:
        corpus = Output("Table", Table)

    want_main_area = True

    # settings
    type_index = settings.Setting(0)
    selected_method = settings.Setting(0)
    freq_filter = settings.Setting(1)
    auto_apply = settings.Setting(True)

    def __init__(self) -> None:
        OWWidget.__init__(self)
        self.corpus = None
        self.type = NGRAM_TYPES[self.type_index]
        self.method = None
        self.results = None

        setting_box = gui.vBox(self.controlArea, box=__("settings"))
        gui.radioButtons(setting_box, self, "type_index",
                         btnLabels=[__("bigrams"), __("trigrams")],
                         orientation=Qt.Horizontal,
                         callback=self._change_type)

        gui.spin(setting_box, self, "freq_filter", minv=1, maxv=1000, step=1,
                 label=__("frequency"), callback=self.commit)

        method_box = gui.vBox(self.controlArea, box=__("scoring_method"))
        self.method_rb = gui.radioButtons(method_box, self, "selected_method",
                                          btnLabels=[m.name for m in
                                                     SCORING_METHODS],
                                          callback=self.commit)

        gui.rubber(self.controlArea)

        gui.button(self.buttonsArea, self, __("restore"),
                   callback=self.restore_order,
                   tooltip=__("tips"),
                   autoDefault=False)

        # GUI
        self.collModel = model = BarRatioTableModel(parent=self)  # type:
        # TableModel
        model.setHorizontalHeaderLabels([__("collocation"), __("score")])
        self.collView = view = TableView(self)  # type: TableView
        self.mainArea.layout().addWidget(view)
        view.setModel(model)
        view.resizeColumnsToContents()
        view.setItemDelegateForColumn(1, gui.ColoredBarItemDelegate())
        view.setSelectionMode(QTableView.NoSelection)

    @Inputs.corpus
    def set_corpus(self, corpus):
        self.collModel.clear()
        self.collModel.resetSorting(True)
        self.corpus = corpus
        self.commit()

    def _change_type(self):
        self.type = NGRAM_TYPES[self.type_index]
        if self.type_index == 1:
            self.method_rb.buttons[2].setDisabled(True)
            self.method_rb.buttons[3].setDisabled(True)
            self.method_rb.buttons[7].setDisabled(True)
            if self.selected_method in [2, 3, 7]:
                self.method_rb.buttons[0].click()
        else:
            self.method_rb.buttons[2].setDisabled(False)
            self.method_rb.buttons[3].setDisabled(False)
            self.method_rb.buttons[7].setDisabled(False)
        self.commit()

    def compute_scores(self):
        self.collModel.clear()
        self.collModel.resetSorting(True)
        finder = self.type.from_documents(self.corpus.tokens)
        finder.apply_freq_filter(self.freq_filter)

        res = finder.score_ngrams(self.method.scorer[self.type_index])
        collocations = np.array([" ".join(col) for col, score in res],
                                dtype=object)[:, None]
        scores = np.array([score for col, score in res], dtype=float)[:, None]

        self.results = (collocations, scores)
        if len(scores):
            self.collModel.setExtremesFrom(1, scores)

    def commit(self):
        if self.corpus is None:
            return

        self.type = NGRAM_TYPES[self.type_index]
        self.method = SCORING_METHODS[self.selected_method]

        self.compute_scores()

        if not self.results:
            self.collModel.clear()
            self.Outputs.corpus.send(None)
            return

        output = self.create_scores_table()
        self.collModel[:] = np.hstack(self.results)[:20]
        self.collView.resizeColumnsToContents()

        self.Outputs.corpus.send(output)

    def create_scores_table(self):
        domain = Domain([ContinuousVariable("Scores")],
                        metas=[StringVariable("Collocations")])

        collocations, scores = self.results

        new_table = Table.from_numpy(domain, scores, metas=collocations)
        new_table.name = "Collocation Scores"
        return new_table

    def restore_order(self):
        """Restore the original data order of the current view."""
        model = self.collModel
        self.collView.horizontalHeader().setSortIndicator(-1, Qt.AscendingOrder)
        if model is not None:
            model.resetSorting(yes_reset=True)

    def send_report(self):
        view = self.collView
        if self.results:
            self.report_items("Collocations", (
                ("N-grams", ["Bigrams", "Trigrams"][self.type_index]),
                ("Method", self.method.name),
                ("Frequency", self.freq_filter)
            ))
        self.report_table(view)


if __name__ == "__main__":  # pragma: no cover
    previewer = WidgetPreview(OWCollocations)
    previewer.run(Corpus.from_file("deerwester.tab"), no_exit=True)
