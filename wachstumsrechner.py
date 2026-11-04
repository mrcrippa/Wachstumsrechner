from who_datenverarbeiter import WHODatenverarbeiter

# Mithilfe dieses Wachstumsrechners kann man das Wachstum eines Kindes anhand der WHO-Standards für Länge und
# Gewicht [1] berechnen und vorhersagen. Die Daten umfassen die ersten 60 Lebensmonate.
#
# Konkret können Sie mit diesem Wachstumsrechner:
#  - Perzentile und Messwerte berechnen.
#  - Ermitteln, ob oder wann ein Zielmesswert erreicht wird.
#  - Diagramme mit Wachstumsprognosen erstellen.
#
# Die ursprünglich als Excel-Dateien bereitgestellten Tabellen auf der WHO-Website wurden aufgearbeitet und
# in das CSV-Format konvertiert. Anschließend wurden die CSV-Dateien neu formatiert (weitere Informationen über
# das Format finden Sie in der Klasse „WHODatenverarbeiter“). Die Endergebnisse befinden sich im Ordner „who_daten“.
#
# Wenn Sie die Datei „wachstumsrechner.py“ ausführen, erhalten Sie eine einfache Konsolenoberfläche. Wenn Sie Tests mit der
# Klasse "WHODatenverarbeiter" durchführen möchten, können Sie die Datei "who_datenverarbeiter.py" ausführen.
#
# Die Datei „lms_methode.txt“ erläutert kurz, was die LMS-Methode ist und wie sie angewendet wird.
# Diese Methode bezieht sich auf die Berechnung von Perzentilen und Messwerten.
#
# Der Projektordner sollte die folgenden Dateien und Verzeichnisse enthalten:
#     who_daten
#         tab_lhfa_boys_p_0_5.csv
#         tab_lhfa_girls_p_0_5.csv
#         tab_wfa_boys_p_0_5.csv
#         tab_wfa_girls_p_0_5.csv
#     who_test_daten
#         tab_lhfa_boys_p_0_5_falsch.csv
#         tab_lhfa_girls_p_0_5_falsch.csv
#         tab_wfa_girls_p_0_5_falsch.csv
#     lms_methode.txt
#     wachstumsrechner.py
#     who_datenverarbeiter.py
#
# [1] WHO-Standards für Länge und Gewicht (https://www.who.int/tools/child-growth-standards/standards).

