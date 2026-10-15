# Datenschutzerklärung für Finplanr

**Stand: 15. Oktober 2026**

## 1. Verantwortlicher

Verantwortlich für die Verarbeitung personenbezogener Daten im Zusammenhang mit der Website https://finplanr.net ist:

{{OPERATOR_NAME}}  
{{ADDRESS_BLOCK}}  
E-Mail: {{EMAIL}}

Weitere Angaben zum Betreiber findest du im Impressum: {{IMPRESSUM_URL}}

Ein Datenschutzbeauftragter ist nicht benannt, da hierzu keine gesetzliche Pflicht besteht. Für alle Fragen zum Datenschutz erreichst du den Verantwortlichen unter der oben genannten Adresse.

## 2. Allgemeines zur Datenverarbeitung

Finplanr ist eine kostenlos nutzbare Webanwendung zur Planung und Aufteilung monatlicher Sparbeträge auf verschiedene Anlageklassen wie ETFs, ETCs, Kryptowährungen und Tagesgeld. Die Anwendung ist ohne Registrierung oder Benutzerkonto nutzbar. Es gibt keine Werbung, kein Tracking und keine Analysedienste.

Finplanr verwendet keine zentrale Datenbank für individuelle Portfolios. Deine Eingaben (Beträge, Gewichtungen, Namen, Kennungen) werden ausschließlich im Browser auf deinem Gerät gespeichert und nicht an den Betreiber übertragen.

Personenbezogene Daten werden dennoch in folgenden Fällen verarbeitet:

- bei jedem Aufruf der Website (technische Zugriffsdaten, Abschnitt 3),
- wenn du die lokale Speicherung im Browser nutzt (Abschnitt 4),
- wenn du ein Kurschart von TradingView erlaubst und lädst (Abschnitte 5 und 6, nur mit deiner Einwilligung),
- wenn du die optionale Online-Suche erlaubst und nutzt (Abschnitte 5 und 7, nur mit deiner Einwilligung),
- wenn du ein Logo oder Bild von einem externen Anbieter auswählst (Abschnitt 8),
- wenn du uns per E-Mail kontaktierst (Abschnitt 9).

Zwei Funktionen nehmen Kontakt zu Dritten auf und brauchen deshalb deine vorherige, ausdrückliche Einwilligung: **Kurscharts** (TradingView) und **Online-Suche** (CoinGecko, Wikidata, Wikimedia Commons). Solange du in eine Funktion nicht eingewilligt hast, sendet dein Browser nichts an die Anbieter dieser Funktion. Die Suche im integrierten Katalog läuft lokal in deinem Browser und braucht keine Einwilligung.

Bei einem normalen Seitenaufruf ohne diese Aktionen werden keine Daten an andere Drittanbieter als Cloudflare (Abschnitt 3) übermittelt. Alle Skripte, Stile und Logos der Anwendung werden von unserem eigenen Server geliefert; es werden keine Webschriften oder Skripte von Dritten nachgeladen. Cloudflare kann bei der Auslieferung allerdings ein eigenes Sicherheitsskript einfügen und ein technisch erforderliches Cookie setzen (Abschnitte 3 und 10).

## 3. Bereitstellung der Website, Hosting, Cloudflare und Server-Logs

Die Website wird auf einem privat betriebenen Server des Betreibers mit einem Nginx-Webserver in einem Docker-Container bereitgestellt. Der Server ist nicht direkt aus dem Internet erreichbar, sondern ausschließlich über einen Cloudflare Tunnel.

Für DNS, die verschlüsselte HTTPS-Verbindung, die Weiterleitung der Anfragen an unseren Server (Cloudflare Tunnel), die Zwischenspeicherung statischer Dateien (CDN) und technische Sicherheitsfunktionen setzen wir Cloudflare ein. Deine Anfragen laufen deshalb über die Server von Cloudflare. Cloudflare entschlüsselt die Verbindung dabei technisch, um sie an unseren Server weiterzuleiten.

**Anbieter:** Cloudflare, Inc., 101 Townsend St., San Francisco, CA 94107, USA, sowie verbundene Unternehmen (u. a. in der EU).

**Von Cloudflare verarbeitete Daten:** Bei jedem Aufruf werden insbesondere verarbeitet:

- IP-Adresse
- Datum und Uhrzeit des Zugriffs
- aufgerufene Seite bzw. angeforderte Datei und HTTP-Statuscode
- übertragene Datenmenge
- Referrer (Seite, von der du kommst), soweit dein Browser ihn sendet
- Browsertyp, Browserversion und Betriebssystem (User-Agent)
- ungefährer Standort (Land), den Cloudflare aus der IP-Adresse ableitet
- technische Verbindungs- und Browsermerkmale (zum Beispiel die TLS-Protokollversion) sowie Sicherheitsdaten, die zur Erkennung und Abwehr missbräuchlicher oder automatisierter Zugriffe ausgewertet werden

**Bot-Erkennung und Cookie von Cloudflare:** Cloudflare fügt beim Ausliefern unserer Seiten ein kleines Skript ein („JavaScript Detections“). Es wird über unsere eigene Domain geladen (Pfad `/cdn-cgi/`), läuft im Hintergrund, prüft technische Merkmale deines Browsers, um automatisierte Zugriffe (Bots) von menschlichen Besuchen zu unterscheiden, und übermittelt das Ergebnis an Cloudflare. Dabei setzt Cloudflare das Cookie `cf_clearance` (siehe Abschnitt 10). Das dient der Sicherheit, nicht der Reichweitenmessung oder Werbung; wir nutzen diese Daten nicht für eigene Auswertungen.

