"""
This module contains the implementation of the OWWeightedLogisticRegression.

This widget is used to create a logistic regression model which 
can use instance weights in the training process.
"""

import Orange.widgets.model.owlogisticregression

from Orange.base import Learner
from Orange.classification.logistic_regression import LogisticRegressionLearner
from Orange.preprocess import Impute

from orangecontrib.fairness.widgets.utils import check_for_missing_values
from orangecontrib.fairness.i18n_config import *

def __(key):
    return i18n.t('fairness.owweightedlogisticregression.' + key)

class WeightedLogisticRegressionLearner(LogisticRegressionLearner):
    """
    A class used to create a LogisticRegressionLearner which can
    use instance weights in the training and prediction process
    """

    def _fit_model(self, data):
        """
        A override of the _fit_model function of the LogisticRegressionLearner
        class which allows the use of instance weights
        """
        if type(self).fit is Learner.fit:
            return self.fit_storage(data)
        else:
            X, Y, W = data.X, data.Y, data.W if data.has_weights() else None
            if "weights" in map(lambda a: a.name, data.domain.metas):
                return self.fit(X, Y, W=data[:, "weights"].metas[:, 0])
            return self.fit(X, Y, W)


class OWWeightedLogisticRegression(
    Orange.widgets.model.owlogisticregression.OWLogisticRegression
):
    """A class used to create a widget which uses the WeightedLogisticRegressionLearner"""

    name = __("name")
    description = __("desc")
       
    icon = "icons/weighted_log_reg.svg"
    priority = 50
    keywords = "weighted logistic regression"
    replaces = []

    LEARNER = WeightedLogisticRegressionLearner

    class Inputs(Orange.widgets.model.owlogisticregression.OWLogisticRegression.Inputs):
        """The inputs of the widget - the dataset"""

        pass

    @Inputs.data
    @check_for_missing_values
    def set_data(self, data=None):
        """
        Handling input data by first imputing missing values if any and then calling the super class
        """
        if data is not None:
            if data.has_missing():
                data = Impute()(data)
        super().set_data(data)
