# Datenschutzerklärung für Finplanr

**Stand: 14. Oktober 2026**

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
- wenn du ein Kurschart von TradingView lädst (Abschnitt 6, nur mit deiner Einwilligung),
- wenn du die optionale Online-Suche verwendest (Abschnitt 7),
- wenn du ein Logo oder Bild von einem externen Anbieter auswählst (Abschnitt 8),
- wenn du uns per E-Mail kontaktierst (Abschnitt 9).

Bei einem normalen Seitenaufruf ohne diese Aktionen werden keine Daten an andere Drittanbieter als Cloudflare (Abschnitt 3) übermittelt. Schriftarten, Skripte und Logos der Standardwerte werden von unserem eigenen Server geliefert.

## 3. Bereitstellung der Website, Hosting, Cloudflare und Server-Logs

Die Website wird auf einem privat betriebenen Server des Betreibers mit einem Nginx-Webserver in einem Docker-Container bereitgestellt. Der Server ist nicht direkt aus dem Internet erreichbar, sondern ausschließlich über einen Cloudflare Tunnel.

Für DNS, die verschlüsselte HTTPS-Verbindung, die Weiterleitung der Anfragen an unseren Server (Cloudflare Tunnel) und technische Sicherheitsfunktionen setzen wir Cloudflare ein. Deine Anfragen laufen deshalb über die Server von Cloudflare. Cloudflare entschlüsselt die Verbindung dabei technisch, um sie an unseren Server weiterzuleiten.

**Anbieter:** Cloudflare, Inc., 101 Townsend St., San Francisco, CA 94107, USA, sowie verbundene Unternehmen (u. a. in der EU).

**Verarbeitete Daten:** Bei jedem Aufruf werden insbesondere verarbeitet:

- IP-Adresse
- Datum und Uhrzeit des Zugriffs
- aufgerufene Seite bzw. angeforderte Datei und HTTP-Statuscode
- übertragene Datenmenge
- Referrer (Seite, von der du kommst), soweit dein Browser ihn sendet
- Browsertyp, Browserversion und Betriebssystem (User-Agent)
- technische Verbindungs- und Sicherheitsdaten zur Erkennung und Abwehr missbräuchlicher Zugriffe

**Server-Logs auf unserem Server:** Der Webserver schreibt ein Zugriffsprotokoll mit den oben genannten Daten. Nach der aktuellen Konfiguration wird die IP-Adresse des Besuchers von Cloudflare in einer Kopfzeile (X-Forwarded-For) an unseren Server weitergegeben und kann deshalb im Zugriffsprotokoll erscheinen. Wir werten die Protokolle nicht systematisch aus, führen sie nicht mit anderen Daten zusammen und erstellen keine Nutzerprofile. Sie werden nur zur Fehlersuche und zur Aufklärung von Angriffen herangezogen.

**Zweck und Rechtsgrundlage:** Die Verarbeitung dient dazu, die Website sicher, stabil und funktionsfähig bereitzustellen und Angriffe abzuwehren. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse am sicheren und zuverlässigen Betrieb der Website).

**Rolle von Cloudflare:** Soweit Cloudflare Daten in unserem Auftrag verarbeitet (insbesondere die Protokolle des Datenverkehrs), handelt es als Auftragsverarbeiter nach Art. 28 DSGVO. Dazu besteht ein Auftragsverarbeitungsvertrag (Data Processing Addendum, DPA) mit Cloudflare, der nach Angaben von Cloudflare die EU-Standardvertragsklauseln einbezieht. Für einzelne Daten ist Cloudflare nach eigener Aussage selbst Verantwortlicher; Einzelheiten stehen in der Datenschutzerklärung von Cloudflare: https://www.cloudflare.com/privacypolicy/