**Server-Logs auf unserem Server:** Das Zugriffsprotokoll unseres Webservers ist bewusst auf folgende Angaben je Anfrage beschränkt: Zeitpunkt der Anfrage, HTTP-Methode, angeforderter Pfad (ohne Query-String), Statuscode und Größe der Antwort. Es enthält **keine IP-Adresse** (auch keine vom Cloudflare Tunnel weitergegebene Adresse), **keinen Referrer und keinen User-Agent**. Nach unserer Einschätzung enthält das Zugriffsprotokoll deshalb keine personenbezogenen Daten. Das Fehlerprotokoll des Webservers (technische Fehlermeldungen, zum Beispiel bei blockierten Anfragen) kann zusätzlich die Adresse des verbindenden Clients, die angeforderte Adresse und, falls gesendet, den Referrer enthalten; hinter dem Tunnel ist die Client-Adresse die interne Adresse des Tunnel-Connectors auf unserem Server, nicht deine Adresse. Auch der Tunnel-Connector (cloudflared) schreibt auf unserem Server ein Protokoll; in der von uns verwendeten Standard-Protokollstufe enthält es Verbindungs-, Status- und Fehlermeldungen des Tunnels, aber keine einzelnen Seitenaufrufe und keine Besucheradressen. Wir werten die Protokolle nicht systematisch aus, führen sie nicht mit anderen Daten zusammen und erstellen keine Nutzerprofile. Sie werden nur zur Fehlersuche herangezogen.

**Cloudflare Network Error Logging:** Cloudflare bietet eine optionale Funktion an, die Browser auffordert, Netzwerkfehlerberichte an eine Meldeadresse von Cloudflare zu senden. Wir haben diese Funktion deaktiviert; dein Browser wird deshalb nicht aufgefordert, solche Berichte zu senden.

**Zweck und Rechtsgrundlage:** Die Verarbeitung dient dazu, die Website stabil und funktionsfähig bereitzustellen und Angriffe abzuwehren. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse am zuverlässigen und gesicherten Betrieb der Website, am Schutz vor Angriffen und automatisiertem Missbrauch). Das Cookie und das Sicherheitsskript von Cloudflare halten wir nach unserer Einschätzung für den gesicherten und stabilen Betrieb des von dir aufgerufenen Dienstes technisch erforderlich (§ 25 Abs. 2 Nr. 2 TDDDG).

**Rolle von Cloudflare:** Soweit Cloudflare Daten in unserem Auftrag verarbeitet (insbesondere die Protokolle des Datenverkehrs), handelt es als Auftragsverarbeiter nach Art. 28 DSGVO. Dazu besteht ein Auftragsverarbeitungsvertrag (Data Processing Addendum, DPA) mit Cloudflare, der nach Angaben von Cloudflare die EU-Standardvertragsklauseln einbezieht. Für einzelne Daten ist Cloudflare nach eigener Aussage selbst Verantwortlicher; Einzelheiten stehen in der Datenschutzerklärung von Cloudflare: https://www.cloudflare.com/privacypolicy/

**Speicherdauer:** Die Protokolle auf unserem Server (Webserver und Tunnel-Connector) werden von Docker automatisch nach Größe rotiert (je Protokoll höchstens drei Dateien von je 10 MB); ältere Einträge werden überschrieben. Wie lange ein Eintrag vorhanden ist, hängt vom Besucheraufkommen ab: Weil die Zeilen kurz sind, kann das bei wenig Verkehr mehrere Monate dauern; spätestens ist ein Eintrag weg, wenn die Log-Rotation ihn überschreibt. Das Cookie `cf_clearance` bleibt bis zu etwa ein Jahr in deinem Browser (Abschnitt 10). Cloudflare nennt in seiner Datenschutzerklärung keine feste Frist für die Protokolle des Datenverkehrs; die Daten werden dort nur so lange gespeichert, wie es für die Dienste und gesetzliche Pflichten erforderlich ist, und danach gelöscht oder anonymisiert. Näheres siehe oben verlinkte Datenschutzerklärung von Cloudflare.

**Drittlandübermittlung:** Cloudflare verarbeitet Daten auch in den USA. Cloudflare Inc. ist nach eigenen Angaben unter dem EU-US Data Privacy Framework zertifiziert (Angemessenheitsbeschluss der EU-Kommission vom 10. Juli 2023) und verwendet ersatzweise die EU-Standardvertragsklauseln. Mehr dazu in Abschnitt 11.

## 4. Lokale Speicherung im Browser, Export und Import

Finplanr speichert deine Einstellungen im lokalen Speicher deines Browsers (Local Storage), damit sie bei deinem nächsten Besuch wieder da sind. Diese Daten verlassen deinen Browser nicht und werden nicht an uns übertragen.

Konkret werden folgende Einträge angelegt:

- `mein-sparplan-portfolio-v1`: dein Portfolio, also monatliches Sparbudget, Kategorien und Positionen, Gewichtungen und Beträge, Namen, Kürzel, ISIN, WKN, Farben, Symbole, Logos (auch selbst hochgeladene oder in deinen Browser kopierte Bilder, siehe Abschnitt 8), gesperrte Gewichtungen, Sortierreihenfolge und Anzeigeeinstellungen sowie, falls du sie in der optionalen Funktion „Mit meinem Bestand ausgleichen“ einträgst, die aktuellen Werte deiner Positionen, die Auswahl, welche Positionen dabei zählen, sowie ein optionaler einmaliger Zusatzbetrag und der gewählte Zeitraum (derselbe Eintrag, alles nur lokal, ohne Übertragung)
- `mein-sparplan-reset-stand-v1`: ein von dir gespeicherter persönlicher Reset-Stand
- `finplanr-consent`: ein einzelner Eintrag über deine Datenschutz-Entscheidungen (je Funktion eine Entscheidung, „Charts“ und „Online-Suche“, jeweils mit Zeitpunkt), siehe Abschnitt 5

Bei deinem ersten Besuch ist der lokale Speicher leer: Die Einträge entstehen erst, wenn du etwas an deinem Portfolio änderst (bzw. einen Reset-Stand speicherst oder eine Einwilligung erteilst). Finplanr speichert **keine** Spracheinstellung: Die Sprache ergibt sich aus der aufgerufenen Adresse (`finplanr.net/` ist Englisch, `finplanr.net/de/` ist Deutsch). Einträge früherer Versionen (`finplanr-lang` und `finplanr-consent-tv`) werden bei einem Besuch automatisch aus deinem Browser entfernt. Den Sitzungsspeicher (Session Storage) verwendet Finplanr nicht.

Finplanr selbst setzt keine eigenen Cookies (zu Cookies von Cloudflare siehe Abschnitt 10).

