.. cmdtool documentation master file, created by
   sphinx-quickstart on Sun Dec 30 15:19:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======================================================
The **qttool** Documentation
======================================================
Bei diesem Projekt handelt es sich um ein Python Template für ein Qt Tool. Es
besteht aus dem Package :py:mod:`qttool` welches wiederum aus folgenden Modulen besteht.

* Einem Hauptmodul :py:mod:`qttool.qttool` welches Kommandozeilen Argumente mit Hilfe von :py:mod:`argparse` verarbeitet. Siehe hierzu:
    ::

        qttool/qttool.py
* | Dem Modul :py:mod:`qttool.calc`, sowie dem Modul :py:mod:`qttool.employee`.
* | Diese Module dienen keinerlei Zweck, außer getestet zu werden. Siehe hierzu:

    :: 

        qttool/calc.py
        qttool/employee.py

Zusätzlich enthält das Projekt folgende Inhalte:

* Ein paar Unit Tests Beispiele basierend auf :py:mod:`unittest` sowie :py:mod:`unittest.mock`. Siehe hierzu:
    :: 

        unit_tests/test_calc.py
        unit_tests/test_employee.py
* Eine Sphinx Dokumentation dieses Projektes. Siehe hierzu:
    :: 

        docs/*

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
   qttool.rst

Indizes und Tabellen
--------------------
* :ref:`genindex`
* :ref:`qttool_doc`
* :ref:`search`