**Speicherdauer:** Die Protokolle auf unserem Server werden von Docker automatisch nach Größe rotiert (höchstens drei Dateien von je 10 MB); ältere Einträge werden überschrieben. Je nach Besucherzahl sind die Protokolle in der Regel wenige Tage bis Wochen vorhanden, spätestens bis zum Überschreiben durch die Log-Rotation. Cloudflare nennt in seiner Datenschutzerklärung keine feste Frist für die Protokolle des Datenverkehrs; die Daten werden dort nur so lange gespeichert, wie es für die Dienste und gesetzliche Pflichten erforderlich ist, und danach gelöscht oder anonymisiert. Näheres siehe oben verlinkte Datenschutzerklärung von Cloudflare.

**Drittlandübermittlung:** Cloudflare verarbeitet Daten auch in den USA. Cloudflare Inc. ist nach eigenen Angaben unter dem EU-US Data Privacy Framework zertifiziert (Angemessenheitsbeschluss der EU-Kommission vom 10. Juli 2023) und verwendet ersatzweise die EU-Standardvertragsklauseln. Mehr dazu in Abschnitt 11.

## 4. Lokale Speicherung im Browser, Export und Import

Finplanr speichert deine Einstellungen im lokalen Speicher deines Browsers (Local Storage), damit sie bei deinem nächsten Besuch wieder da sind. Diese Daten verlassen deinen Browser nicht und werden nicht an uns übertragen.

Konkret werden folgende Einträge angelegt:

- `mein-sparplan-portfolio-v1`: dein Portfolio, also monatliches Sparbudget, Kategorien und Positionen, Gewichtungen und Beträge, Namen, Kürzel, ISIN, WKN, Farben, Symbole, Logos (auch selbst hochgeladene Bilder), gesperrte Gewichtungen, Sortierreihenfolge und Anzeigeeinstellungen
- `mein-sparplan-reset-stand-v1`: ein von dir gespeicherter persönlicher Reset-Stand
- `finplanr-lang`: deine Spracheinstellung (Deutsch oder Englisch)
- `finplanr-consent-tv`: ein Eintrag über deine Einwilligung zum TradingView-Chart mit Zeitpunkt (Abschnitt 5)

Finplanr setzt selbst keine Cookies.

**Rechtsgrundlage:** Die Speicherung und der Zugriff erfolgen nach § 25 Abs. 2 Nr. 2 TDDDG (Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz), weil sie unbedingt erforderlich sind, damit die von dir ausdrücklich gewünschte Funktion (Planung und Wiederherstellung deines Portfolios) funktioniert. Eine Einwilligung ist dafür nicht nötig. Soweit dabei personenbezogene Daten verarbeitet werden, ist die Rechtsgrundlage Art. 6 Abs. 1 lit. b DSGVO (Bereitstellung der von dir genutzten Funktion), hilfsweise Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse, die Anwendung nutzbar zu machen).

**Speicherdauer und Löschung:** Die Daten bleiben in deinem Browser, bis du sie löschst. Du kannst sie jederzeit selbst entfernen: über die Rücksetzfunktionen der App (zum Beispiel „Werkseinstellungen“) oder durch Löschen der Website-Daten für finplanr.net in deinen Browsereinstellungen. Ein Wechsel des Browsers oder des Geräts überträgt die Daten nicht automatisch.

**Export und Import:** Finplanr kann dein Portfolio als JSON-Datei und den aktuellen Plan als CSV-Tabelle exportieren und eine JSON-Sicherung wieder importieren. Das Erstellen und Einlesen dieser Dateien geschieht vollständig in deinem Browser. Die Dateien werden auf deinem Gerät gespeichert bzw. von dort gelesen und nicht an uns oder Dritte übertragen. Für die Aufbewahrung dieser Dateien bist du selbst verantwortlich.

## 5. Datenschutz-Einstellungen und Einwilligung {#einwilligung}

Es gibt in Finplanr nur eine Funktion, für die wir deine Einwilligung einholen: das Laden des TradingView-Charts (Abschnitt 6). Es gibt kein Einwilligungsbanner beim Seitenaufruf, weil beim Aufruf nichts geladen wird, was eine Einwilligung erfordert.