if __name__ == "__main__":

    # Die WHO-Daten werden in den Speicher geladen.
    geladene_WHO_Daten = {}

    m_G = WHODatenverarbeiter()
    m_G.who_daten_einlesen("./who_daten/tab_wfa_boys_p_0_5.csv", "m", "gewicht - jungen", "G")
    geladene_WHO_Daten["m_G"] = m_G

    m_L = WHODatenverarbeiter()
    m_L.who_daten_einlesen("./who_daten/tab_lhfa_boys_p_0_5.csv", "m", "länge - jungen", "L")
    geladene_WHO_Daten["m_L"] = m_L

    w_G = WHODatenverarbeiter()
    w_G.who_daten_einlesen("./who_daten/tab_wfa_girls_p_0_5.csv", "w", "gewicht - mädchen", "G")
    geladene_WHO_Daten["w_G"] = w_G

    w_L = WHODatenverarbeiter()
    w_L.who_daten_einlesen("./who_daten/tab_lhfa_girls_p_0_5.csv", "m", "länge - mädchen", "L")
    geladene_WHO_Daten["w_L"] = w_L

    # Der Benutzer wählt einen Datensatz als Arbeitsdatensatz aus. Dieser ist am Anfang leer.
    arbeitsdatensatz = WHODatenverarbeiter()

    while True:
        print("#" * 96)
        print(" " * 31, "Willkommen beim Wachstumsrechner")
        print("#" * 96)
        print("Was möchten Sie tun?")
        print("     einen [daten]sätz auswählen")
        print("     [zeigen], welcher datensatz geladen ist")
        print("     [perzentil] von messwert und alter berechnen")
        print("     [messwert]  von perzentil und alter berechnen")
        print("     ermitteln, ob oder wann ein Zielmesswert [erreicht] ist")
        print("     ein [diagramm] mit Wachstumsprognose erstellen")
        print("     programm [beenden]")
        print()

        auswahl = input("Auswahl[daten,perzentil,messwert,erreicht,diagramm,beenden]: ")
        auswahl = auswahl.strip()

        if auswahl == "daten":

            print(f"\nAktuell geladene Daten : {arbeitsdatensatz.get_info()}\n")

            print("""Verfügbare Datensätze:
            [m_G] - Gewicht für Jungen
            [m_L] - Länge/Größe für Jungen
            [w_G] - Gewicht für Mädchen
            [w_L] - Länge/Größe für Mädchen""")
            daten_id = input("Wahlen Sie eine Option aus: ")
            daten_id = daten_id.strip()
            if daten_id in ["m_G", "m_L", "w_G", "w_G"]:
                arbeitsdatensatz = geladene_WHO_Daten[daten_id]
            else:
                print("\nUngültige Auswahl.")

            print(f"\nAktuell geladene Daten : {arbeitsdatensatz.get_info()}\n")
            input("Drücken Sie die Eingabetaste, um fortzufahren.\n")
            print()

        elif auswahl == "zeigen":

            print(f"\nAktuell geladene Daten : {arbeitsdatensatz.get_info()}\n")
            input("Drücken Sie die Eingabetaste, um fortzufahren.\n")

        elif auswahl in ["perzentil", "messwert", "diagramm", "erreicht"]:

            if not arbeitsdatensatz.einlesen_status():
                print("\nWählen Sie bitte einen Datensätz aus.\n")
                continue

            try:

                ak_mw = pz = 0.0

                ak_al = int(input(
                    "Geben Sie das aktuelles Alter des Kindes in vollendeten Monaten (Bereich: 0 bis 60 inklusive): "))

                if auswahl == "messwert":
                    pz = float(input("Geben Sie das Perzentil ein (Bereich: 0.0 bis 100.0 exklusive): "))
                else:
                    ak_mw = float(input(
                        "Geben Sie den aktuellen Messwert (Größe in cm oder Gewicht in kg) ein. Muss größer als 0.0 "
                        "sein.: "))

                einheit = "kg" if arbeitsdatensatz.get_eigenschaft() == "G" else "cm"

                if auswahl == "diagramm":

                    z_alter = input(
                        "Geben Sie ein Zielalter. Muss größer sein als das aktuelle Alter.(Bereich: 0 bis 60 "
                        "inklusive) (optionaler Parameter, kann leer sein) : ")
                    z_alter = z_alter.strip()
                    print("\nSie können die Prognose mit anderen Perzentilen aus den WHO-Daten vergleichen.")
                    print(
                        "Die Optionen sind : P01; P1; P3; P5; P10; P15; P25; P50; P75; P85; P90; P95; P97; P99; P999\n")
                    p_liste = input(
                        "Geben Sie die Perzentile im format x,z,y (Beispiel: P1,P5,P999): ")
                    perzentil_liste = p_liste.strip().split(",")

                    # der Wert von z_alter wird bereits innerhalb der Methode prognose_diagramm_erstellen überprüft.
                    # Hier wird geprüft, ob die Eingabe eine gültige Ziffer ist.
                    if z_alter and z_alter[0] == "+":
                        z_alter = z_alter[1:]

                    if z_alter.isdigit():
                        ziel_alter = int(z_alter)
                    else:
                        ziel_alter = 60

                    arbeitsdatensatz.prognose_diagramm_erstellen(ak_mw, ak_al, ziel_alter, perzentil_liste)

                elif auswahl == "erreicht":

                    zielmesswert = float(input(
                        "Geben Sie den Zielmesswert (Größe in cm oder Gewicht in kg) ein. Muss größer als 0.0 und der "
                        "aktuelle Messwert sein.: "))

                    result = arbeitsdatensatz.wann_wird_erreicht(ak_mw, zielmesswert, ak_al)

                    if result == -1:
                        print(f"\nZielmesswert wird nicht in ersten 60 Lebensmonate erreicht.\n")
                    else:
                        print(f"\nZielmesswert wird im Lebensmonat {result} erreicht.\n")

                elif auswahl == "perzentil":
                    print(
                        f"\nMesswert: {ak_mw} {einheit}| Alter: {ak_al} Monaten | Perzentil: {arbeitsdatensatz.perzentil_von_messwert_und_alter(ak_mw, ak_al)} %")

                else:
                    print(
                        f"\nMesswert: {arbeitsdatensatz.wert_von_perzentil_und_alter(pz, ak_al)} {einheit} | Alter: {ak_al} Monaten | Perzentil: {pz} %")

            except Exception as e:
                print(repr(e))

            input("\nDrücken Sie die Eingabetaste, um fortzufahren.\n")

        elif auswahl == "beenden":
            print("\nProgramm beendet.\n")
            input("Drücken Sie die Eingabetaste, um fortzufahren.\n")
            break
        else:
            print("\nUngültige Auswahl.\n")
            input("Drücken Sie die Eingabetaste, um fortzufahren.\n")