**Rechtsgrundlage:** Die Speicherung und der Zugriff auf die Portfolio-Einträge erfolgen nach § 25 Abs. 2 Nr. 2 TDDDG (Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz), weil sie unbedingt erforderlich sind, damit die von dir ausdrücklich gewünschte Funktion (Planung und Wiederherstellung deines Portfolios) funktioniert. Eine Einwilligung ist dafür nicht nötig. Soweit dabei personenbezogene Daten verarbeitet werden, ist die Rechtsgrundlage Art. 6 Abs. 1 lit. b DSGVO (Bereitstellung der von dir genutzten Funktion), hilfsweise Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse, die Anwendung nutzbar zu machen). Dasselbe gilt für den Eintrag `finplanr-consent`, der erforderlich ist, um deine Entscheidungen zu merken und nachweisen zu können (Art. 7 Abs. 1 DSGVO).

**Speicherdauer und Löschung:** Die Daten bleiben in deinem Browser, bis du sie löschst. Du kannst sie jederzeit selbst entfernen: Mit „Werkseinstellungen wiederherstellen“ (in den Einstellungen der App) ersetzt du dein Portfolio durch das eingebaute Beispiel und löschst den Reset-Stand; deine Datenschutz-Entscheidungen widerrufst du im Dialog „Datenschutz-Einstellungen“. Alle Einträge zusammen entfernst du durch Löschen der Website-Daten für finplanr.net in deinen Browsereinstellungen. Ein Wechsel des Browsers oder des Geräts überträgt die Daten nicht automatisch.

**Export und Import:** Finplanr kann dein Portfolio als JSON-Datei und den aktuellen Plan als CSV-Tabelle exportieren und eine JSON-Sicherung wieder importieren. Das Erstellen und Einlesen dieser Dateien geschieht vollständig in deinem Browser. Die Dateien werden auf deinem Gerät gespeichert bzw. von dort gelesen und nicht an uns oder Dritte übertragen. Für die Aufbewahrung dieser Dateien bist du selbst verantwortlich. Die Kopier-Schaltflächen (zum Beispiel für ISIN oder WKN) legen den Wert nur in die Zwischenablage deines Geräts; es wird nichts übertragen.

## 5. Datenschutz-Einstellungen und Einwilligung {#einwilligung}

Finplanr hat kein Cookie-Banner und keinen Einwilligungsdialog beim Seitenaufruf, weil Finplanr selbst keine eigenen Cookies setzt, beim Aufruf nichts von Dritten lädt und das einzige beim Aufruf gesetzte Cookie (von Cloudflare, Abschnitt 10) aus unserer Sicht technisch erforderlich ist. Stattdessen wird die Einwilligung **dort eingeholt, wo die Funktion genutzt wird**, getrennt für zwei Zwecke und **bevor eine Anfrage** an die Anbieter gesendet wird:

- **Charts** (TradingView.com, Inc., USA): Ein Hinweisfeld im Chart-Panel erklärt, was passiert, und fragt vor dem Laden des Chart-Widgets nach deiner Einwilligung.
- **Online-Suche** (CoinGecko = Gecko Labs Pte. Ltd., Singapur; Wikidata, der Wikidata-Abfragedienst und Wikimedia Commons = Wikimedia Foundation, Inc., USA): Ein Hinweisfeld im Suchdialog erklärt, was passiert, und fragt vor der ersten Online-Anfrage nach deiner Einwilligung. Die Suche im integrierten Katalog funktioniert ohne sie.

Du kannst die Einwilligungen außerdem jederzeit im Dialog **„Datenschutz-Einstellungen“** (Link in der Fußzeile der App) erteilen und widerrufen. Dort sind beide Zwecke aufgeführt; du kannst jeden einzeln erlauben oder widerrufen. Eine Änderung gilt sofort, auch in allen anderen geöffneten Tabs und Fenstern desselben Browsers: Eine widerrufene Funktion wird auch dort gestoppt (zum Beispiel wird ein geöffnetes Chart geschlossen), und vom Anbieter wird nichts mehr geladen, bis du erneut einwilligst.

**Rechtsgrundlagen:**

- Deine ausdrückliche Einwilligung ist die Grundlage für die Verarbeitung nach **Art. 6 Abs. 1 lit. a DSGVO**.
- Für die Übermittlung deiner Daten an die Anbieter in den USA und in Singapur stützen wir uns auf deine ausdrückliche Einwilligung nach **Art. 49 Abs. 1 lit. a DSGVO** (siehe „Risiken der Übermittlungen“ unten).
- Soweit das TradingView-Widget Informationen in deinem Browser speichert oder ausliest (Abschnitt 6), ist die Grundlage deine Einwilligung nach **§ 25 Abs. 1 TDDDG**.
- Die Speicherung deiner Entscheidung selbst (`finplanr-consent`, Abschnitt 4) ist für die von dir gewünschte Funktion technisch erforderlich (§ 25 Abs. 2 Nr. 2 TDDDG).

**Risiken der Übermittlungen (Art. 49 Abs. 1 lit. a DSGVO):** Für die oben genannten Anbieter hat die EU-Kommission entweder keinen Angemessenheitsbeschluss erlassen (Singapur) oder wir können keine Zertifizierung unter dem EU-US Data Privacy Framework angeben (TradingView, Wikimedia Foundation), und mit ihnen bestehen keine Standardvertragsklauseln. Das bedeutet: Das Datenschutzniveau dort kann niedriger sein als in der EU, Behörden in diesen Ländern können unter Umständen auf Daten zugreifen, ohne dass du durchsetzbare Rechte oder wirksame Rechtsbehelfe wie in der EU hast, und die Anbieter sind nicht an diese Datenschutzerklärung gebunden. Die Hinweisfelder und dieser Abschnitt informieren dich darüber, bevor du entscheidest. Die Einwilligung ist freiwillig: Ohne sie funktioniert die gesamte App weiterhin, nur ohne eingebettetes Chart und ohne Online-Suche.

**Widerruf:** Du kannst jede Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen, für jeden Zweck einzeln, im Dialog „Datenschutz-Einstellungen“. Daten, die ein Anbieter bereits erhalten oder in deinem Browser gespeichert hat, werden durch den Widerruf nicht gelöscht; Daten in deinem Browser (bei TradingView unter den Websitedaten für tradingview-widget.com) kannst du in den Browser-Einstellungen entfernen und beim Anbieter die Löschung verlangen. Die Rechtmäßigkeit der bis zum Widerruf erfolgten Verarbeitung bleibt unberührt (Art. 7 Abs. 3 DSGVO).

