.. cmdtool documentation master file, created by
   sphinx-quickstart on Sun Dec 30 15:19:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. include globals.rst

======================================================
Die **autocomment** Dokumentation
======================================================
Bei diesem Projekt handelt es sich um ein Python Template für ein Qt Tool. Es
besteht aus dem Package :py:mod:`autocomment` welches wiederum aus folgenden Modulen besteht.

* Einem Hauptmodul :py:mod:`autocomment.main` welches Kommandozeilen Argumente mit Hilfe von :py:mod:`argparse` verarbeitet.
  Die Methode :py:meth:`~autocomment.main.main` dieses Moduls verwendet die Klasse :py:class:`~.MainWindow` um ein qt Fenster 
  darzustellen. Siehe hierzu::

    autocomment/main.py

* Dem Modul :py:mod:`autocomment.mainwindow`, welches die
  Klasse :py:class:`~autocomment.mainwindow.MainWindow` enthält. Diese Klasse baut das
  UI auf. Siehe hierzu::

    autocomment/mainwindow.py

Zusätzlich enthält das Projekt folgende Inhalte:

* Eine Sphinx Dokumentation dieses Projektes. Siehe hierzu:: 

    docs/*

HowTo: QtDesigner
-------------------
#. Das Qt-Programm `Designer` aufrufen. Das Programm ist bei Anaconda 3 dabei.
#. Die UI im Designer erstellen. 
    * Beim erstellen eines neuen UI, die Basisklasse auswählen (z.B. :py:class:`QMainWindow`)
    * Als ersten Schritt sollte man der Hauptklasse (z.B. :py:class:`QMainWindow`) in der Objektanzeige ein Layout zuweisen. Hierzu rechte Maustaste und danach Layout.
    * Das UI erstellen.
#. Die uic Datei unter dem Package :py:mod:`autocomment.ui` speichern.
#. Mit Hilfe des Tool pyuic5 die uic Datei in eine Python Datei umwandlen.
#. Die Python Datei in den bestehenden Code einbinden.

Das ganze ist schon im Modul :py:mod:`autocomment.mainwindow` beispielhaft vorbereitet worden. Siehe hierzu::

    autocomment/mainwindow.py
    autocomment/ui/mainWindow.ui
    autocomment/ui/ui_mainwindow.py

Um die Datei :file:`ui_mainWindow.py` zu aktualisieren gibt es das Make Target :code:`ui`.


Sphinx-Referenz
-------------------
Um beim schreiben einer Sphinx Dokumentation zu helfen sind zwei rst Dateien
angehängt die die wichtigsten reStructuredText und Sphinx Kommandos enthalten:

* :ref:`quick-rst`
* :ref:`quick-sphinx`

Nützliche Links
-------------------
Folgende Links sind für die Verwendung dieses Templates nützlich:

* **Python:**
    #. `Google Python Style Guide <http://google.github.io/styleguide/pyguide.html>`_
    #. `Argparse Tutorial <https://docs.python.org/3/howto/argparse.html>`_
    #. `The Hitchhiker’s Guide to Packaging <https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/index.html>`_ 
    #. `python-packaging Command-Line-Scripts <https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html>`_
* **Sphinx:**
    #. `reStructuredText Markup Specification <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html>`_
    #. `Quick reStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
    #. `Documenting Your Project Using Sphinx <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`_
    #. `Cross referencing Python objects <http://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cross-referencing-python-objects>`_
    #. `Support for NumPy and Google style docstrings <https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_

Inhaltsverzeichniss
-------------------
.. toctree::
   :maxdepth: 2

   quick-rst.rst
   quick-sphinx.rst
   autocomment.rst

Indizes und Tabellen
--------------------
* :ref:`genindex`
* :ref:`qttool_doc`
* :ref:`search`

