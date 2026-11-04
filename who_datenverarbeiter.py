import pandas as pd  # pandas dataframe und für csv einlesen
import matplotlib
import matplotlib.pyplot as plt  # prognosediagramm erstellen
from matplotlib.widgets import Cursor
import matplotlib.ticker as ticker
from scipy.stats import norm  # normalverteilung
import math  # exp


class WHODatenverarbeiter:
    """
    Klasse zum Einlesen und Verarbeiten von Daten der WHO-Standards für Länge und Gewicht [1].

    Die Klasse lädt die Daten in den Arbeitsspeicher und bietet Methoden zur Berechnung von Perzentilen und Messwerten
    sowie zur Ermittlung an, ob bzw. wann ein Zielmesswert erreicht wird. Darüber hinaus ist
    es möglich, Diagramme mit Wachstumsprognosen zu erstellen.

    [1] WHO-Standards für Länge und Gewicht (https://www.who.int/tools/child-growth-standards/standards).

    """

    def __init__(self):
        """
        Initialisiert die Instanz.

        Die WHO-Daten müssen anschließend separat über die Methode 'who_daten_einlesen' geladen werden.
        """

        # Pandas-DataFrame mit den eingelesenen WHO-Daten (None, solange nichts erfolgreich geladen wurde)
        self.__dataframe = None
        # Gibt an, ob die WHO-Daten erfolgreich eingelesen wurden
        self.__einlesen_erfolgreich = False
        # Ursprüngliche CSV-Datei
        self.__dateiname = ""
        # Die Daten unterscheiden sich je nach Geschlecht. Dieses Attribut sollte immer entweder „m“ oder „w“ lauten.
        self.__geschlecht = ""
        # Kurze Beschreibung des Inhalts der Datei.
        self.__beschreibung = ""
        # Die in den Daten enthaltene physikalische Eigenschaft. Dieses Klassenattribut muss immer entweder „G“ für
        # das Gewicht oder „L“ für die Länge lauten.
        self.__eigenschaft = ""

    def get_info(self) -> str:
        """
        Gibt Informationen zu dieser Instanz des WHODatenverarbeiters zurück.

        :return: Informationen zu dieser Instanz (dateiname, geschlecht, eigenschaft, beschreibung, einlesen status)
        """

        eg = self.__eigenschaft
        if self.__eigenschaft == "G":
            eg = "Gewicht"
        elif self.__eigenschaft == "L":
            eg = "Länge"

        ges = self.__eigenschaft
        if self.__geschlecht == "m":
            ges = "Männlich"
        elif self.__geschlecht == "w":
            ges = "Weiblich"

        return (f"[Dateiname: {self.__dateiname} | Geschlecht: {ges} | Eigenschaft: {eg} |"
                f" Beschreibung: {self.__beschreibung} | Einlesen erfolgreich:  {self.__einlesen_erfolgreich}]")

    def get_eigenschaft(self) -> str:
        """
        Gibt die in den Daten enthaltene physikalische Eigenschaft zurück.

        :return: "G" für Gewicht, oder "L" für Länge/Größe
        """
        return self.__eigenschaft

    def einlesen_status(self) -> bool:
        """
        Gibt zurück, ob das Einlesen der WHO-Daten erfolgreich war.

        :return: True, wenn die Daten korrekt eingelesen wurden, andernfalls False.
        """
        return self.__einlesen_erfolgreich

    def who_daten_einlesen(self, dateiname: str, geschlecht: str, beschreibung: str, eigenschaft: str):
        """
        Liest die WHO-Datendatei und erstellt ein Pandas-DataFrame. Prüft, ob die angegebene Datei das richtige Format hat.

        Jedes Mal, wenn diese Funktion aufgerufen wird, werden die zuvor gelesenen Daten überschrieben.

        :param dateiname: Speicherort der WHO-Datendatei, zum Beispiel ".\\tab_lhfa_boys_p_0_5.csv"
        :param geschlecht: Die WHO Standards-Werte unterscheiden sich je nach Geschlecht. Dieser Parameter sollte immer entweder „m“ für Männlich oder „w“ für Weiblich lauten.
        :param eigenschaft: Die in den Daten enthaltenen physikalischen Eigenschaften. Dieses Klassenattribut muss immer entweder „G“ für das Gewicht oder „L“ für die Länge lauten.
        :param beschreibung: Kurze Beschreibung des Inhalts der Datei.
        """
        try:
            # In den WHO-Daten werden Kommas als Dezimaltrennzeichen und Semikolons als Spaltentrenner verwendet.
            # Alle numerischen Werte werden als Float eingelesen.
            self.__dataframe = pd.read_csv(dateiname, delimiter=";", decimal=",", dtype=float)  # csv Datei einlesen

            # Kurze Beschreibung des Inhalts der Datei.
            self.__beschreibung = beschreibung

            # überprüft die Zeilen
            if len(self.__dataframe) != 61:
                raise ValueError("Die Daten müssen aus 61 Zeilen mit Werten bestehen, "
                                 "wobei jeweils eine Zeile einem der ersten 60 Lebensmonate (0 inklusive) entspricht.")

            who_spalte = ["Month", "L", "M", "S", "P01", "P1", "P3", "P5", "P10", "P15", "P25", "P50", "P75",
                          "P85", "P90", "P95", "P97", "P99", "P999"]

            # überprüft die Spalten
            if list(self.__dataframe.columns) != who_spalte:
                raise ValueError((
                    "Die erwarteten Spalten sind [Month;L;M;S;P01;P1;P3;P5;P10;P15;P25;P50;P75;P85;P90;P95;P97;P99;P999]"))

            # Die WHO Standards-Werte unterscheiden sich je nach Geschlecht. Dieser Parameter
            # sollte immer entweder „m“ oder „w“ lauten.
            if geschlecht != "m" and geschlecht != "w":
                raise ValueError((
                    "Geschlecht muss entweder 'm' oder 'w' lauten."))
            else:
                self.__geschlecht = geschlecht

            # Die in den Daten enthaltenen physikalischen Eigenschaften. Dieses Klassenattribut muss
            # immer entweder „G“ für das Gewicht oder „L“ für die Länge lauten.
            if eigenschaft != "G" and eigenschaft != "L":
                raise ValueError((
                    "Eigenschaft muss entweder 'G' oder 'L' lauten."))
            else:
                self.__eigenschaft = eigenschaft

            self.__einlesen_erfolgreich = True
            self.__dateiname = dateiname
        except Exception as excep:
            print(repr(excep))

    def perzentil_von_messwert_und_alter(self, messwert: float, alter: int) -> float:
        """
        Berechnet anhand der LMS-Methode das Perzentil für einen Messwert und das Alter des Kindes in vollendeten Monaten.

        Weitere Informationen zur LMS-Methode finden sich in der Datei `lms_methode.txt`.

        Bei Messwerten, die unter dem 0,1-Perzentil oder über dem 99,9-Perzentil liegen, kann keine Genauigkeit garantiert werden (abweichende WHO-Extremwertbehandlung).

        Die berechneten Werte können von den offiziellen WHO-Tabellen abweichen. Die Werte in den Perzentil-Spalten sind auf eine Dezimalstelle gerundet. Der Unterschied bei dieser Methode kann spürbar sein.

        :param messwert: Messwert (z. B. Größe in cm oder Gewicht in kg). Muss größer als 0.0 sein.
        :param alter: Alter des Kindes in vollendeten Monaten (Bereich: 0 bis 60 inklusive).
        :return: Das berechnete Perzentil (0.0 bis 100.0)
        :raises ValueError: wenn `messwert` ≤ 0.0 ist oder `alter` nicht zwischen 0 und 60 liegt.
        :raises RuntimeError: wenn die WHO-Daten nicht eingelesen werden konnten.
        """

        # überprüfung der Parameter
        if not self.__einlesen_erfolgreich:
            raise RuntimeError("Fehler beim Einlesen der WHO-Daten.")

        if not (0 <= alter <= 60):
            raise ValueError("Alter des Kindes in vollendeten Monaten muss zwischen 0 und 60 liegen (inklusive).")

        if messwert <= 0.0:
            raise ValueError("Messwert muss größer als 0.0 sein.")

        # LMS methode
        l = self.__dataframe.at[alter, "L"]
        m = self.__dataframe.at[alter, "M"]
        s = self.__dataframe.at[alter, "S"]

        # Die verwendete Formel hängt vom Wert von L ab.
        if l == 0.0:
            z = math.log(messwert / m) / s
        else:
            z = (((messwert / m) ** l) - 1.0) / (l * s)

        # kumulative Verteilungsfunktion (CDF) der Standardnormalverteilung
        perzentil = norm.cdf(z) * 100

        return perzentil

    def wert_von_perzentil_und_alter(self, perzentil: float, alter: int) -> float:
        """
        Berechnet anhand der LMS-Methode den Messwert für ein Perzentil und das Alter des Kindes in Monaten.

        Weitere Informationen zur LMS-Methode finden sich in der Datei `lms_methode.txt`.

        Bei Perzentilen, die kleiner als 0.01 oder größer als 99.9 liegen, kann keine Genauigkeit garantiert werden (abweichende WHO-Extremwertbehandlung).

        Die berechneten Werte können von den offiziellen WHO-Tabellen abweichen. Die Werte in den Perzentil-Spalten sind auf eine Dezimalstelle gerundet. Der Unterschied bei dieser Methode ist minimal.

        :param perzentil: Das Perzentil für das Wachstum des Kindes (Bereich: 0.0 bis 100.0 exklusive).
        :param alter: Alter des Kindes in vollendeten Monaten (Bereich: 0 bis 60 inklusive).
        :return: Der berechnete Messwert.
        :raises ValueError: wenn `perzentil` ≤ 0.0 oder `perzentil` >= 100.0 ist, oder `alter` nicht zwischen 0 und 60 liegt.
        :raises RuntimeError: wenn die WHO-Daten nicht eingelesen werden konnten.
        """

        # überprüfung der Parameter
        if not self.__einlesen_erfolgreich:
            raise RuntimeError("Fehler beim Einlesen der WHO-Daten.")

        if not (0 <= alter <= 60):
            raise ValueError("Alter des Kindes in Monaten muss zwischen 0 und 60 liegen (inklusive).")

        if not (0.0 < perzentil < 100.0):
            raise ValueError("Perzentil muss größer als 0.0 und kleiner als 100.0 sein.")

        # LMS methode
        l = self.__dataframe.at[alter, "L"]
        m = self.__dataframe.at[alter, "M"]
        s = self.__dataframe.at[alter, "S"]

        #  umkehrfunktion der kumulativen Verteilungsfunktion (CDF) der Standardnormalverteilung
        z = norm.ppf(perzentil / 100)

        # Die verwendete Formel hängt vom Wert von L ab.
        if l == 0.0:
            messwert = m * (math.exp(s * z))
        else:
            messwert = m * ((1.0 + l * s * z) ** (1 / l))

        return messwert

    def wann_wird_erreicht(self, aktueller_messwert: float, ziel_messwert: float, aktuelles_alter: int) -> int:
        """
        Ermittelt anhand der angegebenen Eingabewerte, in welchem Lebensmonat der Zielmesswert erreicht wird, sofern dies in den ersten 60 Lebensmonaten überhaupt möglich ist.

        :param aktueller_messwert: Messwert (z. B. Größe in cm oder Gewicht in kg). Muss größer als 0.0 sein.
        :param ziel_messwert: Messwert, der bis zum 60. Lebensmonat erreicht sein muss. Muss größer als aktueller_messwert sein.
        :param aktuelles_alter: aktuelles Alter des Kindes in vollendeten Monaten (Bereich: 0 bis 60 inklusive).
        :return: Das Alter in vollendeten Monaten, in dem der Zielmesswert erreicht wird, oder -1, wenn dieser in den ersten 60 Lebensmonaten nicht erreicht wird,
        :raises ValueError: wenn `aktueller_messwert` ≤ 0.0 ist, `ziel_messwert` ≤ `aktueller_messwert` ist oder `alter` nicht zwischen 0 und 60 liegt,
        :raises RuntimeError: wenn die WHO-Daten nicht eingelesen werden konnten.
        """

        # überprüfung der Parameter
        if not self.__einlesen_erfolgreich:
            raise RuntimeError("Fehler beim Einlesen der WHO-Daten.")

        if not (0 <= aktuelles_alter <= 60):
            raise ValueError("Aktuelles Alter des Kindes in Monaten muss zwischen 0 und 60 liegen (inklusive).")

        if aktueller_messwert <= 0.0:
            raise ValueError("Messwert muss größer als 0.0 sein.")

        if aktueller_messwert >= ziel_messwert:
            raise ValueError("Der Zielmesswert muss größer sein als der aktuelle Messwert.")

        perzentil = self.perzentil_von_messwert_und_alter(aktueller_messwert, aktuelles_alter)

        for alt in range(aktuelles_alter, 61):
            if self.wert_von_perzentil_und_alter(perzentil, alt) >= ziel_messwert:
                # zielmesswert erreicht, gibt das lebensmonat zurück
                return alt

        # zielmesswert wurde nicht erreicht
        return -1

    def prognose_diagramm_erstellen(self, messwert: float, aktuelles_alter: int, ziel_alter: int = 60,
                                    perzentil_liste=None):
        """
        Erstellt ein Diagramm mit einer Prognose, die auf einem Messwert, dem aktuellen Alter des Kindes (in vollendeten Monaten) und einem Zielalter (in vollendeten Monaten) basiert.

        Die Grafik beginnt beim angegebenen aktuellen Alter und endet beim Zielalter (wenn nichts angegeben ist, beim 60. Lebensmonat).

        Liegt eine Liste von Perzentilen vor, kann auch ein Vergleich mit den WHO-Perzentilkurven angezeigt werden.

        Bei Messwerten, die unter dem 0,1-Perzentil oder über dem 99,9-Perzentil liegen, kann keine Genauigkeit garantiert werden (abweichende WHO-Extremwertbehandlung).

        :param messwert: Messwert (z. B. Größe in cm oder Gewicht in kg). Muss größer als 0.0 sein.
        :param aktuelles_alter: aktuelles Alter des Kindes in vollendeten Monaten (Bereich: 0 bis 60 inklusive).
        :param ziel_alter: Zielalter des Kindes in vollendeten Monaten. Muss größer als aktuelles_alter sein. (Bereich: 0 bis 60 inklusive).
        :param perzentil_liste: die Prognose kann mit den Perzentilkurven aus der eingegebenen Liste verglichen werden. Gültige Werte sind Strings in [P01,P1,P3,P5,P10,P15,P25,P50,P75,P85,P90,P95,P97,P99,P999]
        :raises ValueError: wenn `messwert` ≤ 0.0 ist oder `alter` nicht zwischen 0 und 60 liegt.
        :raises RuntimeError: wenn die WHO-Daten nicht eingelesen werden konnten.
        """

        # überprüfung der Parameter

        if not self.__einlesen_erfolgreich:
            raise RuntimeError("Fehler beim Einlesen der WHO-Daten.")

        if not (0 <= aktuelles_alter <= 60):
            raise ValueError("Aktuelles Alter des Kindes in Monaten muss zwischen 0 und 60 liegen (inklusive).")
        if not (0 <= ziel_alter <= 60):
            raise ValueError("Zielalter des Kindes in Monaten muss zwischen 0 und 60 liegen (inklusive).")
        if aktuelles_alter >= ziel_alter:
            raise ValueError("Das Zielalter muss größer sein als das aktuelle Alter.")

        if messwert <= 0.0:
            raise ValueError("Messwert muss größer als 0.0 sein.")

        if perzentil_liste is None:
            perzentil_liste = []

        # Aus dem Messwert und dem Alter lässt sich ein Perzentil berechnen.
        perzentil = self.perzentil_von_messwert_und_alter(messwert, aktuelles_alter)

        # Mithilfe des Perzentils kann man eine Liste mit prognostizierten Werten erstellen.
        alter_liste = [x for x in range(aktuelles_alter, ziel_alter + 1)]
        prognostizierte_messwerte_liste = []
        for al in range(len(alter_liste)):
            prognostizierte_messwerte_liste.append(
                self.wert_von_perzentil_und_alter(perzentil, alter_liste[al]))

        # perzentil_liste muss verarbeitet werden, um Duplikate und falsche Eingabe zu entfernen
        # Beispiel: ["r","p50","P25","P25","P5","p1","P90","P75"] -> ["P5","P25","P50","P75","P90"]
        # python-Sets können Duplikate entfernen
        perzentil_set = set(perzentil_liste)
        # gültige Eingabewerte
        who_perzentile_set = {"P01", "P1", "P3", "P5", "P10", "P15", "P25", "P50", "P75", "P85", "P90", "P95", "P97",
                              "P99",
                              "P999"}
        # Schnittmenge kann falsche Eingabe entfernen
        # sorted() gibt immer eine Liste zurück
        perzentil_liste = sorted(perzentil_set & who_perzentile_set)

        # Erstellt anhand der WHO-Daten ein dict auf der Grundlage der Elemente in der perzentil_liste,
        # um diese zusammen mit den Elementen in prognostizierte_messwerte_liste grafisch darzustellen.
        who_perzen_zu_plotten = {}
        for p in perzentil_liste:
            who_perzen_zu_plotten[p] = self.__dataframe[p].to_numpy()[aktuelles_alter:ziel_alter + 1]


        # plotten mit matplotlib mit maus Cursor, andere Perzentilkurven, minorticks, legend, grid
        matplotlib.use("TkAgg")

        fig, ax = plt.subplots()

        # perzentilkurve, die von Eingabewerten erstellt wurde
        fig.canvas.manager.set_window_title(f"Wachstumsprognose : {self.get_info()}")
        ax.set_title(f"Wachstumsprognose : {self.get_info()}")
        ax.plot(alter_liste, prognostizierte_messwerte_liste, label=f"prognose P {perzentil:.2f}", marker="s",
                linestyle="dashed")

        # WHO Perzentilkurven plotten
        for k in who_perzen_zu_plotten:
            ax.plot(alter_liste, who_perzen_zu_plotten[k], label=k)

        # achse-labels
        if self.__eigenschaft == "G":
            ax.set_ylabel(f"Messwerte (kg)")
        else:
            ax.set_ylabel("Messwerte (cm)")

        ax.set_xlabel("Alter (Monaten)")

        # minor ticks, grid und legend, zur Verbesserung der Lesbarkeit
        ax.minorticks_on()
        ax.xaxis.set_minor_formatter(ticker.ScalarFormatter())
        ax.yaxis.set_minor_formatter(ticker.ScalarFormatter())
        ax.tick_params(
            axis='both',
            which='minor',
            labelsize=8,
            labelcolor='gray',
            length=3
        )

        ax.grid(True)
        ax.legend()

        # maus cursor
        fig._cursor = Cursor(
            ax,
            useblit=True,
            color='red',
            linewidth=1,
            linestyle='--'
        )

        # eingabewerte unten zeigen
        fig.text(0.5, 0.01, f"[Messwert: {messwert} | Aktuelles Alter: {aktuelles_alter} | Perzentil: {perzentil:.2f}]",
                 ha='center', fontsize=12)

        plt.subplots_adjust(bottom=0.1)

        plt.show()


