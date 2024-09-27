"""
Orange Canvas Configuration

"""
import pkgutil

import random
import uuid
import warnings
import os
import sys

from typing import Dict, Any, Optional, Iterable, List

import packaging.version
import requests

from AnyQt.QtGui import (
    QPainter, QFont, QFontMetrics, QColor, QImage, QPixmap, QIcon,
    QGuiApplication
)
from AnyQt.QtCore import Qt, QPoint, QRect, QSettings

from orangecanvas import config as occonfig
from orangecanvas.config import entry_points, EntryPoint
from orangecanvas.utils.settings import config_slot
from orangewidget.workflow import config
from orangewidget.settings import set_widget_settings_dir_components

import Orange
from Orange.misc import environ

from Orange.i18n_config import *

# i18n.set('locale', 'zh')
def __(key):
    return i18n.t("orange." + key)


# generated from biolab/orange3-addons repository
OFFICIAL_ADDON_LIST = "https://bw.dashenglab.com/addons/data_bw"

WIDGETS_ENTRY = "orange.widgets"

spec = [
    ("startup/check-updates", bool, True, "Check for updates"),

    ("startup/launch-count", int, 0, ""),

    ("reporting/machine-id", str, str(uuid.uuid4()), ""),

    ("reporting/send-statistics", bool, False, ""),

    ("reporting/permission-requested", bool, False, ""),

    ("notifications/check-notifications", bool, True, "Check for notifications"),

    ("notifications/announcements", bool, True,
     "Show notifications about Biolab announcements"),

    ("notifications/blog", bool, True,
     "Show notifications about blog posts"),

    ("notifications/new-features", bool, True,
     "Show notifications about new features"),

    ("notifications/displayed", str, 'set()',
     "Serialized set of notification IDs which have already been displayed")
]

spec = [config_slot(*t) for t in spec]


def _pixmap_from_pkg_data(package, path, format):
    contents = pkgutil.get_data(package, path)
    return QPixmap.fromImage(QImage.fromData(contents, format))


