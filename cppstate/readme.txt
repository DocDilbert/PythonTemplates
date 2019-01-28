Dieses Skript erzeugt eine C++ State Machine basierend auf dem State Pattern
zum Einsatz in einem embedded System.

Kurzanleitung
------------------
1) Die gewünschten Zustände in der Datei "config.json" eintragen.
2) Die gewünschten Zustandstransitionen in der Datei "config.json" eintragen.
3) Den Befehl "make" ausführen. Die Statemachine wird nun unter dem Ordner ./autogen erzeugt
4) Der Befehl "make run" kompiliert die Statemachine mittels gcc und führt sie aus.
