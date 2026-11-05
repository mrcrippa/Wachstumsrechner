Mithilfe dieses Wachstumsrechners kann man das Wachstum eines Kindes anhand der WHO-Standards für Länge und
Gewicht [1] berechnen und vorhersagen. Die Daten umfassen die ersten 60 Lebensmonate.

Konkret können Sie mit diesem Wachstumsrechner:
 - Perzentile und Messwerte berechnen.
 - Ermitteln, ob oder wann ein Zielmesswert erreicht wird.
 - Diagramme mit Wachstumsprognosen erstellen.

Die ursprünglich als Excel-Dateien bereitgestellten Tabellen auf der WHO-Website wurden aufgearbeitet und
in das CSV-Format konvertiert. Anschließend wurden die CSV-Dateien neu formatiert (weitere Informationen über
das Format finden Sie in der Klasse „WHODatenverarbeiter“). Die Endergebnisse befinden sich im Ordner „who_daten“.

Wenn Sie die Datei „wachstumsrechner.py“ ausführen, erhalten Sie eine einfache Konsolenoberfläche. Wenn Sie Tests mit der
Klasse "WHODatenverarbeiter" durchführen möchten, können Sie die Datei "who_datenverarbeiter.py" ausführen.

Die Datei „lms_methode.txt“ erläutert kurz, was die LMS-Methode ist und wie sie angewendet wird.
Diese Methode bezieht sich auf die Berechnung von Perzentilen und Messwerten.

Der Projektordner sollte die folgenden Dateien und Verzeichnisse enthalten:
    
    who_daten
        tab_lhfa_boys_p_0_5.csv
        tab_lhfa_girls_p_0_5.csv
        tab_wfa_boys_p_0_5.csv
        tab_wfa_girls_p_0_5.csv
    who_test_daten
        tab_lhfa_boys_p_0_5_falsch.csv
        tab_lhfa_girls_p_0_5_falsch.csv
        tab_wfa_girls_p_0_5_falsch.csv
    lms_methode.txt
    wachstumsrechner.py
    who_datenverarbeiter.py

[1] WHO-Standards für Länge und Gewicht (https://www.who.int/tools/child-growth-standards/standards).