- Das Chart-Panel zeigt dir zuerst einen Hinweis, welche Daten an TradingView übertragen werden und dass TradingView seinen Sitz in den USA hat. Erst wenn du auf **„Chart laden“** klickst (oder in den „Datenschutz-Einstellungen“ „Charts erlauben“ wählst), wird das Widget von TradingView geladen. Das ist deine ausdrückliche Einwilligung (Art. 6 Abs. 1 lit. a DSGVO, § 25 Abs. 1 TDDDG, für die Übermittlung in die USA zusätzlich Art. 49 Abs. 1 lit. a DSGVO).
- Deine Entscheidung wird als Eintrag `finplanr-consent-tv` (mit Zeitpunkt der Einwilligung) im lokalen Speicher deines Browsers vermerkt, damit du nicht bei jedem Chart erneut gefragt wirst. Dieser Eintrag ist technisch erforderlich, um deine Wahl zu merken (§ 25 Abs. 2 Nr. 2 TDDDG).
- **Widerruf:** Du kannst die Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen, über den Link **„Datenschutz-Einstellungen“** in der Fußzeile der App (Schaltfläche „Einwilligung widerrufen“). Danach werden geöffnete Charts geschlossen und TradingView wird nicht mehr geladen, bis du erneut einwilligst. Von TradingView in deinem Browser bereits gespeicherte Daten werden dadurch nicht gelöscht; du kannst sie in den Browser-Einstellungen unter den Websitedaten für tradingview-widget.com entfernen. Die Rechtmäßigkeit der bis zum Widerruf erfolgten Verarbeitung bleibt unberührt (Art. 7 Abs. 3 DSGVO).
- Die Einwilligung ist freiwillig. Ohne sie funktioniert die gesamte App weiterhin, nur ohne eingebettetes Chart.

## 6. Kurscharts von TradingView

Wenn du in der App auf den Namen einer Position klickst, öffnet sich darunter ein Panel für ein Kurschart. Dafür binden wir den „Advanced Chart“-Widget von TradingView ein. Ohne deine Einwilligung (Abschnitt 5) wird nichts von TradingView geladen.

**Anbieter:** TradingView.com, Inc., 1330 Avenue of the Americas, 23rd Floor, New York, NY 10019, USA. TradingView hat nach eigener Aussage einen Vertreter in der EU nach Art. 27 DSGVO in Barcelona (Spanien) benannt. Datenschutzerklärung: https://www.tradingview.com/privacy-policy/

**Verarbeitete Daten:** Nachdem du auf „Chart laden“ geklickt hast, baut dein Browser eine Verbindung zu TradingView auf (u. a. zu s3.tradingview.com und weiteren TradingView-Servern). Dabei werden insbesondere übertragen:

- deine IP-Adresse und technische Verbindungsdaten (z. B. Browser und Betriebssystem),
- die Adresse der einbettenden Seite (bei uns die Adresse von finplanr.net),
- die Art des Widgets und das angezeigte Symbol. Das Symbol wird aus dem von dir eingetragenen Kürzel (Ticker) abgeleitet, zum Beispiel „XETR:VWCE“. Beträge, Gewichtungen oder dein übriges Portfolio werden nicht übertragen.

Nach den Angaben von TradingView setzt das Widget keine Cookies. Es kann aber Daten im lokalen Speicher deines Browsers unter der Domain tradingview-widget.com ablegen. Außerdem weist TradingView in seiner Datenschutzerklärung darauf hin, dass über seine Widgets Analysedaten (zum Beispiel mit Google Analytics) erhoben werden können. Auf diese Verarbeitung haben wir keinen Einfluss. Die Widget-FAQ von TradingView: https://www.tradingview.com/widget-docs/faq/general/

**Zweck:** Anzeige eines Kurscharts zum von dir gewählten Wertpapier oder Coin.

**Rechtsgrundlage:** Deine Einwilligung, Art. 6 Abs. 1 lit. a DSGVO und § 25 Abs. 1 TDDDG (Speicherung von und Zugriff auf Informationen in deinem Endgerät durch das Widget). Widerruf jederzeit wie in Abschnitt 5 beschrieben.