## 6. Kurscharts von TradingView

Wenn du in der App auf den Namen einer Position klickst, öffnet sich darunter ein Panel für ein Kurschart. Dafür binden wir den „Advanced Chart“-Widget von TradingView ein. Ohne deine Einwilligung (Abschnitt 5) wird nichts von TradingView geladen: Das Panel zeigt zuerst ein Hinweisfeld; erst nachdem du bestätigt hast (oder in den „Datenschutz-Einstellungen“ Charts erlaubt hast), wird das Widget geladen.

**Anbieter:** TradingView.com, Inc., 1330 Avenue of the Americas, 23rd Floor, New York, NY 10019, USA. TradingView hat nach eigener Aussage einen Vertreter in der EU nach Art. 27 DSGVO in Barcelona (Spanien) benannt. Datenschutzerklärung: https://www.tradingview.com/privacy-policy/

**Verarbeitete Daten:** Nach deiner Einwilligung baut dein Browser Verbindungen zu TradingView auf (bei unserem Test zu s3.tradingview.com, www.tradingview-widget.com, widget-sheriff.tradingview-widget.com, scanner-backend.tradingview.com, s3-symbol-logo.tradingview.com und www.tradingview.com; TradingView kann diese Server ändern). Dabei werden insbesondere übertragen:

- deine IP-Adresse und technische Verbindungsdaten (z. B. Browser und Betriebssystem),
- die Adresse der einbettenden Seite (bei uns finplanr.net bzw. finplanr.net/de/, ohne Parameter) und die gewählte Sprache,
- die Art des Widgets und das angezeigte Symbol. Das Symbol wird aus dem von dir eingetragenen Kürzel (Ticker) abgeleitet, zum Beispiel „XETR:VWCE“. Beträge, Gewichtungen oder dein übriges Portfolio werden nicht übertragen.

Nach den Angaben von TradingView setzt das Widget keine Cookies; bei unserem Test hat es auch keine gesetzt. Es legt aber Daten im lokalen Speicher deines Browsers unter der Domain tradingview-widget.com ab (ein von finplanr.net getrennter Speicherbereich; bei unserem Test Einstellungen des Charts). Außerdem weist TradingView in seiner Datenschutzerklärung darauf hin, dass über seine Widgets Analysedaten (zum Beispiel mit Google Analytics) erhoben werden können. Auf diese Verarbeitung haben wir keinen Einfluss. Die Widget-FAQ von TradingView: https://www.tradingview.com/widget-docs/faq/general/

**Zweck:** Anzeige eines Kurscharts zum von dir gewählten Wertpapier oder Coin.

**Rechtsgrundlage:** Deine Einwilligung, Art. 6 Abs. 1 lit. a DSGVO und § 25 Abs. 1 TDDDG (Speicherung von und Zugriff auf Informationen in deinem Endgerät durch das Widget). Widerruf jederzeit wie in Abschnitt 5 beschrieben.

**Speicherdauer:** Bei uns wird zu diesem Vorgang nichts gespeichert außer deinem Einwilligungseintrag. TradingView gibt an, dass die IP-Adresse beim Widget nicht mit identifizierbaren Daten gespeichert und nur kurzfristig vorgehalten wird. Daten im lokalen Speicher unter tradingview-widget.com bleiben, bis du sie in deinen Browsereinstellungen löschst. Weitere Angaben findest du in der Datenschutzerklärung von TradingView.

**Drittlandübermittlung:** Die Daten gehen an TradingView in die USA. Die Datenschutzerklärung von TradingView nennt keinen bestimmten Übermittlungsmechanismus. Wir stützen die Übermittlung deshalb auf deine ausdrückliche Einwilligung nach Information über die Risiken (Art. 49 Abs. 1 lit. a DSGVO; Risiken wie in Abschnitt 5 beschrieben): In den USA kann ein anderes Datenschutzniveau als in der EU bestehen, und US-Behörden können unter Umständen auf Daten zugreifen. Wenn du das nicht möchtest, willige nicht in Charts ein.

**Quellenangabe:** Unter dem Chart zeigt TradingView den Hinweis „Track all markets on TradingView“. Er gehört zum Widget und wird unverändert angezeigt.

## 7. Optionale Online-Suche (CoinGecko, Wikidata, Wikimedia Commons)

Im Bearbeitungsmodus kannst du für eine Position eine Suche nutzen, um Aktien, ETFs und Kryptowährungen, Kennungen (ISIN, WKN, Kürzel) und passende Bilder zu finden. Im Suchdialog wählst du die Quelle („Aktien & ETFs“ oder „Krypto“); voreingestellt ist sie nach dem Typ der Kategorie, du kannst sie jederzeit umschalten. Die Suche im **integrierten Katalog** findet lokal in deinem Browser statt und braucht keine Einwilligung. Die **Online-Suche** läuft erst nach deiner ausdrücklichen Einwilligung (Abschnitt 5): Der Dialog zeigt zuerst ein Hinweisfeld, und an keinen Anbieter wird eine Anfrage gesendet, bevor du bestätigt hast (oder die Online-Suche in den „Datenschutz-Einstellungen“ erlaubt hast). Das Hinweisfeld nennt die Anbieter und verlinkt auf diese Datenschutzerklärung.

**Logo-Angebot nach dem Hinzufügen einer Position:** Übernimmst du einen Treffer, der ohne Logo kommt (nicht bei Sparkonten), bietet der Dialog in einem kurzen zweiten Schritt eine Logo-Suche an. Diese Logo-Suche ist eine Bildersuche bei Wikimedia Commons und von derselben Einwilligung gedeckt wie die übrige Online-Suche: Hast du sie noch nicht erlaubt, zeigt der zweite Schritt nur das Hinweisfeld mit der Wahl „Online-Suche erlauben“ oder „Überspringen“, und es wird nichts angefragt, bevor du bestätigt hast. Als Suchbegriff dient dann der Name der Position ohne Rechtsformzusätze plus das Wort „logo“ (zum Beispiel „Apple logo“); du kannst ihn vor dem Suchen ändern. Mit „Überspringen“, Esc oder dem Schließen des Dialogs bleibt die Position ohne Logo. Du kannst das Angebot dauerhaft ausschalten: mit dem Kästchen „Beim Hinzufügen keine Logo-Suche anbieten“ in diesem Schritt oder in den Einstellungen („Beim Hinzufügen einer Position eine Logo-Suche anbieten“); die Einstellung wird zusammen mit deinem Plan in deinem Browser gespeichert (Abschnitt 4).

