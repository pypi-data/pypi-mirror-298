from AnyQt.QtCore import Qt

from orangewidget.utils.widgetpreview import WidgetPreview
from Orange.widgets import gui, settings
from orangecontrib.timeseries import Timeseries, VAR
from orangecontrib.timeseries.widgets._owmodel import OWBaseModel
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owvarmodel." + key)


class OWVARModel(OWBaseModel):
    name = __('name')
    description = __('desc')
    icon = 'icons/VAR.svg'
    priority = 220

    maxlags = settings.Setting(1)
    ic = settings.Setting(0)
    trend = settings.Setting(0)

    IC_LABELS = dict(((__('btn.none'), None),
                      (__("btn.aic"), 'aic'),
                      (__('btn.bic'), 'bic'),
                      (__('btn.hannan–quinn'), 'hqic'),
                      (__("btn.fpe"), 'fpe'),
                      (__('btn.average_of_the_above'), 'magic')))
    TREND_LABELS = dict(((__('btn.none'), 'nc'),
                         (__('btn.constant'), 'c'),
                         (__('btn.constant_linear'), 'ct'),
                         (__('btn.constant_linear_quadratic'), 'ctt')))

    def add_main_layout(self):
        box = gui.vBox(self.controlArea, box=__('box.parameter'))
        gui.spin(
            box, self, 'maxlags', 1, 100,
            label=__('label.maxlags'), alignment=Qt.AlignRight,
            callback=self.apply.deferred)
        gui.separator(self.controlArea, 12)
        box = gui.vBox(self.controlArea, box=True)
        gui.radioButtons(
            box, self, 'ic',
            btnLabels=tuple(self.IC_LABELS),
            label=__('label.optimize_ar_order'),
            callback=self.apply.deferred)
        gui.separator(self.controlArea, 12)
        gui.radioButtons(
            box, self, 'trend',
            btnLabels=tuple(self.TREND_LABELS),
            label=__('label.add_trend_vector'),
            callback=self.apply.deferred)

    def create_learner(self):
        ic = self.IC_LABELS[tuple(self.IC_LABELS.keys())[self.ic]]
        trend = self.TREND_LABELS[tuple(self.TREND_LABELS.keys())[self.trend]]
        return VAR(self.maxlags, ic, trend)


if __name__ == "__main__":
    data = Timeseries.from_file('airpassengers')
    WidgetPreview(OWVARModel).run(set_data=data)