**Speicherdauer:** Bei uns wird zu diesem Vorgang nichts gespeichert außer deinem Einwilligungseintrag. TradingView gibt an, dass die IP-Adresse beim Widget nicht mit identifizierbaren Daten gespeichert und nur kurzfristig vorgehalten wird. Daten im lokalen Speicher unter tradingview-widget.com bleiben, bis du sie in deinen Browsereinstellungen löschst. Weitere Angaben findest du in der Datenschutzerklärung von TradingView.

**Drittlandübermittlung:** Die Daten gehen an TradingView in die USA. Die Datenschutzerklärung von TradingView nennt keinen bestimmten Übermittlungsmechanismus. Wir stützen die Übermittlung deshalb auf deine ausdrückliche Einwilligung (Art. 49 Abs. 1 lit. a DSGVO). Darüber informieren wir dich hier und im Hinweis vor dem Laden (Sitz in den USA): In den USA kann ein anderes Datenschutzniveau als in der EU bestehen und US-Behörden können unter Umständen auf Daten zugreifen. Wenn du das nicht möchtest, klicke nicht auf „Chart laden“.

**Quellenangabe:** Unter dem Chart zeigt TradingView den Hinweis „Track all markets on TradingView“. Er gehört zum Widget und wird unverändert angezeigt.

## 7. Optionale Online-Suche (CoinGecko, Wikidata, Wikimedia Commons)

Im Bearbeitungsmodus kannst du für eine Position eine optionale Online-Suche nutzen, um Aktien, ETFs und Kryptowährungen, Kennungen (ISIN, WKN, Kürzel) und passende Bilder zu finden. Im Suchdialog wählst du die Quelle („Aktien & ETFs“ oder „Krypto“); voreingestellt ist sie nach dem Typ der Kategorie, du kannst sie jederzeit umschalten. Die Anfrage wird erst gesendet, wenn du im Suchdialog auf „Suchen“ klickst oder Enter drückst. Der Dialog weist dich vorher darauf hin, dass dein Suchbegriff und deine IP-Adresse an den jeweiligen Anbieter gesendet werden, und verlinkt auf diese Datenschutzerklärung. Ohne diese Aktion findet keine Verbindung statt.

Folgende Dienste können dabei abgefragt werden:

- **CoinGecko** (api.coingecko.com), Suche nach Kryptowährungen. Anbieter: Gecko Labs Pte. Ltd., Singapur (EU-Vertreter nach Art. 27 DSGVO: Euverify Ltd, Cork, Irland). Datenschutz: https://www.coingecko.com/en/privacy
- **Wikidata** (www.wikidata.org und der zugehörige Abfragedienst query.wikidata.org), Suche nach Wertpapier- und Unternehmensdaten (Quelle „Aktien & ETFs“; der Abfragedienst erhält nur Kennungen der gefundenen Wikidata-Einträge, nicht deinen Suchbegriff), sowie **Wikimedia Commons** (commons.wikimedia.org), Bildersuche. Anbieter beider Dienste: Wikimedia Foundation, Inc., USA. Datenschutz: https://foundation.wikimedia.org/wiki/Policy:Privacy_policy