Nach deiner Einwilligung können folgende Dienste abgefragt werden:

- **CoinGecko** (api.coingecko.com), Suche nach Kryptowährungen. Anbieter: Gecko Labs Pte. Ltd., Singapur (EU-Vertreter nach Art. 27 DSGVO: Euverify Ltd, Cork, Irland). Datenschutz: https://www.coingecko.com/en/privacy
- **Wikidata** (www.wikidata.org und der zugehörige Abfragedienst query.wikidata.org), Suche nach Wertpapier- und Unternehmensdaten (Quelle „Aktien & ETFs“; der Abfragedienst erhält nur Kennungen der gefundenen Wikidata-Einträge, nicht deinen Suchbegriff), sowie **Wikimedia Commons** (commons.wikimedia.org), Bildersuche. Anbieter dieser Dienste: Wikimedia Foundation, Inc., USA. Datenschutz: https://foundation.wikimedia.org/wiki/Policy:Privacy_policy

**Verarbeitete Daten:** Dein Browser sendet deinen Suchbegriff und die dabei technisch notwendigen Daten direkt an den jeweiligen Anbieter: deine IP-Adresse, Browser- und Betriebssystemangaben und als Herkunft der Anfrage die Adresse „https://finplanr.net“ (einen Referrer sendet Finplanr bei diesen Anfragen nicht). Unser Server sieht und speichert deinen Suchbegriff nicht. Die Trefferlisten können Vorschaubilder enthalten (zum Beispiel Coin-Logos von coin-images.coingecko.com oder Bilder von thumb.wikimedia.org bzw. upload.wikimedia.org), die dein Browser ebenfalls direkt von dort lädt.

**Cookies:** Finplanr lädt diese Vorschaubilder in einem Modus, in dem dein Browser keine Cookies an die Bildserver sendet und keine von ihnen annimmt (das HTML-Attribut `crossorigin="anonymous"`, das den Browser das Bild ohne Anmeldeinformationen abrufen lässt). Dasselbe gilt für die Suchanfragen selbst und für die Kopie eines gewählten Bildes (Abschnitt 8). Wir haben die Wirkung gemessen: Werden die Vorschaubilder auf die übliche Weise geladen, setzen die Bildserver von Wikimedia (thumb.wikimedia.org, upload.wikimedia.org) die Cookies `WMF-Uniq` (bis zu etwa ein Jahr gültig) und `NetworkProbeLimit` (etwa eine Stunde). Mit dem Modus, den Finplanr verwendet, wurde bei unserem Test (Suche, Vorschaubilder, Auswahl eines Bildes) kein Cookie von CoinGecko, Wikidata oder Wikimedia im Browser gespeichert; die Server senden zwar weiterhin Cookie-Header, der Browser verwirft sie aber. Das kann sich ändern, wenn ein Anbieter seine Server umstellt; wir prüfen es von Zeit zu Zeit erneut. Die einzige Ausnahme ist ein Bild, das du selbst per Hotlink einbindest (Abschnitt 8).

**Zweck:** Ausführung der von dir angeforderten Suchfunktion und Anzeige der Treffer.

**Rechtsgrundlage:** Deine ausdrückliche Einwilligung, Art. 6 Abs. 1 lit. a DSGVO. Weil diese Anbieter keine Informationen auf deinem Gerät speichern oder aus ihm auslesen (siehe „Cookies“ oben), ist § 25 TDDDG auf die Suche nicht anwendbar. Du kannst die Einwilligung jederzeit wie in Abschnitt 5 beschrieben widerrufen.

**Speicherdauer:** Bei uns werden die Suchanfragen nicht gespeichert. Die Anbieter speichern Verbindungsdaten nach ihren eigenen Regeln, zum Beispiel gibt die Wikimedia Foundation an, dass die meisten personenbezogenen Daten nach 90 Tagen gelöscht, aggregiert oder anonymisiert werden. CoinGecko speichert Daten so lange, wie es für seine Zwecke und gesetzliche Pflichten erforderlich ist.

**Drittlandübermittlung:** CoinGecko sitzt in Singapur, die Wikimedia Foundation in den USA. Für Singapur gibt es keinen Angemessenheitsbeschluss der EU-Kommission. Die Wikimedia Foundation nennt in ihrer Datenschutzerklärung keine Zertifizierung unter dem EU-US Data Privacy Framework, und mit keinem der beiden Anbieter bestehen Standardvertragsklauseln. Wir stützen die Übermittlung deshalb ausschließlich auf deine ausdrückliche Einwilligung nach Information über die Risiken (**Art. 49 Abs. 1 lit. a DSGVO**; die Risiken sind in Abschnitt 5 und im Hinweisfeld beschrieben). Wenn du das nicht möchtest, willige nicht in die Online-Suche ein.

**Folgen:** Wenn du nicht einwilligst, entstehen diese Verbindungen nicht. Die App lässt sich vollständig auch ohne Online-Suche bedienen (du kannst den integrierten Katalog nutzen oder Kennungen und Namen von Hand eintragen).

## 8. Logos und externe Bilder

Die Logos der Standardwerte (6 Kryptowährungen und 11 Fondsanbieter) sowie die Symbole der App werden von unserem eigenen Server ausgeliefert. Beim normalen Aufruf von Finplanr werden **keine** Logos von Drittanbietern geladen. Eine Position ohne Logo erhält ein kleines **Buchstaben-Symbol** (Kürzel oder Initialen auf farbigem Grund), das dein Browser selbst aus dem Namen der Position zeichnet: Es nutzt kein Bild und löst keine Anfrage aus.