# Testbereich
if __name__ == "__main__":
    # 'j' für testen
    eingabe = input("WHODatenverarbeiter testen? [j] : ")
    if eingabe == "j":

        # eingabewerte für testen
        test_perzentile_liste = [0.0, 100.0, 50.0, 50.0, 50.0]
        test_messwerte_liste = [0.0, -30.0, 30.0, 30.0, 91.9]
        test_alter_liste = [30, 30, -1, 70, 30]

        print("test : daten erfolgreich einlesen")
        test_laenge_junge1 = WHODatenverarbeiter()
        try:
            test_laenge_junge1.who_daten_einlesen(".\\who_daten\\tab_lhfa_boys_p_0_5.csv", "m",
                                                  "länge - jungen", "L")
        except Exception as e:
            print(repr(e))
        print("test_laenge_junge1 einlesen_status : ", test_laenge_junge1.einlesen_status())
        print()

        print("test : methode perzentil_von_messwert_und_alter")
        print(
            "messwerte muss > 0.0, messwerte muss > 0.0, alter muss zwischen 0 und 60 inklusive, "
            "alter muss zwischen 0 und 60 inklusive, normalfall")
        for i in range(len(test_messwerte_liste)):
            try:
                test_result = test_laenge_junge1.perzentil_von_messwert_und_alter(test_messwerte_liste[i],
                                                                                  test_alter_liste[i])
                print(f"test_result = {test_result}")
            except Exception as e:
                print(repr(e))
        print()

        print("test : zweimal who_daten_einlesen aufrufen")
        try:
            test_laenge_junge1.who_daten_einlesen(".\\who_daten\\tab_lhfa_girls_p_0_5.csv",
                                                  "w", "länge - mädchen", "L")
        except Exception as e:
            print(repr(e))
        print("test_laenge_junge1 jetzt mit maedchen werte einlesen_status : ", test_laenge_junge1.einlesen_status())
        print()

        print("test : falsch geschlecht eingeben")
        try:
            test_laenge_junge1.who_daten_einlesen(".\\who_daten\\tab_lhfa_boys_p_0_5.csv", "k",
                                                  "länge - jungen", "L")
        except Exception as e:
            print(repr(e))
        print("test_laenge_junge1 einlesen_status : ", test_laenge_junge1.einlesen_status())
        print()

        print("test : daten hat nicht genug zeilen")
        test_laenge_junge2 = WHODatenverarbeiter()
        try:
            test_laenge_junge2.who_daten_einlesen(".\\who_test_daten\\tab_lhfa_boys_p_0_5_falsch.csv",
                                                  "m", "länge - jungen", "L")
        except Exception as e:
            print(repr(e))
        print("test_laenge_junge2 einlesen_status : ", test_laenge_junge2.einlesen_status())
        print()

        print("test : datei existiert nicht")
        test_laenge_junge3 = WHODatenverarbeiter()
        try:
            test_laenge_junge3.who_daten_einlesen(".\\who_daten\\tabsboys_p_0_5.csv", "m",
                                                  "länge - jungen", "L")
        except Exception as e:
            print(repr(e))
        print("test_laenge_junge3 einlesen_status : ", test_laenge_junge3.einlesen_status())
        print()

        print("test : datei hat falsche spalte")
        test_laenge_maedchen1 = WHODatenverarbeiter()
        try:
            test_laenge_maedchen1.who_daten_einlesen(".\\who_test_daten\\tab_lhfa_girls_p_0_5_falsch.csv",
                                                     "w", "länge - mädchen", "L")
        except Exception as e:
            print(repr(e))
        print("test_laenge_maedchen1 einlesen_status : ", test_laenge_maedchen1.einlesen_status())
        print()

        print("test : methode wert_von_perzentil_und_alter")
        test_laenge_maedchen2 = WHODatenverarbeiter()
        try:
            test_laenge_maedchen2.who_daten_einlesen(".\\who_daten\\tab_lhfa_girls_p_0_5.csv", "w",
                                                     "länge - mädchen",
                                                     "L")
        except Exception as e:
            print(repr(e))
        print("test_laenge_maedchen2 einlesen_status : ", test_laenge_maedchen2.einlesen_status())

        print(
            "perzentil muss > 0.0, perzentil muss < 100.0, alter muss zwischen 0 und 60 inklusive, "
            "alter muss zwischen 0 und 60 inklusive, normalfall")
        for i in range(len(test_messwerte_liste)):
            try:
                test_result = test_laenge_maedchen2.wert_von_perzentil_und_alter(test_perzentile_liste[i],
                                                                                 test_alter_liste[i])
                print(f"test_result = {test_result}")
            except Exception as e:
                print(repr(e))

        print()

        print("test : werte in der datei sind nicht alle nummern")
        test_gewicht_maedchen1 = WHODatenverarbeiter()
        try:
            test_gewicht_maedchen1.who_daten_einlesen(".\\who_test_daten\\tab_wfa_girls_p_0_5_falsch.csv",
                                                      "w", "gewicht - mädchen", "G")
        except Exception as e:
            print(repr(e))
        print("test_gewicht_maedchen1 einlesen_status : ", test_gewicht_maedchen1.einlesen_status())
        print()

        print("Beispiel dafür, wie die Funktion wert_von_perzentil_und_alter die Rundung der "
              "WHO-Daten berücksichtigt.")
        print("Der Unterschied ist minimal")
        print("wert_von_perzentil_und_alter test mit alter 30 und datei tab_lhfa_girls_p_0_5.csv : ")
        print("Die WHO-Tabellewerte sind  perzentil:15  messwert:87  alter:30")
        test_perzentile_liste = [14.8, 14.9, 14.95, 14.98, 14.999, 15.0, 15.01, 15.05, 15.09, 15.1, 15.2, 15.3]
        for i in range(len(test_perzentile_liste)):
            try:
                print("perzentil :", test_perzentile_liste[i], "messwert : ",
                      test_laenge_maedchen2.wert_von_perzentil_und_alter(test_perzentile_liste[i], 30))
            except Exception as e:
                print(repr(e))
        print()

        print(
            "Beispiel dafür, wie die Funktion perzentil_von_messwert_und_alter die Rundung der "
            "WHO-Daten berücksichtigt.")
        print("Der Unterschied bei dieser Funktion kann deutlich spürbar sein.")
        print("perzentil_von_messwert_und_alter test mit alter 30 und datei tab_lhfa_girls_p_0_5.csv : ")
        print("Die WHO-Tabellewerte sind  perzentil:15  messwert:87  alter:30")
        test_messwerte_liste = [86.8, 86.9, 86.95, 86.98, 86.999, 87.0, 87.01, 87.05, 87.09, 87.1, 87.2, 87.3]
        for i in range(len(test_messwerte_liste)):
            try:
                print("messwert :", test_messwerte_liste[i], "perzentil : ",
                      test_laenge_maedchen2.perzentil_von_messwert_und_alter(test_messwerte_liste[i], 30))
            except Exception as e:
                print(repr(e))
        print()

        print("test : methode prognose_diagramm_generieren")

        print("normalfall")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(92.0, 30)
        except Exception as e:
            print(repr(e))

        print("messwert falsch - nichts plotten")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(-92.0, 30, 60)
        except Exception as e:
            print(repr(e))

        print("aktuelles alter falsch - nichts plotten")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(92.0, 70, 60)
        except Exception as e:
            print(repr(e))

        print(
            "alter 60 - soll nicht funktionieren, weil standard wert für ziel_alter=60, ziel_alter muss "
            "größer als aktuelles alter sein")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(109.9638, 60)
        except Exception as e:
            print(repr(e))

        print("alter 59 - soll kleines Diagramm plotten")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(108.8948, 59, 60)
        except Exception as e:
            print(repr(e))

        print("vergleichen mit anderen Perzentile - [P10, P50, P999] - soll P10,P50,P999 plotten")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(92.0, 30, 60,
                                                              ["P10", "P50", "P999"])
        except Exception as e:
            print(repr(e))

        print("vergleichen mit anderen Perzentile - [r, p50, P999] - soll nur P999 plotten")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(92.0, 30, 60,
                                                              ["r", "p50", "P999"])
        except Exception as e:
            print(repr(e))

        print("vergleichen mit anderen Perzentile - [P25, P25, P75, P50] - soll P25,P50,P75 plotten")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(92.0, 30, 60,
                                                              ["P25", "P25", "P75", "P50"])
        except Exception as e:
            print(repr(e))

        print("vergleichen mit anderen Perzentile - [] - wie normalfall")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(92.0, 30, 60, [])
        except Exception as e:
            print(repr(e))

        print("ziel_alter zu groß - nichts plotten")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(92.0, 30, 70, [])
        except Exception as e:
            print(repr(e))

        print("ziel_alter kleiner als aktuelles_alter - nichts plotten")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(92.0, 30, 20, [])
        except Exception as e:
            print(repr(e))

        print("ziel_alter == aktuelles_alter - nichts plotten")
        try:
            test_laenge_maedchen2.prognose_diagramm_erstellen(92.0, 30, 30, [])
        except Exception as e:
            print(repr(e))

        print("einlesen erfolglos - nichts plotten")
        try:
            test_laenge_maedchen1.prognose_diagramm_erstellen(92.0, 30, 60)
        except Exception as e:
            print(repr(e))

        print()

        print("test : methode wann_wird_erreicht")

        print("normalfall")
        try:
            r = test_laenge_maedchen2.wann_wird_erreicht(92.0, 100.0, 30)
            print(f"Erreicht in : {r} Monaten")
        except Exception as e:
            print(repr(e))

        print("einlesen erfolglos")
        try:
            r = test_laenge_maedchen1.wann_wird_erreicht(92.0, 100.0, 30)
            print(f"Erreicht in : {r} Monaten")
        except Exception as e:
            print(repr(e))

        print("ziel_messwert == aktuelles_messwert")
        try:
            r = test_laenge_maedchen2.wann_wird_erreicht(100.0, 100.0, 30)
            print(f"Erreicht in : {r} Monaten")
        except Exception as e:
            print(repr(e))

        print("ziel_messwert < aktuelles_messwert")
        try:
            r = test_laenge_maedchen2.wann_wird_erreicht(100.0, 90.0, 30)
            print(f"Erreicht in : {r} Monaten")
        except Exception as e:
            print(repr(e))

        print("alter falsch")
        try:
            r = test_laenge_maedchen2.wann_wird_erreicht(90.0, 100.0, 70)
            print(f"Erreicht in : {r} Monaten")
        except Exception as e:
            print(repr(e))
