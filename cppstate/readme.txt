Dieses Skript erzeugt eine C++ State Machine basierend auf dem State Pattern
zum Einsatz in einem embedded System.

Vorraussetzungen
------------------
1) Python Version 3
    - Cog - Code - Generator für Python
2) PlantUml - Für die Generierung des Zustandsdiagrams
3) GraphViz - Vorraussetzungen von PlantUml zur Erzeugung von Graphen

Kurzanleitung
------------------
1) Die gewünschten Zustände in der Datei "config.json" eintragen. Der oberste Zustand ist immer der Initialzustand.
2) Die gewünschten Zustandstransitionen in der Datei "config.json" eintragen.
3) Den Befehl "make" ausführen. Die Statemachine wird nun unter dem Ordner ./autogen erzeugt
4) Der Befehl "make run" kompiliert die Statemachine mittels gcc und führt sie aus.
5) Der Befehl "make doc" generiert ein Zustandsdiagramm der State Machine
