from orangewidget.utils.widgetpreview import WidgetPreview

from Orange.data import Table
from Orange.util import try_
from Orange.widgets import gui, settings
from Orange.widgets.widget import Input, Output, Msg, OWWidget

from orangecontrib.timeseries import Timeseries
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owinterpolate." + key)


class OWInterpolate(OWWidget):
    name = __("name")
    description = __("desc")
    icon = 'icons/Interpolate.svg'
    priority = 15

    class Inputs:
        time_series = Input('Time series', Table, label=i18n.t("timeseries.common.time_series"))

    class Outputs:
        interpolated = Output("Interpolated time series", Timeseries, label=i18n.t("timeseries.common.interpolated_time_series"))

    want_main_area = False
    resizing_enabled = False

    Linear, Cubic, Nearest, Mean = range(4)
    Options = [__("linear_interpolation"), __("cubic_interpolation"),
               __("nearest_point_interpolation"), __("mean_interpolation")]
    OptArgs = ["linear", "cubic", "nearest", "mean"]

    interpolation = settings.Setting(Linear)
    multivariate = settings.Setting(False)
    autoapply = settings.Setting(True)

    settings_version = 2

    class Warning(OWWidget.Warning):
        # This message's formulation is weird but: the widget is narrow and
        # it's better to start the sentence with "Categorical" (which is seen)
        # than with "Missing values for ..."
        discrete_mode = Msg(__("msg.categorical"))

    def __init__(self):
        self.data = None
        box = gui.vBox(self.controlArea, True)
        gui.comboBox(box, self, 'interpolation', items=self.Options,
                     label=__('label.interpolation_missing_values'),
                     callback=self.commit.deferred)
        gui.checkBox(box, self, 'multivariate',
                     label=__('label.multi-variate_interpolation'),
                     callback=self.commit.deferred)
        gui.auto_commit(box, self, 'autoapply', __('btn_apply'))

    @Inputs.time_series
    def set_data(self, data):
        self.data = Timeseries.from_data_table(data) if data else None
        self.commit.now()

    @gui.deferred
    def commit(self):
        self.Warning.clear()

        if not self.data:
            self.Outputs.interpolated.send(None)
            return

        if self.interpolation not in (self.Mean, self.Nearest) \
                and any(var.is_discrete for var in self.data.domain.variables):
            self.Warning.discrete_mode()

        data = self.data.copy()
        data.set_interpolation(self.OptArgs[self.interpolation], self.multivariate)
        self.Outputs.interpolated.send(try_(lambda: data.interp()) or None)

    @classmethod
    def migrate_settings(cls, settings, version):
        if not version or version < 2:
            settings["interpolation"] = \
                cls.OptArgs.index(settings["interpolation"])


if __name__ == "__main__":
    data = Timeseries.from_file('airpassengers')
    WidgetPreview(OWInterpolate).run(data)
