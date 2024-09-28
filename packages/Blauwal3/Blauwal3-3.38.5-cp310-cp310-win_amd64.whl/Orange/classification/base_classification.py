from Orange.base import Learner, Model, SklLearner, SklModel
from Orange.i18n_config import *
def __(key):
    return i18n.t("orange." + key)

__all__ = ["LearnerClassification", "ModelClassification",
           "SklModelClassification", "SklLearnerClassification"]


class LearnerClassification(Learner):
    learner_adequacy_err_msg = __("tip.need_discrete_class_variable")

    def incompatibility_reason(self, domain):
        reason = None
        if len(domain.class_vars) > 1 and not self.supports_multiclass:
            reason = "Too many target variables."
        elif not domain.has_discrete_class:
            reason = "Categorical class variable expected."
        return reason


class ModelClassification(Model):
    def predict_proba(self, data):
        return self(data, ret=Model.Probs)


class SklModelClassification(SklModel, ModelClassification):
    pass


class SklLearnerClassification(SklLearner, LearnerClassification):
    __returns__ = SklModelClassification
