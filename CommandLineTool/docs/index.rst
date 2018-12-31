.. Command Line Tool Template documentation master file, created by
   sphinx-quickstart on Sun Dec 30 15:19:55 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CommandLineTool
======================================================
Bei diesem Projekt handelt es sich um ein Template für ein Kommandozeilen Tool. Es beeinhaltet:

* Ein Hauptskript welches Kommandozeilen Argumente mit hilfe von ArgParse :py:class:`argparse` verarbeitet. Siehe hierzu:
    .. code-block:: c

        cmdtool/cmdtool.py
* Ein wenig Business Logic die keinerlei zweck dient außer getestet zu werden. Siehe hierzu:
    .. code-block:: c

        cmdtool/calc.py
        cmdtool/employee.py
* Ein paar Unit Tests die als Beispiel dienen. Siehe hierzu:
    .. code-block:: c

        unit_tests/test_calc.py
        unit_tests/test_employee.py
* Einer Sphinx Dokumentation die als Referenz dient. Siehe hierzu:
    .. code-block:: c

        docs/*

Sphinx
------
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
