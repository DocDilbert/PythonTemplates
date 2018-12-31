.. Command Line Tool Template documentation master file, created by
   sphinx-quickstart on Sun Dec 30 15:19:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CommandLineTool
======================================================
Bei diesem Projekt handelt es sich um ein Template für ein Kommandozeilen Tool. Es beeinhaltet:

* Ein Hauptskript welches Kommandozeilen Argumente mit hilfe von :py:mod:`argparse` verarbeitet. Siehe hierzu:
    .. code-block:: c

        cmdtool/cmdtool.py
* Ein wenig Business Logic, die keinerlei zweck dient, außer getestet zu werden. Siehe hierzu:
    .. code-block:: c

        cmdtool/calc.py
        cmdtool/employee.py
* Ein paar Unit Tests Beispiele basierend auf :py:mod:`unittest` sowie :py:mod:`unittest.mock`. Siehe hierzu:
    .. code-block:: c

        unit_tests/test_calc.py
        unit_tests/test_employee.py
* Eine Sphinx Dokumentation dieses Projektes. Siehe hierzu:
    .. code-block:: python

        docs/*

Nützliche Links
---------------
* `Google Python Style Guide' <http://google.github.io/styleguide/pyguide.html>`_
* `Argparse Tutorial <https://docs.python.org/3/howto/argparse.html>`_
* `Documenting Your Project Using Sphinx <https://pythonhosted.org/an_example_pypi_project/sphinx.html>`_
* `Support for NumPy and Google style docstrings <https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_

Sphinx-Referenz
---------------
Um beim schreiben einer Sphinx Dokumentation zu helfen sind zwei rst Dateien
angehängt die die wichtigsten reStructuredText und Sphinx Kommandos enthalten:

* :ref:`quick-rst`
* :ref:`quick-sphinx`

Inhaltsverzeichniss
-------------------
.. toctree::
   :maxdepth: 2

   quick-rst.rst
   quick-sphinx.rst
   cmdtool.rst

Indizes und Tabellen
--------------------
* :ref:`genindex`
* :ref:`cmdtool_doc`
* :ref:`search`
