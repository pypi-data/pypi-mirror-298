"""
WebAppify
=========

WebAppify is a simple module to easily create your own desktop apps of websites. WebAppify uses PySide6 and
QtWebEngine for displaying the web page, and works on Python 3.10 and up.

To create your own desktop web app, import and set up the WebApp class.

.. code:: python

   from webappify import WebApp

   app = WebApp('OpenStreetMap', 'https://www.openstreetmap.org', 'osm.png')
   app.run()

This will create a window with the website, using the icon provided.

.. note::

   If your site needs Flash Player, you'll need the appropriate Flash Player plugin installed system-wide.
"""
import logging
import sys
import platform

from PySide6 import QtCore, QtGui, QtWidgets, QtWebEngineCore, QtWebEngineWidgets

SETTINGS = [
    QtWebEngineCore.QWebEngineSettings.PluginsEnabled,
    QtWebEngineCore.QWebEngineSettings.JavascriptCanAccessClipboard,
    QtWebEngineCore.QWebEngineSettings.LocalContentCanAccessRemoteUrls
]
LOG_LEVELS = {
    QtWebEngineCore.QWebEnginePage.InfoMessageLevel: logging.INFO,
    QtWebEngineCore.QWebEnginePage.WarningMessageLevel: logging.WARNING,
    QtWebEngineCore.QWebEnginePage.ErrorMessageLevel: logging.ERROR
}

log = logging.getLogger(__name__)


class WebPage(QtWebEngineCore.QWebEnginePage):
    """
    A custom QWebEnginePage which logs JS console messages to the Python logging system
    """
    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        """
        Custom logger to log console messages to the Python logging system
        """
        log.log(LOG_LEVELS[level], f'{source_id}:{line_number} {message}')


class WebWindow(QtWidgets.QWidget):
    """
    A window with a single web view and nothing else
    """
    def __init__(self, app, title, url, icon, can_minimize_to_tray=False, canMinimizeToTray=False):
        """
        Create the window
        """
        super(WebWindow, self).__init__(None)
        self._has_shown_warning = False
        self.app = app
        self.icon = QtGui.QIcon(icon)
        self.can_minimize_to_tray = can_minimize_to_tray or canMinimizeToTray
        self.setWindowTitle(title)
        self.setWindowIcon(self.icon)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.webview = QtWebEngineWidgets.QWebEngineView(self)
        self.webview.setPage(WebPage(self.webview))
        for setting in SETTINGS:
            self.webview.settings().setAttribute(setting, True)
        self.webview.setUrl(QtCore.QUrl(url))
        self.layout.addWidget(self.webview)
        self.webview.titleChanged.connect(self.on_title_changed)

    def _show_warning(self):
        """
        Show a balloon message to inform the user that the app is minimized
        """
        if not self._has_shown_warning:
            self.tray_icon.showMessage(self.windowTitle(), 'This program will continue running in the system tray. '
                                       'To close the program, choose <b>Quit</b> in the context menu of the system '
                                       'tray icon.', QtWidgets.QSystemTrayIcon.Information, 5000)
            self._has_shown_warning = True

    def _update_tray_menu(self):
        """
        Update the enabled/disabled status of the items in the tray icon menu
        """
        if not self.can_minimize_to_tray:
            return
        self.restore_action.setEnabled(not self.isVisible())
        self.minimize_action.setEnabled(self.isVisible() and not self.isMinimized())
        self.maximize_action.setEnabled(self.isVisible() and not self.isMaximized())

    def _restore_window(self):
        """
        Restore the window and activate it
        """
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def _maximize_window(self):
        """
        Restore the window and activate it
        """
        self.showMaximized()
        self.activateWindow()
        self.raise_()

    def _get_tray_menu(self):
        """
        Create and return the menu for the tray icon
        """
        # Create the actions for the menu
        self.restore_action = QtGui.QAction('&Restore', self)
        self.restore_action.triggered.connect(self._restore_window)
        self.minimize_action = QtGui.QAction('Mi&nimize', self)
        self.minimize_action.triggered.connect(self.close)
        self.maximize_action = QtGui.QAction('Ma&ximize', self)
        self.maximize_action.triggered.connect(self._maximize_window)
        self.quit_action = QtGui.QAction('&Quit', self)
        self.quit_action.triggered.connect(self.app.quit)
        # Create the menu and add the actions
        tray_icon_menu = QtWidgets.QMenu(self)
        tray_icon_menu.addAction(self.restore_action)
        tray_icon_menu.addAction(self.minimize_action)
        tray_icon_menu.addAction(self.maximize_action)
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(self.quit_action)
        return tray_icon_menu

    def setup_tray_icon(self):
        """
        Set up the tray icon
        """
        self.tray_icon = QtWidgets.QSystemTrayIcon(self.icon, self)
        self.tray_icon.setContextMenu(self._get_tray_menu())
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def closeEvent(self, event):
        """
        Override the close event to minimize to the tray
        """
        # If we don't want to minimize to the tray, just close the window as per usual
        if not self.can_minimize_to_tray:
            super(WebWindow, self).closeEvent(event)
            return
        # If we want to minimize to the tray, then just hide the window
        if platform.platform().lower() == 'darwin' and (not event.spontaneous() or not self.isVisible()):
            return
        else:
            self._show_warning()
            self.hide()
            event.ignore()
        # Update the menu to match
        self._update_tray_menu()

    def showEvent(self, event):
        """
        Override the show event to catch max/min/etc events and update the tray icon menu accordingly
        """
        super(WebWindow, self).showEvent(event)
        self._update_tray_menu()

    def hideEvent(self, event):
        """
        Override the hide event to catch max/min/etc events and update the tray icon menu accordingly
        """
        super(WebWindow, self).hideEvent(event)
        self._update_tray_menu()

    def changeEvent(self, event):
        """
        Catch the minimize event and close the form
        """
        if self.can_minimize_to_tray:
            if event.type() == QtCore.QEvent.WindowStateChange and self.windowState() & QtCore.Qt.WindowMinimized:
                self.close()
        super(WebWindow, self).changeEvent(event)

    def on_title_changed(self, title):
        """
        React to title changes
        """
        if title:
            self.setWindowTitle(title)
            if self.can_minimize_to_tray:
                self.tray_icon.setToolTip(title)

    def on_tray_icon_activated(self, reason):
        """
        React to the tray icon being activated
        """
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.close()
            else:
                self.showNormal()


class WebApp(QtWidgets.QApplication):
    """
    A generic application to open a web page in a desktop app
    """
    def __init__(self, title, url, icon, can_minimize_to_tray=False, canMinimizeToTray=False):
        """
        Create an application which loads a URL into a window
        """
        super(WebApp, self).__init__(sys.argv)
        self.window = None
        self.tray_icon = None
        self.title = title
        self.url = url
        self.icon = icon
        self.can_minimize_to_tray = QtWidgets.QSystemTrayIcon.isSystemTrayAvailable() and \
            (can_minimize_to_tray or canMinimizeToTray)
        if self.can_minimize_to_tray:
            self.setQuitOnLastWindowClosed(False)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setApplicationName(title)
        self.setApplicationDisplayName(title)

    def run(self):
        """
        Set up the window and the tray icon, and run the app
        """
        self.window = WebWindow(self, self.title, self.url, self.icon, self.can_minimize_to_tray)
        if self.can_minimize_to_tray:
            self.window.setup_tray_icon()
        self.window.showMaximized()
        return self.exec()