Eine Verbindung zu einem Drittanbieter entsteht nur, wenn du selbst eine externe Bildquelle auswählst:

- eine **Bildadresse (URL)**, die du eingibst (der Anbieter ist dann der Betreiber des Servers hinter dieser Adresse),
- ein **Bild aus Wikimedia Commons**, das du in der Bildauswahl wählst (thumb.wikimedia.org bzw. upload.wikimedia.org, Wikimedia Foundation, Inc., USA),
- das **Logo, das CoinGecko** für eine über die Suche hinzugefügte Kryptowährung liefert (coin-images.coingecko.com, Gecko Labs Pte. Ltd., Singapur).

Bilder aus Wikimedia Commons und von CoinGecko stammen aus der Online-Suche und sind von deiner Einwilligung dazu (Abschnitt 5) gedeckt. Das gilt auch für die Logo-Suche, die nach dem Hinzufügen einer Position angeboten wird (Abschnitt 7): Sie läuft erst nach dieser Einwilligung, und du kannst das Angebot in den Einstellungen ausschalten.

**Was mit dem gewählten Bild passiert:** Wenn du ein externes Bild auswählst, versucht Finplanr, es **in die lokalen Daten deines Browsers zu kopieren** (als Data-URL mit höchstens 150 KB). Ist das gelungen, wird das Bild aus deinem eigenen Browser angezeigt, und dein Browser sendet bei späteren Besuchen **keine weiteren Anfragen** an den Bildserver. Nur der einmalige Abruf beim Auswählen kontaktiert den Anbieter (deine IP-Adresse, Browser-Angaben und als Herkunft der Anfrage „https://finplanr.net“; einen Referrer und Cookies sendet Finplanr bei diesem Abruf nicht und nimmt auch keine an).

**Wenn das Kopieren scheitert** (zum Beispiel weil das Bild größer als 150 KB ist oder der Server die Kopie nicht zulässt), wird stattdessen die Adresse gespeichert, und dein Browser lädt das Bild **bei jedem späteren Besuch** erneut vom ursprünglichen Server („Hotlinking“). Der Anbieter erhält dann schon beim Auswählen zwei oder drei Abrufe (den fehlgeschlagenen Kopierversuch und die Anzeige) und sieht später jedes Mal deine IP-Adresse und deine Browser-Angaben. Finplanr fordert das Bild zunächst ohne Cookies und ohne Referrer an und nennt „https://finplanr.net“ als Herkunft der Anfrage; der Anbieter kann daraus ablesen, dass du Finplanr nutzt. Lässt der Server diese Art der Anfrage nicht zu (deshalb scheitert das Kopieren oft), wiederholt die App die Anfrage einmal als einfache Bildanfrage, weiterhin ohne Referrer; dann kann der Server eigene Cookies setzen oder auslesen, was Finplanr nicht verhindern kann. Das ist deine eigene Entscheidung durch die Wahl dieses Bildes; die App weist dich mit einem Hinweis darauf hin, wenn das Kopieren nicht möglich war. Das gilt für jede Seite, die du dort hinterlegst.

**So vermeidest du das:** Nutze Symbole oder ein selbst hochgeladenes Bild (wird als Daten in deinem Browser gespeichert und nirgendwohin übertragen) oder die mitgelieferten Logos. Ein bereits gesetztes externes Logo entfernst du im Bearbeitungsmodus über „Standardlogo verwenden“.

**Rechtsgrundlage:** Für Bilder aus Commons und von CoinGecko: deine Einwilligung, Art. 6 Abs. 1 lit. a und Art. 49 Abs. 1 lit. a DSGVO (Abschnitte 5 und 7). Für eine von dir selbst eingegebene Bildadresse: Art. 6 Abs. 1 lit. b DSGVO (die von dir gewählte Darstellung deines Portfolios), hilfsweise Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse, dir die gewünschte Anpassung zu ermöglichen; die Auswahl nimmst du selbst vor). Setzt oder liest der Server eines von dir selbst per Hotlink eingebundenen Bildes eigene Cookies, geschieht das auf deine eigene Veranlassung (§ 25 Abs. 2 Nr. 2 TDDDG, weil die Anzeige des von dir gewählten Bildes die Anfrage erfordert) und in der Verantwortung dieses Anbieters.

**Speicherdauer und Drittlandübermittlung:** Bei den Anbietern gelten deren eigene Regeln (Abschnitt 7 bzw. deren Datenschutzerklärungen). Bei frei eingegebenen Adressen entscheidest du selbst, welchen Server du kontaktierst; dessen Standort kennen wir nicht.

## 9. Kontaktaufnahme per E-Mail

Wenn du uns per E-Mail an {{EMAIL}} schreibst, verarbeiten wir die von dir übermittelten Daten: deine E-Mail-Adresse, deinen Namen (soweit angegeben), den Inhalt deiner Nachricht und technische Angaben zur Zustellung.

**Technischer Ablauf:** Die Adresse {{EMAIL}} ist eine Weiterleitung über Cloudflare Email Routing (Cloudflare, Inc., USA, als Auftragsverarbeiter). Cloudflare leitet die Nachricht an das private Postfach des Betreibers weiter. Anbieter dieses Postfachs ist: {{MAILBOX_PROVIDER}}. Antworten werden aus demselben Postfach versendet.

Das im Impressum verlinkte Kontaktformular wird vom Anbieter der Impressum-Seite ({{IMPRESSUM_PROVIDER}}) betrieben und leitet deine Nachricht an uns weiter. Dessen Datenverarbeitung richtet sich nach den Datenschutzhinweisen auf der dortigen Seite.

**Zweck und Rechtsgrundlage:** Bearbeitung und Beantwortung deiner Anfrage. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der Beantwortung von Anfragen), bzw. Art. 6 Abs. 1 lit. b DSGVO, wenn sich deine Anfrage auf eine Leistung von uns bezieht.

**Speicherdauer:** So lange, wie es zur Bearbeitung deines Anliegens erforderlich ist. Danach löschen wir die Korrespondenz, sofern keine gesetzlichen Aufbewahrungspflichten eine längere Speicherung verlangen.

**Pflicht zur Bereitstellung:** Du bist nicht verpflichtet, uns zu schreiben. Ohne deine E-Mail-Adresse können wir dir aber nicht antworten.

