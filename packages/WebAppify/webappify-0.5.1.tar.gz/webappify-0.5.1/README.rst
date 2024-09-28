WebAppify
=========

|pypi| |license| |build|

WebAppify is a simple module to easily create your own desktop apps of websites. WebAppify uses PyQt5 and QtWebEngine
for displaying the web page, and works on Python 3.8 and up.

To create your own desktop web app, import and set up the WebApp class.

.. code:: python

   from webappify import WebApp

   app = WebApp('OpenStreetMap', 'https://www.openstreetmap.org', 'osm.png')
   app.run()

This will create a window with the website, using the icon provided.

.. note::

   If your site needs Flash Player, you'll need the appropriate Flash Player plugin installed system-wide. For QtWebKit
   you will need the NPAPI plugin, and for QtWebEngine you will need the PPAPI plugin.

Additional Options
------------------

``can_minimize_to_tray``
''''''''''''''''''''''''

.. important::

   This option was changed in version 0.4.0 from ``canMinimizeToTray`` to ``can_minimize_to_tray``. The old option
   is still available, but is deprecated. It will be removed in 0.5.0.

To install a system tray icon, and minimize your application to the system tray, simply pass
``can_minimize_to_tray=True`` to the class and a tray icon will be installed with the necessary menu options.

.. code:: python

   app = WebApp('OpenStreetMap', 'https://www.openstreetmap.org', 'osm.png', can_minimize_to_tray=True)
   
Clicking on the tray icon will show the window, while right-clicking will show the menu.

.. |pypi| image:: https://img.shields.io/pypi/v/WebAppify
   :target: https://pypi.org/project/webappify/
.. |license| image:: https://img.shields.io/pypi/l/WebAppify
   :target: https://git.snyman.info/raoul/webappify/src/branch/master/LICENSE
.. |build| image:: https://ci.snyman.info/api/badges/raoul/webappify/status.svg
   :target: https://ci.snyman.info/raoul/webappify