**Verarbeitete Daten:** Dein Browser sendet deinen Suchbegriff und die dabei technisch notwendigen Daten direkt an den jeweiligen Anbieter: deine IP-Adresse, Browser- und Betriebssystemangaben und die Adresse unserer Website (nur der Hauptteil, „https://finplanr.net/“, als Referrer). Unser Server sieht und speichert deinen Suchbegriff nicht. Die Trefferlisten können Vorschaubilder enthalten (zum Beispiel Coin-Logos von coin-images.coingecko.com oder Bilder von upload.wikimedia.org), die dein Browser ebenfalls direkt von dort lädt.

**Zweck:** Ausführung der von dir angeforderten Suchfunktion und Anzeige der Treffer.

**Rechtsgrundlage:** Art. 6 Abs. 1 lit. b DSGVO, weil die Übermittlung nötig ist, um die von dir ausdrücklich angeforderte Funktion zu erbringen. Hilfsweise Art. 6 Abs. 1 lit. f DSGVO: Unser berechtigtes Interesse besteht darin, dir diese optionale Funktion anzubieten. Deine Interessen überwiegen nicht, weil die Funktion von dir selbst ausgelöst wird, nur den Suchbegriff und technisch notwendige Verbindungsdaten betrifft und wir keine weiteren Daten oder Profile verknüpfen. Es werden dabei keine Informationen auf deinem Gerät gespeichert oder ausgelesen, die eine Einwilligung nach § 25 TDDDG erfordern.

**Speicherdauer:** Bei uns werden die Suchanfragen nicht gespeichert. Die Anbieter speichern Verbindungsdaten nach ihren eigenen Regeln, zum Beispiel gibt die Wikimedia Foundation an, dass die meisten personenbezogenen Daten nach 90 Tagen gelöscht, aggregiert oder anonymisiert werden. CoinGecko speichert Daten so lange, wie es für seine Zwecke und gesetzliche Pflichten erforderlich ist.

**Drittlandübermittlung:** CoinGecko sitzt in Singapur, die Wikimedia Foundation in den USA. Für Singapur gibt es keinen Angemessenheitsbeschluss der EU-Kommission. Die Wikimedia Foundation nennt in ihrer Datenschutzerklärung keine Zertifizierung unter dem EU-US Data Privacy Framework. Die Verbindungen kommen erst durch deine Aktion zustande, nachdem der Dialog dich auf die Übertragung hingewiesen hat. Dass Singapur und die USA außerhalb der EU liegen, steht hier. Soweit die Verbindung eine Übermittlung in ein Drittland ohne Angemessenheitsbeschluss darstellt, stützen wir sie auf Art. 49 Abs. 1 lit. b DSGVO (nötig für die von dir angeforderte Leistung) und, soweit du dich nach dem Hinweis im Dialog für die Suche entscheidest, auf Art. 49 Abs. 1 lit. a DSGVO (ausdrückliche Einwilligung nach Information über die Risiken).

**Folgen:** Wenn du die Suche nicht nutzt, entstehen diese Verbindungen nicht. Die App lässt sich vollständig auch ohne Suche bedienen (Kennungen und Namen kannst du von Hand eintragen).

## 8. Logos und externe Bilder

Die Logos der Standardwerte (6 Kryptowährungen und 11 Fondsanbieter) sowie die Symbole der App werden von unserem eigenen Server ausgeliefert. Beim normalen Aufruf von Finplanr werden **keine** Logos von Drittanbietern geladen.

Eine Verbindung zu einem Drittanbieter entsteht nur, wenn du selbst eine externe Bildquelle auswählst:

- eine **Bildadresse (URL)**, die du eingibst (der Anbieter ist dann der Betreiber des Servers hinter dieser Adresse),
- ein **Bild aus Wikimedia Commons**, das du im Bild-Picker auswählst (upload.wikimedia.org, Wikimedia Foundation, Inc., USA),
- das **Logo, das CoinGecko** für eine über die Suche hinzugefügte Kryptowährung liefert (coin-images.coingecko.com bzw. assets.coingecko.com, Gecko Labs Pte. Ltd., Singapur).

Diese Adresse wird dann in deinen lokalen Einstellungen (Abschnitt 4) gespeichert, und dein Browser lädt das Bild bei jedem späteren Besuch erneut vom jeweiligen Anbieter („Hotlinking“). Der Anbieter sieht dabei deine IP-Adresse, deine Browser-Angaben und die Adresse unserer Website (Referrer, nur Hauptteil) und kann daraus ablesen, dass du Finplanr nutzt. Das gilt für jede Seite, die du dort hinterlegst.

**So vermeidest du das:** Nutze Symbole oder ein selbst hochgeladenes Bild (wird als Daten in deinem Browser gespeichert und nirgendwohin übertragen) oder die mitgelieferten Logos. Ein bereits gesetztes externes Logo entfernst du im Bearbeitungsmodus über „Standard-Logo verwenden“.

**Rechtsgrundlage:** Art. 6 Abs. 1 lit. b DSGVO (die von dir gewählte Darstellung deines Portfolios), hilfsweise Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse, dir die gewünschte Anpassung zu ermöglichen; die Auswahl nimmst du selbst vor).