**Drittlandübermittlung:** siehe Abschnitt 11 (Cloudflare und Postfachanbieter).

## 10. Cookies und vergleichbare Technologien

Finplanr selbst setzt keine eigenen Cookies. Es gibt keine Werbe-, Marketing- oder Analysecookies und keine Analysedienste. Deshalb gibt es kein globales Cookie-Banner: Die Einwilligung wird nur dort eingeholt, wo du die zwei in Abschnitt 5 beschriebenen Funktionen nutzt.

**Cookie von Cloudflare:** Beim Aufruf unserer Seiten setzt Cloudflare derzeit das Cookie `cf_clearance` (Cookie der Bot-Erkennung, siehe Abschnitt 3). Es ist ein sogenanntes HttpOnly-Cookie, wird nur über HTTPS übertragen, merkt sich, dass die Prüfung bestanden wurde, und ist bei unserem Test bis zu etwa ein Jahr gültig. Je nach den bei Cloudflare aktivierten Schutzfunktionen können weitere technisch erforderliche Cookies hinzukommen (zum Beispiel `__cf_bm`). Wir halten diese Cookies für den gesicherten Betrieb des Dienstes technisch erforderlich (§ 25 Abs. 2 Nr. 2 TDDDG). Du kannst sie in den Einstellungen deines Browsers jederzeit löschen oder blockieren; die App funktioniert dann weiter, die Bot-Prüfung wird dann bei einem späteren Aufruf neu durchgeführt. Näheres: https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/

Zur Speicherung deiner Einstellungen und deiner Datenschutz-Entscheidungen wird der lokale Speicher deines Browsers verwendet (Abschnitt 4). Das TradingView-Widget legt nach deiner Einwilligung Daten im lokalen Speicher unter tradingview-widget.com ab (Abschnitt 6); die Bilder der Online-Suche werden so geladen, dass keine Cookies von CoinGecko oder Wikimedia in deinem Browser gespeichert werden (Abschnitt 7). Die einzige mögliche Ausnahme ist ein Bild, das du selbst per Hotlink einbindest (Abschnitt 8).

**Google AdSense, Google Analytics und andere Werbe- oder Analysedienste sind nicht eingebunden.** Falls künftig Werbung oder zusätzliche Dienste hinzukommen, wird diese Datenschutzerklärung vor der Aktivierung aktualisiert und, soweit erforderlich, vorab deine Einwilligung eingeholt.

## 11. Empfänger und Datenübermittlungen in Drittländer

Empfänger personenbezogener Daten sind je nach deiner Nutzung:

- **Cloudflare, Inc.** (USA, mit Unternehmen in der EU): DNS, Weiterleitung (Tunnel), Zwischenspeicherung, Sicherheit und Bot-Erkennung, E-Mail-Weiterleitung (Auftragsverarbeiter, Abschnitte 3 und 9)
- **TradingView.com, Inc.** (USA): nur nach deiner Einwilligung, Abschnitt 6
- **Gecko Labs Pte. Ltd. / CoinGecko** (Singapur): nur nach deiner Einwilligung in die Online-Suche (Krypto-Suche, CoinGecko-Logos), Abschnitte 7 und 8
- **Wikimedia Foundation, Inc.** (USA): nur nach deiner Einwilligung in die Online-Suche (Wikidata und Abfragedienst, Wikimedia-Commons-Suche und -Bilder), Abschnitte 7 und 8
- {{MAILBOX_RECIPIENT}}
- der Anbieter der Impressum-Seite ({{IMPRESSUM_PROVIDER}}): bei Formularkontakt über deren Seite
- von dir eingegebene **Bildserver**: wenn du eine externe Bildadresse einträgst, Abschnitt 8

Weitere Empfänger gibt es nicht. Eine Weitergabe zu Werbezwecken findet nicht statt.

**Drittlandübermittlungen und Garantien (Art. 13 Abs. 1 lit. f DSGVO):**

- **Cloudflare, Inc. (USA):** Cloudflare erklärt, unter dem EU-US Data Privacy Framework (DPF) zertifiziert zu sein. Für Übermittlungen an zertifizierte US-Unternehmen hat die EU-Kommission mit Beschluss vom 10. Juli 2023 ein angemessenes Datenschutzniveau festgestellt (Art. 45 DSGVO). Fällt die Zertifizierung weg, greifen nach Cloudflares Angaben die EU-Standardvertragsklauseln (Art. 46 Abs. 2 lit. c DSGVO), die Teil des Auftragsverarbeitungsvertrags sind. Informationen: https://www.cloudflare.com/trust-hub/gdpr/
- **TradingView (USA):** Die Datenschutzerklärung nennt keinen Übermittlungsmechanismus, und wir können keine Zertifizierung angeben; ein Angemessenheitsbeschluss oder andere Garantien sind nicht angegeben. Grundlage ist deine ausdrückliche Einwilligung nach Information über die Risiken, Art. 49 Abs. 1 lit. a DSGVO (Abschnitte 5 und 6).
- **CoinGecko (Singapur):** kein Angemessenheitsbeschluss und keine Garantien angegeben; Grundlage ist deine ausdrückliche Einwilligung nach Information über die Risiken, Art. 49 Abs. 1 lit. a DSGVO (Abschnitte 5 und 7). CoinGecko hat zudem einen EU-Vertreter benannt.
- **Wikimedia Foundation (USA):** keine DPF-Zertifizierung bekannt bzw. angegeben und keine anderen Garantien; Grundlage ist deine ausdrückliche Einwilligung nach Information über die Risiken, Art. 49 Abs. 1 lit. a DSGVO (Abschnitte 5 und 7).
- {{MAILBOX_TRANSFER}}

Eine Kopie der genannten Garantien (z. B. der Standardvertragsklauseln) kannst du über die oben verlinkten Seiten der Anbieter einsehen; bei Fragen schreibe an die in Abschnitt 1 genannte Adresse. Die Standardvertragsklauseln der EU-Kommission findest du unter https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj

## 12. Speicherdauer im Überblick