class Config(config.Config):
    """
    Orange application configuration
    """
    OrganizationDomain = "biolab.si"
    ApplicationName = __("name.application_name")
    ApplicationVersion = Orange.__version__
    AppUserModelID = "Biolab.Orange"  # AppUserModelID for windows task bar

    def init(self):
        super().init()
        self.update_language_settings()  # 添加这行代码
        QGuiApplication.setApplicationDisplayName(self.ApplicationName)
        widget_settings_dir_cfg = environ.get_path("widget_settings_dir", "")
        if widget_settings_dir_cfg:
            # widget_settings_dir is configured via config file
            set_widget_settings_dir_components(
                widget_settings_dir_cfg, self.ApplicationVersion
            )

        canvas_settings_dir_cfg = environ.get_path("canvas_settings_dir", "")
        if canvas_settings_dir_cfg:
            # canvas_settings_dir is configured via config file
            QSettings.setPath(
                QSettings.IniFormat, QSettings.UserScope,
                canvas_settings_dir_cfg
            )

        for t in spec:
            occonfig.register_setting(*t)

    def update_language_settings(self):
        """
        Update the application language settings based on user preferences.
        """
        settings = QSettings()
        language = settings.value("application-style/languages", "en")
        i18n.set('locale', language)
        self.ApplicationName = __("name.application_name")

    @staticmethod
    def application_icon():
        """
        Return the main application icon.
        """
        return QIcon(
            _pixmap_from_pkg_data(__package__, "icons/orange.ico", "ico")
        )

    @staticmethod
    def splash_screen():
        splash_n = random.randint(1, 3)
        pm = _pixmap_from_pkg_data(
            # __name__, f"icons/orange-splash-screen-{splash_n:02}.png", "png"
            __name__, f"icons/orange-splash-screen.png", "png"
        )

        version = Config.ApplicationVersion
        if version:
            version_parsed = packaging.version.Version(version)
            version_comp = version_parsed.release
            version = ".".join(map(str, version_comp[:2]))
        size = 21 if len(version) < 5 else 16
        font = QFont("Helvetica")
        font.setPixelSize(size)
        font.setBold(True)
        font.setItalic(True)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
        metrics = QFontMetrics(font)
        br = metrics.boundingRect(version).adjusted(-5, 0, 5, 0)
        br.moveTopLeft(QPoint(410, 218))

        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setFont(font)
        p.setPen(QColor("#000000"))
        p.drawText(br, Qt.AlignLeft, version)
        p.end()
        return pm, QRect(88, 193, 200, 20)

    @staticmethod
    def widgets_entry_points():
        """
        Return an `EntryPoint` iterator for all 'orange.widget' entry
        points.
        """
        # Ensure the 'this' distribution's ep is the first. iter_entry_points
        # yields them in unspecified order.
        all_eps = sorted(
            entry_points(group=WIDGETS_ENTRY),
            key=lambda ep:
            0 if ep.dist.name.lower() == "bluewhale3" else 1
        )
        return iter(all_eps)

    @staticmethod
    def addon_entry_points():
        return Config.widgets_entry_points()

    @staticmethod
    def addon_defaults_list(session=None):
        # type: (Optional[requests.Session]) -> List[Dict[str, Any]]
        """
        Return a list of available add-ons.
        """
        if session is None:
            session = requests.Session()
        return session.get(OFFICIAL_ADDON_LIST).json()

    @staticmethod
    def core_packages():
        # type: () -> List[str]
        """
        Return a list of 'core packages'

        These packages constitute required the application framework. They
        cannot be removes via the 'Add-on/plugins' manager. They however can
        be updated. The package that defines the application's `main()` entry
        point must always be in this list.
        """
        return ["bluewhale3 >=3.38,<4.5a"]

    @staticmethod
    def examples_entry_points():
        # type: () -> Iterable[EntryPoint]
        """
        Return an iterator over the entry points yielding 'Example Workflows'
        """
        # `iter_entry_points` yields them in unspecified order, so we order
        # them by name. The default is at the beginning, unless another
        # entrypoint precedes it alphabetically (e.g. starting with '!').
        default_ep = EntryPoint(
            "bluewhale3", "Orange.canvas.workflows", "orange.widgets.tutorials",
        )

        all_ep = list(entry_points(group="orange.widgets.tutorials"))
        all_ep.append(default_ep)
        all_ep.sort(key=lambda x: x.name)
        return iter(all_ep)

    APPLICATION_URLS = {
        #: Submit a bug report action in the Help menu
        "Bug Report": "https://github.com/biolab/orange3/issues",
        #: A url quick tour/getting started url
        "Quick Start": "https://bw.dashenglab.com/5fbb9705a6e5e67080638ac6.html",
        #: The 'full' documentation, should be something like current /docs/
        #: but specific for 'Visual Programing' only
        "Documentation": "https://bw.dashenglab.com/5f96afc397e57e5494285683.html",
        #: YouTube tutorials
        "Screencasts":
            "https://www.youtube.com/watch"
            "?v=HXjnDIgGDuI&list=PLmNPvQr9Tf-ZSDLwOzxpvY-HrE0yv-8Fy&index=1",
        #: Used for 'Submit Feedback' action in the help menu
        "Feedback": "https://orange.biolab.si/survey/long.html",
    }


def init():
    # left for backwards compatibility
    raise RuntimeError("This is not the init you are looking for.")


def data_dir():
    """
    Return the Orange application data directory. If the directory path
    does not yet exists then create it.
    """
    path = os.path.join(environ.data_dir(), "canvas")
    try:
        os.makedirs(path, exist_ok=True)
    except OSError:
        pass
    return path


def cache_dir():
    """
    Return the Orange application cache directory. If the directory path
    does not yet exists then create it.
    """
    path = os.path.join(environ.cache_dir(), "canvas")
    try:
        os.makedirs(path, exist_ok=True)
    except OSError:
        pass
    return path


def log_dir():
    """
    Return the application log directory.
    """
    if sys.platform == "darwin":
        name = Config.ApplicationName
        logdir = os.path.join(os.path.expanduser("~/Library/Logs"), name)
    else:
        logdir = data_dir()

    logdir = environ.get_path("log_dir", logdir)

    try:
        os.makedirs(logdir, exist_ok=True)
    except OSError:
        pass
    return logdir


def widget_settings_dir():
    """
    Return the widget settings directory.

    .. deprecated:: 3.38
    """
    warnings.warn(
        __("tip.deprecate").format(__name__),
        DeprecationWarning, stacklevel=2
    )
    import orangewidget.settings
    return orangewidget.settings.widget_settings_dir()


def widgets_entry_points():
    return Config.widgets_entry_points()


def addon_entry_points():
    return Config.addon_entry_points()


def splash_screen():
    return Config.splash_screen()


def application_icon():
    return Config.application_icon()
