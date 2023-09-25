Tangente Neomatik README

In diesem README finden Sie alle nötigen Informationen zum Programm „Tangente Neomatik.exe“ sowie dessen Installationsprogramm.
Das Design von „Tangente Neomatik.exe“ ist eine Adaption der Armbanduhr „Tangente Sport Neomatik 42 Date“ der Uhrenmanufaktur „NOMOS Glashütte/SA“.
Es dient nicht dem Gewinnerwerb und ist lediglich für den privaten Gebrauch vorgesehen.

„Tangente Neomatik.exe“ zeigt die momentane Systemzeit des PC und den Tag des Monats an.
Darüber hinaus verfügt es über zwei weitere Funktionen: „Schlafen“ und „Schlummern“.

- Schlafen:
Wird die Schaltfläche „Schlafen“ betätigt, geht das Programm in einen Energiesparmodus über. Die Anzeige wird weißlich überdeckt und die Uhr bleibt stehen.
In diesem Modus sinken der Stromverbrauch und die benötigte Rechenleistung des Programms. Durch erneutes Klicken auf die nun als „Wecken“ bezeichnete
Schaltfläche geht das Programm in den normalen Zustand über und die Uhr wird automatisch auf die richtige Zeit gestellt.
- Schlummern:
Da das Programm für die meiste Zeit im Hintergrund läuft, wurde ein weiterer automatischer Energiesparmodus implementiert. Wenn sich das Programm im
Hintergrund befindet, geht es von selbst in den Schlummermodus. In diesem Zustand läuft die Uhr weiter, jedoch mit reduzierter Bildrate. Sobald sich das
Programm wieder im Vordergrund befindet, wird der Schlummermodus automatisch wieder deaktiviert und die Uhr läuft normal weiter. Die Funktionalität des
Schlummermodus kann über die Schaltfläche „Schlummern aktivieren“ bzw. „Schlummern deaktivieren“ kontrolliert werden.

Falls Sie mit den Bildraten von „Tangente Neomatik.exe“ nicht zufrieden sind (Anzeige ist nicht sanft genug, Programm verbraucht zu viel Leistung, etc.),
können Sie die Einstellungen des Programms manuell bearbeiten. Öffnen Sie dazu den Ordner, in dem „Tangente Neomatik.exe“ installiert ist. Dort finden Sie
den Unterordner „settings“, in dem sich die Datei „settings.json“ befindet. Öffnen Sie diese Datei nun mit einem Textbearbeitungsprogramm Ihrer Wahl.
Die „fps“-Werte geben Maximalwerte für die Bildfrequenz des Programms an. Höhere Werte entsprechen einer geschmeidigeren Anzeige, niedrige Werte
reduzieren den Stromverbrauch und die benötigte Rechenleistung. Für unbegrenzte Bildfrequenz (beste Anzeige, höchster Stromverbrauch) setzen Sie den
entsprechenden Wert auf 0. Sie können die Zahlenwerte nach Belieben ändern. Die Werte kontrollieren folgende Aspekte von „Tangente Neomatik.exe“:

- „fps“: Bildrate im Normalzustand
- „slumber fps“: Bildrate im Schlummermodus
- „sleep fps“: Bildrate im Schlafmodus
- „slumber enabled“: Automatisches Energiesparen (kann im Programm über die Schaltfläche geändert werden, siehe „Schlummern“)

Bitte ändern Sie die Einstellungen nur, wenn „Tangente Neomatik.exe“ nicht ausgeführt wird. Falls Sie beim Ändern der Einstellungen einen Fehler machen
oder Sie die Datei „settings.json“ löschen, wird diese beim nächsten Start von „Tangente Neomatik.exe“ auf die Standardeinstellungen zurückgesetzt.

Um „Tangente Neomatik.exe“ sowie alle zugehörigen Verknüpfungen zu installieren, benötigen sie das Programm „Installer.exe“. Wenn Sie das
Installationsprogramm als Administrator ausführen, können Sie die für Sie relevanten Optionen auswählen.

- Installationsordner: Der Ordner, in dem „Tangente Neomatik.exe“ installiert wird. Bestenfalls ist der angegebene Ordner leer oder existiert noch nicht.
- Desktopverknüpfung: Eine Schnellstart-Verknüpfung auf der Startseite Ihres PC.
- Auto Start: „Tangente Neomatik.exe“ wird automatisch gestartet, wenn Sie Ihren PC hochfahren.
- Start-Menü: Hiermit können Sie „Tangente Neomatik.exe“ im Windows Menü suchen, nachdem sie die Windows-Taste gedrückt haben. (empfohlen)

Um den Installationsordner von „Tangente Neomatik.exe“ wiederzufinden, wird mindestens die Desktopverknüpfung oder die Start-Menü-Verknüpfung empfohlen.
Falls Sie sich dazu entschließen, „Tangente Neomatik.exe“ deinstallieren zu wollen, müssen Sie dies manuell tun. Hierzu müssen Sie folgende Dateien
von Ihrem PC löschen:

1. Den Installationsordner bzw. sämtliche Dateien darin:
Finden Sie dazu lediglich den Installationsordner und löschen Sie alles.
2. (Optional) Die Desktopverknüpfung:
Suchen Sie „Tangente Neomatik.exe“ auf Ihrem Startbildschirm oder im Ordner „C:/Users/[NUTZERNAME]/Desktop“
3. (Optional) Die Auto-Start-Verknüpfung:
Verwenden Sie die Tastenkombination „Win + R“ und geben Sie „shell:startup“ ein. Dort befindet sich die Auto-Start-Verknüpfung.
Alternativ können Sie den Ordner „C:/Users/[NUTZERNAME]/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup“ auch manuell öffnen.
4. (Optional) Die Start-Menü-Verknüpfung:
Folgen Sie den Anweisungen von 3. und navigieren Sie in den darüberliegenden Ordner „Programs“.

Die mit (Optional) beschrifteten Anweisungen treffen nur dann zu, falls Sie die entsprechenden Verknüpfungen im Installationsprozess angegeben haben.
Ersetzen Sie außerdem [Nutzername] gegen den Namen des momentanen Benutzers.

Ich wünsche Ihnen viel Spaß mit dem Programm „Tangente Neomatik.exe“. Sollten Sie Fragen oder Probleme bezüglich des Programms oder des Installations-
oder Deinstallationsprozess haben, wenden Sie sich an mich via [Github](https://github.com/MrHxID/Watch/issues).