"""Learners"""
from Orange.i18n_config import *


def __(key):
    return i18n.t("widget.model.model." + key)


NAME = 'Model'
ID = "orange.widgets.model"
LABEL = __("package_label")

DESCRIPTION = __("package_desc")

BACKGROUND = '#FAC1D9'

ICON = 'icons/Category-Model.svg'

PRIORITY = 4