- **Zugriffsprotokoll auf unserem Server:** nur Zeit, Methode, Pfad, Status und Größe, keine IP-Adresse; durch automatische Log-Rotation begrenzt (3 Dateien à 10 MB); je nach Besucheraufkommen bis zu mehreren Monaten, spätestens bis zum Überschreiben. Dasselbe Rotationsverfahren gilt für das Fehlerprotokoll des Webservers und das Protokoll des Tunnel-Connectors.
- **Cloudflare-Cookie `cf_clearance`:** in deinem Browser bis zu etwa ein Jahr, du kannst es jederzeit löschen.
- **Protokolle bei Cloudflare:** keine feste Frist veröffentlicht; nur so lange wie nötig, danach gelöscht oder anonymisiert (siehe deren Datenschutzerklärung).
- **Portfolio, Reset-Stand:** in deinem Browser, bis du sie löschst. Sie liegen nicht auf unserem Server.
- **Datenschutz-Entscheidungen (`finplanr-consent`):** in deinem Browser, bis du beide Einwilligungen widerrufst oder die Website-Daten löschst.
- **Online-Suche, Charts und externe Bilder:** bei uns keine Speicherung. Bei den Anbietern nach deren Regeln (Wikimedia: in der Regel 90 Tage; TradingView: IP kurzfristig; CoinGecko: nach Erforderlichkeit). Cookies dieser Anbieter werden in deinem Browser nicht gespeichert (Abschnitte 7 und 10).
- **E-Mails:** bis zur Erledigung deines Anliegens, danach Löschung, soweit keine gesetzliche Aufbewahrungspflicht besteht.

## 13. Pflicht zur Bereitstellung von Daten

Die Nutzung von Finplanr ist ohne die Angabe personenbezogener Daten möglich. Eine gesetzliche oder vertragliche Pflicht zur Bereitstellung besteht nicht.

Bei jedem Seitenaufruf werden technisch bedingt Verbindungsdaten wie deine IP-Adresse übertragen, sonst kann die Seite nicht ausgeliefert werden. Für Chart, Online-Suche und externe Logos gilt: Wenn du die jeweilige Funktion nicht nutzt oder deine Einwilligung nicht erteilst, entstehen keine Verbindungen zu den Drittanbietern. Die Folge ist lediglich, dass das Chart oder die Ergebnisse der Online-Suche nicht angezeigt werden. Wenn du uns schreibst, brauchen wir deine E-Mail-Adresse für die Antwort.

## 14. Externe Links

Finplanr enthält Links auf externe Seiten, zum Beispiel zu Produktseiten von Fondsanbietern, zur Deutschen Börse, zu CoinGecko, TradingView und den Dateiseiten von Wikimedia Commons sowie zum Impressum bei {{IMPRESSUM_PROVIDER}}. Sie öffnen sich nur, wenn du sie anklickst, in einem neuen Tab. Beim Aufruf verlässt du Finplanr; der Anbieter der Zielseite erhält dann deine IP-Adresse und Browserangaben (Finplanr sendet dabei keinen Referrer mit; ausgenommen ist der Quellenhinweis „Track all markets on TradingView“ unter dem Chart, der Teil des TradingView-Widgets ist und „finplanr.net“ als Herkunft angeben kann). Für die dortige Verarbeitung personenbezogener Daten ist der jeweilige Anbieter nach seinen eigenen Datenschutzinformationen verantwortlich.

## 15. Deine Rechte

Dir stehen nach der DSGVO folgende Rechte zu, soweit die jeweiligen Voraussetzungen vorliegen:

- Auskunft über die Verarbeitung deiner personenbezogenen Daten (Art. 15 DSGVO)
- Berichtigung unrichtiger Daten (Art. 16 DSGVO)
- Löschung (Art. 17 DSGVO)
- Einschränkung der Verarbeitung (Art. 18 DSGVO)
- Datenübertragbarkeit (Art. 20 DSGVO)
- **Widerspruch** gegen Verarbeitungen, die auf Art. 6 Abs. 1 lit. f DSGVO beruhen, aus Gründen, die sich aus deiner besonderen Situation ergeben (Art. 21 DSGVO)
- **Widerruf** einer erteilten Einwilligung jederzeit mit Wirkung für die Zukunft (Art. 7 Abs. 3 DSGVO). Jede Einwilligung (Charts, Online-Suche) widerrufst du einzeln über „Datenschutz-Einstellungen“ in der Fußzeile der App; der Widerruf wirkt sofort in allen geöffneten Tabs desselben Browsers.

Zur Ausübung deiner Rechte schreibe an die in Abschnitt 1 genannte Adresse. Beachte, dass wir keine Portfolios von dir speichern; dein Portfolio kannst du selbst im Browser einsehen, exportieren und löschen (Abschnitt 4). Anbieter, die nach deiner Einwilligung Daten erhalten haben (Abschnitt 11), sind für ihre eigene Verarbeitung verantwortlich; für Auskunft oder Löschung dort wende dich bitte an sie.

**Beschwerderecht:** Du hast das Recht, dich bei einer Datenschutzaufsichtsbehörde zu beschweren (Art. 77 DSGVO), insbesondere in dem Mitgliedstaat deines gewöhnlichen Aufenthalts, deines Arbeitsplatzes oder des Orts des mutmaßlichen Verstoßes. Zuständig ist in der Regel die Aufsichtsbehörde an deinem Wohnort oder an dem Ort, an dem der Verantwortliche seinen Sitz hat; die Aufsichtsbehörden der Mitgliedstaaten findest du unter https://www.edpb.europa.eu/about-edpb/about-edpb/members_de.

## 16. Keine automatisierten Entscheidungen

Finplanr berechnet Sparbeträge und Gewichtungen anhand der von dir gewählten Eingaben, direkt in deinem Browser. Eine automatisierte Entscheidungsfindung einschließlich Profiling im Sinne von Art. 22 DSGVO findet nicht statt.

## 17. Änderungen dieser Datenschutzerklärung

Wir passen diese Datenschutzerklärung an, wenn sich die Funktionen von Finplanr, die eingesetzten Dienstleister oder die rechtlichen Anforderungen ändern. Die jeweils aktuelle Fassung findest du unter https://finplanr.net/datenschutz.html (Stand siehe oben). Sie ist auch über den Link „Datenschutz“ in der Fußzeile der App erreichbar.
