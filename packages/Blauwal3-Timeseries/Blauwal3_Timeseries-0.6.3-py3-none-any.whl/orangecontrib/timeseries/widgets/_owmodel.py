from AnyQt.QtCore import QTimer, Qt
from AnyQt.QtWidgets import QFormLayout

from Orange.data import Table
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Input, Output
from orangecontrib.timeseries import Timeseries
from orangecontrib.timeseries.models import _BaseModel
from orangecontrib.timeseries.i18n_config import *


def __(key):
    return i18n.t("timeseries.owmodel." + key)


class OWBaseModel(widget.OWWidget):
    """Abstract widget representing a time series model"""
    LEARNER = None

    class Inputs:
        time_series = Input('Time series', Table, default=True, label=i18n.t("timeseries.common.time_series"))

    class Outputs:
        learner = Output('Time series model', _BaseModel, label=i18n.t("timeseries.common.time_series_model"))
        forecast = Output('Forecast', Timeseries, label=i18n.t("timeseries.common.forecast"))
        fitted_values = Output('Fitted values', Timeseries, label=i18n.t("timeseries.common.fit_value"))
        residuals = Output('Residuals', Timeseries, label=i18n.t("timeseries.common.residual"))

    want_main_area = False
    resizing_enabled = False

    autocommit = settings.Setting(True)
    learner_name = settings.Setting('')
    forecast_steps = settings.Setting(3)
    forecast_confint = settings.Setting(95)

    class Error(widget.OWWidget.Error):
        not_continuous = widget.Msg(__("msg.target_var_type"))
        no_target = widget.Msg(__("msg.missing_target_var"))
        model_error = widget.Msg(__('msg.err'))

    def __init__(self):
        super().__init__()
        self.name_lineedit = None
        self.data = None
        self.learner = None
        self.model = None
        self.preprocessors = None
        self.outdated_settings = False
        self.setup_layout()
        QTimer.singleShot(0, self.apply.now)

    def create_learner(self):
        """Creates a learner (cunfit model) with current configuration """
        raise NotImplementedError

    @Inputs.time_series
    def set_data(self, data):
        self.data = data = None if data is None else \
                           Timeseries.from_data_table(data)
        self.update_model()

    @gui.deferred
    def apply(self):
        self.update_learner()
        self.update_model()

    def update_learner(self):
        learner = self.learner = self.create_learner()
        self.name_lineedit.setPlaceholderText(str(self.learner))
        learner.name = self.learner_name or str(learner)
        self.Outputs.learner.send(learner)

    def fit_model(self, model, data):
        return model.fit(data.interp())

    def forecast(self, model):
        return model.predict(self.forecast_steps,
                             alpha=1 - self.forecast_confint / 100,
                             as_table=True)

    def update_model(self):
        forecast = None
        fittedvalues = None
        residuals = None
        self.Error.model_error.clear()
        if self.is_data_valid():
            model = self.learner = self.create_learner()
            model.name = self.learner_name or str(model)
            try:
                is_fit = False
                self.fit_model(model, self.data)
                is_fit = True
                forecast = self.forecast(model)
                forecast.name = f"Forecast ({model.name})"
                fittedvalues = model.fittedvalues(as_table=True)
                fittedvalues.name = f"Fitted values ({model.name})"
                residuals = model.residuals(as_table=True)
                residuals.name = f"Residuals ({model.name})"
            except Exception as ex:
                action = 'forecasting' if is_fit else 'fitting model'
                self.Error.model_error(action, ex.__class__.__name__,
                                       ex.args[0] if ex.args else '')
        self.Outputs.forecast.send(forecast)
        self.Outputs.fitted_values.send(fittedvalues)
        self.Outputs.residuals.send(residuals)

    def is_data_valid(self):
        data = self.data
        if data is None:
            return False
        self.Error.clear()
        if not data.domain.class_var:
            self.Error.no_target()
            return False
        if not data.domain.class_var.is_continuous:
            self.Error.not_continuous()
            return False
        return True

    def send_report(self):
        name = self.learner_name or str(self.learner if self.learner else '')
        if name:
            self.report_items(((__("report.name"), name),))
        if str(self.learner) != name:
            self.report_items(((__("report.model_type"), str(self.learner)),))
        self.report_items(((__("report.forecast_step"), self.forecast_steps),
                           (__("report.confidence_interval"), self.forecast_confint),))
        if self.data is not None:
            self.report_data(__("report.time_series"), self.data)

    # GUI
    def setup_layout(self):
        self.add_learner_name_widget()
        self.add_main_layout()
        self.add_bottom_buttons()

    def add_main_layout(self):
        """Creates layout with the learner configuration widgets.

        Override this method for laying out any learner-specific parameter controls.
        See setup_layout() method for execution order.
        """
        raise NotImplementedError

    def add_learner_name_widget(self):
        self.name_lineedit = gui.lineEdit(
            self.controlArea, self, 'learner_name', box=__('box.name'),
            tooltip=__('box.name_tip'))

    def add_bottom_buttons(self):
        layout = QFormLayout()
        gui.widgetBox(self.controlArea, __("box.forecast"), orientation=layout)
        layout.addRow(__('label.forecast_steps_ahead'),
                      gui.spin(None, self, 'forecast_steps', 1, 100,
                               alignment=Qt.AlignRight,
                               controlWidth=50, callback=self.apply.deferred))
        layout.addRow(__('label.confidence_intervals'),
                      gui.hSlider(None, self, 'forecast_confint', None, 1, 99,
                      callback=self.apply.deferred))
        gui.auto_commit(self.controlArea, self, 'autocommit', i18n.t("timeseries.common_btn.apply"),
                        commit=self.apply)