**Speicherdauer und Drittlandübermittlung:** Bei den Anbietern gelten deren eigene Regeln (Abschnitt 7 bzw. deren Datenschutzerklärungen). Für Wikimedia Commons und CoinGecko gilt dieselbe Einordnung wie in Abschnitt 7. Bei frei eingegebenen Adressen entscheidest du selbst, welchen Server du kontaktierst.

## 9. Kontaktaufnahme per E-Mail

Wenn du uns per E-Mail an {{EMAIL}} schreibst, verarbeiten wir die von dir übermittelten Daten: deine E-Mail-Adresse, deinen Namen (soweit angegeben), den Inhalt deiner Nachricht und technische Angaben zur Zustellung.

**Technischer Ablauf:** Die Adresse {{EMAIL}} ist eine Weiterleitung über Cloudflare Email Routing (Cloudflare, Inc., USA, als Auftragsverarbeiter). Cloudflare leitet die Nachricht an das private Postfach des Betreibers weiter. Anbieter dieses Postfachs ist: {{MAILBOX_PROVIDER}}. Antworten werden aus demselben Postfach versendet.

Das im Impressum verlinkte Kontaktformular wird vom Anbieter der Impressum-Seite ({{IMPRESSUM_PROVIDER}}) betrieben und leitet deine Nachricht an uns weiter. Dessen Datenverarbeitung richtet sich nach den Datenschutzhinweisen auf der dortigen Seite.

**Zweck und Rechtsgrundlage:** Bearbeitung und Beantwortung deiner Anfrage. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der Beantwortung von Anfragen), bzw. Art. 6 Abs. 1 lit. b DSGVO, wenn sich deine Anfrage auf eine Leistung von uns bezieht.

**Speicherdauer:** So lange, wie es zur Bearbeitung deines Anliegens erforderlich ist. Danach löschen wir die Korrespondenz, sofern keine gesetzlichen Aufbewahrungspflichten eine längere Speicherung verlangen.

**Pflicht zur Bereitstellung:** Du bist nicht verpflichtet, uns zu schreiben. Ohne deine E-Mail-Adresse können wir dir aber nicht antworten. **Drittlandübermittlung:** siehe Abschnitt 11 (Cloudflare).

## 10. Cookies und vergleichbare Technologien

Finplanr setzt selbst keine Cookies. Es gibt keine Werbe-, Marketing- oder Analysecookies und keine Analysedienste.

Zur Speicherung deiner Einstellungen wird der lokale Speicher deines Browsers verwendet (Abschnitt 4). Das TradingView-Widget schreibt nach deiner Einwilligung Daten in den lokalen Speicher unter tradingview-widget.com (Abschnitt 6).

Cloudflare kann bei aktivierten Schutzfunktionen technisch erforderliche Cookies setzen (zum Beispiel zur Bot-Erkennung wie `__cf_bm` oder `cf_clearance`). Diese dienen ausschließlich der Sicherheit und dem Betrieb (§ 25 Abs. 2 Nr. 2 TDDDG). Näheres: https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/

**Google AdSense, Google Analytics und andere Werbe- oder Analysedienste sind nicht eingebunden.** Sollten künftig Werbung oder zusätzliche Dienste hinzukommen, wird diese Datenschutzerklärung vor der Aktivierung aktualisiert und, soweit erforderlich, vorab deine Einwilligung eingeholt.

## 11. Empfänger und Datenübermittlungen in Drittländer

Empfänger personenbezogener Daten sind je nach deiner Nutzung:

- **Cloudflare, Inc.** (USA, mit Unternehmen in der EU): Hosting-Infrastruktur, Weiterleitung, Sicherheit, E-Mail-Weiterleitung (Auftragsverarbeiter, Abschnitte 3 und 9)
- **TradingView.com, Inc.** (USA): nur nach deiner Einwilligung, Abschnitt 6
- **Gecko Labs Pte. Ltd. / CoinGecko** (Singapur): nur bei Nutzung der Krypto-Suche oder wenn du ein CoinGecko-Logo verwendest, Abschnitte 7 und 8
- **Wikimedia Foundation, Inc.** (USA): nur bei Nutzung der Wikidata-/Commons-Suche oder wenn du ein Commons-Bild verwendest, Abschnitte 7 und 8
- {{MAILBOX_RECIPIENT}}
- der Anbieter der Impressum-Seite ({{IMPRESSUM_PROVIDER}}): bei Formularkontakt über deren Seite
- vom dir eingegebene **Bildserver**: wenn du eine externe Bildadresse einträgst, Abschnitt 8

Weitere Empfänger gibt es nicht. Eine Weitergabe zu Werbezwecken findet nicht statt.

**Drittlandübermittlungen und Garantien (Art. 13 Abs. 1 lit. f DSGVO):**

- **Cloudflare, Inc. (USA):** Cloudflare erklärt, unter dem EU-US Data Privacy Framework (DPF) zertifiziert zu sein. Für Übermittlungen an zertifizierte US-Unternehmen hat die EU-Kommission mit Beschluss vom 10. Juli 2023 ein angemessenes Datenschutzniveau festgestellt (Art. 45 DSGVO). Fällt die Zertifizierung weg, greifen nach Cloudflares Angaben die EU-Standardvertragsklauseln (Art. 46 Abs. 2 lit. c DSGVO), die Teil des Auftragsverarbeitungsvertrags sind. Informationen: https://www.cloudflare.com/trust-hub/gdpr/
- **TradingView (USA):** keine Angabe eines Übermittlungsmechanismus in deren Datenschutzerklärung; Grundlage ist deine ausdrückliche Einwilligung, Art. 49 Abs. 1 lit. a DSGVO (Abschnitt 6).
- **CoinGecko (Singapur):** kein Angemessenheitsbeschluss; Grundlage Art. 49 Abs. 1 lit. b bzw. lit. a DSGVO (Abschnitt 7). CoinGecko hat zudem einen EU-Vertreter benannt.
- **Wikimedia Foundation (USA):** keine DPF-Zertifizierung bekannt bzw. angegeben; Grundlage Art. 49 Abs. 1 lit. b bzw. lit. a DSGVO (Abschnitt 7).
- {{MAILBOX_TRANSFER}}

Eine Kopie der genannten Garantien (z. B. der Standardvertragsklauseln) kannst du über die oben verlinkten Seiten der Anbieter einsehen; bei Fragen schreibe an die in Abschnitt 1 genannte Adresse. Die Standardvertragsklauseln der EU-Kommission findest du unter https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj

## 12. Speicherdauer im Überblick

- **Server-Logs auf unserem Server:** durch automatische Log-Rotation begrenzt (3 Dateien à 10 MB); in der Regel wenige Tage bis Wochen, spätestens bis zum Überschreiben.
- **Protokolle bei Cloudflare:** keine feste Frist veröffentlicht; nur so lange wie nötig, danach gelöscht oder anonymisiert (siehe deren Datenschutzerklärung).
- **Portfolio, Reset-Stand, Spracheinstellung:** in deinem Browser, bis du sie löschst. Sie liegen nicht auf unserem Server.
- **Einwilligungseintrag (TradingView):** in deinem Browser, bis du widerrufst oder die Website-Daten löschst.
- **Online-Suche und externe Bilder:** bei uns keine Speicherung. Bei den Anbietern nach deren Regeln (Wikimedia: in der Regel 90 Tage; TradingView: IP kurzfristig; CoinGecko: nach Erforderlichkeit).
- **E-Mails:** bis zur Erledigung deines Anliegens, danach Löschung, soweit keine gesetzliche Aufbewahrungspflicht besteht.

## 13. Pflicht zur Bereitstellung von Daten

