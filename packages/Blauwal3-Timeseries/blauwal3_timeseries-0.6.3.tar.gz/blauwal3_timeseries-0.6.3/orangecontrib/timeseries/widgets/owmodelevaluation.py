from collections import OrderedDict

import numpy as np

from AnyQt.QtCore import QSize

from Orange.data import Table
from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.itemmodels import PyTableModel
from Orange.widgets.widget import Input

from orangecontrib.timeseries import Timeseries, model_evaluation
from orangecontrib.timeseries.models import _BaseModel
from orangewidget.utils.widgetpreview import WidgetPreview
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owmodelevaluation." + key)


class Output:
    TIMESERIES = 'Time series'


class OWModelEvaluation(widget.OWWidget):
    name = __('name')
    description = __('desc')
    icon = 'icons/ModelEvaluation.svg'
    priority = 300

    class Inputs:
        time_series = Input('Time Series', Table, label=i18n.t("timeseries.common.time_series"))
        time_series_model = Input('Time Series model', _BaseModel, multiple=True,
                                  label=i18n.t("timeseries.common.time_series_model"))

    n_folds = settings.Setting(20)
    forecast_steps = settings.Setting(3)
    autocommit = settings.Setting(False)

    class Error(widget.OWWidget.Error):
        unexpected_error = widget.Msg(__('msg.error'))

    class Warning(widget.OWWidget.Warning):
        model_failed = widget.Msg(__('msg.model_setting_err'))

    def __init__(self):
        self.data = None
        self._models = OrderedDict()
        box = gui.vBox(self.controlArea, __('box_evaluation_parameters'))
        gui.spin(box, self, 'n_folds', 1, 100,
                 label=__('label_number_folds'),
                 callback=self.commit.deferred)
        gui.spin(box, self, 'forecast_steps', 1, 100,
                 label=__('forecast_steps'),
                 callback=self.commit.deferred)
        gui.auto_commit(self.buttonsArea, self, 'autocommit', __('btn_apply'))
        gui.rubber(self.controlArea)

        self.model = model = PyTableModel(parent=self)
        view = gui.TableView(self)
        view.setModel(model)
        view.horizontalHeader().setStretchLastSection(False)
        view.verticalHeader().setVisible(True)
        self.mainArea.layout().addWidget(view)

    def sizeHint(self):
        return QSize(650, 175)

    @Inputs.time_series
    def set_data(self, data):
        self.data = None if data is None else Timeseries.from_data_table(data)

    @Inputs.time_series_model
    def set_model(self, model, id):
        if model is None:
            self._models.pop(id, None)
        else:
            self._models[id] = model.copy()

    def handleNewSignals(self):
        self.commit.now()

    @gui.deferred
    def commit(self):
        self.Error.unexpected_error.clear()
        self.Warning.model_failed.clear()
        self.model.clear()
        data = self.data
        if not data or not self._models:
            return
        try:
            with self.progressBar(len(self._models) * (self.n_folds + 1) + 1) as progress:
                res = model_evaluation(data, list(self._models.values()),
                                       self.n_folds, self.forecast_steps,
                                       callback=progress.advance)
        except ValueError as e:
            self.Error.unexpected_error(e.args[0])
            return
        res = np.array(res, dtype=object)
        self.Warning.model_failed(shown="err" in res)
        self.model.setHorizontalHeaderLabels(res[0, 1:].tolist())
        self.model.setVerticalHeaderLabels(res[1:, 0].tolist())
        self.model.wrap(res[1:, 1:].tolist())


if __name__ == "__main__":
    class BadModel(_BaseModel):
        def _predict(self):
            return 1 / 0

    from orangecontrib.timeseries import ARIMA, VAR
    data = Timeseries.from_file('airpassengers')
    learners = [ARIMA((1, 1, 1)), ARIMA((2, 1, 0)), VAR(1), VAR(5), BadModel()]
    WidgetPreview(OWModelEvaluation).run(
        set_data=data,
        set_model=[(model, i) for i, model in enumerate(learners)]
    )