Die Nutzung von Finplanr ist ohne die Angabe personenbezogener Daten möglich. Eine gesetzliche oder vertragliche Pflicht zur Bereitstellung besteht nicht.

Bei jedem Seitenaufruf müssen technisch bedingt Verbindungsdaten wie deine IP-Adresse übertragen werden, sonst kann die Seite nicht ausgeliefert werden. Für Chart, Online-Suche und externe Logos gilt: Wenn du die jeweilige Funktion nicht nutzt oder deine Einwilligung nicht erteilst, entstehen keine Verbindungen zu den Drittanbietern. Die Folge ist lediglich, dass das Chart oder die Suchergebnisse nicht angezeigt werden. Wenn du uns schreibst, brauchen wir deine E-Mail-Adresse für die Antwort.

## 14. Externe Links

Finplanr enthält Links auf externe Seiten, zum Beispiel zu Produktseiten von Fondsanbietern, zur Deutschen Börse, zu justETF, Finanzfluss, CoinGecko und TradingView sowie zum Impressum bei {{IMPRESSUM_PROVIDER}}. Sie öffnen sich nur, wenn du sie anklickst, in einem neuen Tab. Beim Aufruf verlässt du Finplanr. Für die dortige Verarbeitung personenbezogener Daten ist der jeweilige Anbieter nach seinen eigenen Datenschutzinformationen verantwortlich.

## 15. Deine Rechte

Dir stehen nach der DSGVO folgende Rechte zu, soweit die jeweiligen Voraussetzungen vorliegen:

- Auskunft über die Verarbeitung deiner personenbezogenen Daten (Art. 15 DSGVO)
- Berichtigung unrichtiger Daten (Art. 16 DSGVO)
- Löschung (Art. 17 DSGVO)
- Einschränkung der Verarbeitung (Art. 18 DSGVO)
- Datenübertragbarkeit (Art. 20 DSGVO)
- **Widerspruch** gegen Verarbeitungen, die auf Art. 6 Abs. 1 lit. f DSGVO beruhen, aus Gründen, die sich aus deiner besonderen Situation ergeben (Art. 21 DSGVO)
- **Widerruf** einer erteilten Einwilligung jederzeit mit Wirkung für die Zukunft (Art. 7 Abs. 3 DSGVO). Die TradingView-Einwilligung widerrufst du über „Datenschutz-Einstellungen“ in der Fußzeile der App.

Zur Ausübung deiner Rechte schreibe an die in Abschnitt 1 genannte Adresse. Beachte, dass wir keine Portfolios von dir speichern; dein Portfolio kannst du selbst im Browser einsehen, exportieren und löschen (Abschnitt 4).

**Beschwerderecht:** Du hast das Recht, dich bei einer Datenschutzaufsichtsbehörde zu beschweren (Art. 77 DSGVO), insbesondere in dem Mitgliedstaat deines gewöhnlichen Aufenthalts, deines Arbeitsplatzes oder des Orts des mutmaßlichen Verstoßes. Zuständig ist in der Regel die Aufsichtsbehörde an deinem Wohnort oder an dem Ort, an dem der Verantwortliche seinen Sitz hat; die Aufsichtsbehörden der Mitgliedstaaten findest du unter https://www.edpb.europa.eu/about-edpb/about-edpb/members_de.

## 16. Keine automatisierten Entscheidungen

Finplanr berechnet Sparbeträge und Gewichtungen anhand der von dir gewählten Eingaben, direkt in deinem Browser. Eine automatisierte Entscheidungsfindung einschließlich Profiling im Sinne von Art. 22 DSGVO findet nicht statt.

## 17. Änderungen dieser Datenschutzerklärung

Wir passen diese Datenschutzerklärung an, wenn sich die Funktionen von Finplanr, die eingesetzten Dienstleister oder die rechtlichen Anforderungen ändern. Die jeweils aktuelle Fassung findest du unter https://finplanr.net/datenschutz.html (Stand siehe oben). Sie ist auch über den Link „Datenschutz“ in der Fußzeile der App erreichbar.
