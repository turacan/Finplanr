# Privacy Policy for Finplanr

**Last updated: 15 October 2026**

## 1. Controller

The controller responsible for processing personal data in connection with the website https://finplanr.net is:

{{OPERATOR_NAME}}  
{{ADDRESS_BLOCK}}  
Email: {{EMAIL}}

Further details about the operator are in the legal notice (Impressum): {{IMPRESSUM_URL}}

No data protection officer has been appointed because there is no legal obligation to do so. For any data protection question, contact the controller at the address above.

## 2. General information about data processing

Finplanr is a free web application for planning and splitting monthly savings amounts across asset classes such as ETFs, ETCs, cryptocurrencies and cash. It can be used without registration or a user account. There is no advertising, no tracking and no analytics service.

Finplanr has no central database for individual portfolios. Your entries (amounts, weights, names, identifiers) are stored only in the browser on your device and are not transmitted to the operator.

Personal data is nevertheless processed in the following cases:

- whenever the website is accessed (technical access data, section 3),
- when you use local storage in your browser (section 4),
- when you allow and load a TradingView price chart (sections 5 and 6, only with your consent),
- when you allow and use the optional online search (sections 5 and 7, only with your consent),
- when you choose a logo or image from an external provider (section 8),
- when you contact us by email (section 9).

There are two functions that contact third parties and therefore need your prior, explicit consent: **price charts** (TradingView) and **online search** (CoinGecko, Wikidata, Wikimedia Commons). Until you consent to a function, your browser sends nothing to the providers of that function. The built-in catalog search works locally in your browser and needs no consent.

On a normal page view without these actions, no data is sent to any third party other than Cloudflare (section 3). All scripts, styles and logos of the application are delivered from our own server; no web fonts or scripts are loaded from third parties. However, Cloudflare may insert a security script of its own when delivering pages and sets a technically necessary cookie (sections 3 and 10).

## 3. Providing the website, hosting, Cloudflare and server logs

The website is served from a privately operated server of the operator, running an Nginx web server in a Docker container. The server is not directly reachable from the internet, only through a Cloudflare Tunnel.

We use Cloudflare for DNS, the encrypted HTTPS connection, forwarding requests to our server (Cloudflare Tunnel), caching static files (CDN) and technical security functions. Your requests therefore pass through Cloudflare's servers. Cloudflare technically decrypts the connection in order to forward it to our server.

**Provider:** Cloudflare, Inc., 101 Townsend St., San Francisco, CA 94107, USA, and affiliated companies (including in the EU).

**Data processed by Cloudflare:** Each request involves in particular:

- IP address
- date and time of access
- page or file requested and HTTP status code
- amount of data transferred
- referrer (the page you came from), if your browser sends it
- browser type, browser version and operating system (user agent)
- approximate location (country), which Cloudflare derives from the IP address
- technical connection and browser characteristics (for example the TLS protocol version) and security data that are evaluated to detect and block abusive or automated access

**Cloudflare bot detection and cookie:** When delivering our pages, Cloudflare inserts a small script ("JavaScript Detections"). It is loaded through our own domain (path `/cdn-cgi/`), runs in the background, checks technical characteristics of your browser to tell automated access (bots) from human visits, and sends the result to Cloudflare. In the process Cloudflare sets the cookie `cf_clearance` (see section 10). This serves security, not audience measurement or advertising; we do not use this data for evaluations of our own.

**Server logs on our server:** Our web server's access log is deliberately limited to the following fields per request: time of the request, HTTP method, requested path (without query string), status code and size of the response. It contains **no IP address** (including no forwarded address from the Cloudflare Tunnel), **no referrer and no user agent**. To our assessment the access log therefore contains no personal data. The web server's error log (technical error messages, for example for blocked requests) may additionally contain the address of the connecting client, the requested address and, if sent, the referrer; behind the tunnel the client address is the internal address of the tunnel connector on our server, not your address. The tunnel connector (cloudflared) also writes a log on our server; at the standard log level we use, it contains connection, status and error messages of the tunnel, but no individual page views and no visitor addresses. We do not evaluate the logs systematically, do not combine them with other data and do not create user profiles. They are used only for troubleshooting.

**Cloudflare Network Error Logging:** Cloudflare offers an optional feature that asks browsers to send network error reports to a Cloudflare reporting address. We have deactivated this feature, so your browser is not asked to send such reports.

**Purpose and legal basis:** The processing serves to provide the website securely, stably and functionally and to defend against attacks. The legal basis is Art. 6(1)(f) GDPR (legitimate interest in the secure and reliable operation of the website and in protection against attacks and automated abuse). In our assessment, the Cloudflare cookie and security script are technically necessary for the secure and stable operation of the service you requested (section 25(2) no. 2 TDDDG).

**Role of Cloudflare:** Where Cloudflare processes data on our behalf (in particular the traffic logs), it acts as a processor under Art. 28 GDPR. A data processing agreement (Data Processing Addendum, DPA) with Cloudflare is in place; according to Cloudflare it incorporates the EU Standard Contractual Clauses. For some data Cloudflare states that it is itself a controller; details are in Cloudflare's privacy policy: https://www.cloudflare.com/privacypolicy/

**Retention:** The logs on our server (web server and tunnel connector) are rotated automatically by size by Docker (at most three files of 10 MB each per log); older entries are overwritten. How long an entry exists depends on traffic: because the lines are short, with little traffic this can be several months; at the latest an entry is gone when log rotation overwrites it. The cookie `cf_clearance` stays in your browser for up to about one year (section 10). Cloudflare's privacy policy gives no fixed period for traffic logs; data is kept there only as long as needed for the services and legal obligations and then deleted or anonymised. See Cloudflare's privacy policy linked above.

**Third-country transfer:** Cloudflare also processes data in the USA. Cloudflare, Inc. states that it is certified under the EU-US Data Privacy Framework (adequacy decision of the European Commission of 10 July 2023) and otherwise relies on the EU Standard Contractual Clauses. More in section 11.

## 4. Local storage in your browser, export and import

Finplanr saves your settings in your browser's local storage so that they are there the next time you visit. This data does not leave your browser and is not transmitted to us.

The following entries are created:

- `mein-sparplan-portfolio-v1`: your portfolio, i.e. monthly savings budget, categories and positions, weights and amounts, names, tickers, ISIN, WKN, colours, symbols, logos (including images you upload yourself or that were copied into your browser, see section 8), locked weights, sort order and display settings
- `mein-sparplan-reset-stand-v1`: a personal reset point that you saved
- `finplanr-consent`: a single entry recording your privacy choices (one decision per function, "charts" and "online search", each with the time of the decision), see section 5

On your first visit the local storage is empty: entries are only created once you change something in your portfolio (or save a reset point or give a consent). Finplanr does **not** store a language setting: the language follows the address you open (`finplanr.net/` is English, `finplanr.net/de/` is German). Entries written by earlier versions (`finplanr-lang` and `finplanr-consent-tv`) are removed from your browser automatically when you visit. Finplanr does not use session storage.

Finplanr itself sets no cookies of its own (for cookies from Cloudflare see section 10).

**Legal basis:** Storing and reading the portfolio entries is covered by section 25(2) no. 2 TDDDG (Telecommunications Digital Services Data Protection Act), because it is strictly necessary for the function you explicitly requested (planning and restoring your portfolio). No consent is needed for it. Where personal data is processed in the process, the legal basis is Art. 6(1)(b) GDPR (providing the function you use) and, alternatively, Art. 6(1)(f) GDPR (legitimate interest in making the application usable). The same applies to the entry `finplanr-consent`, which is needed to remember your choices and to be able to prove them (Art. 7(1) GDPR).

**Retention and deletion:** The data stays in your browser until you delete it. You can remove it at any time: "Restore factory defaults" (in the app's settings) replaces your portfolio with the built-in example and deletes the reset point; you withdraw your privacy choices in the "Privacy settings" dialog. You remove all entries together by deleting the site data for finplanr.net in your browser settings. Switching browser or device does not transfer the data automatically.

**Export and import:** Finplanr can export your portfolio as a JSON file and the current plan as a CSV table, and can import a JSON backup. These files are created and read entirely in your browser. They are saved to or read from your device and are not transmitted to us or anyone else. You are responsible for keeping these files safe. The copy buttons (for example for ISIN or WKN) only place the value on your device's clipboard; nothing is transmitted.

## 5. Privacy settings and consent {#consent}

Finplanr has no cookie banner and no consent dialog when a page loads, because Finplanr itself sets no cookies of its own, loads nothing from third parties on page load and the only cookie set on page load (by Cloudflare, section 10) is, in our view, technically necessary. Instead, consent is asked **at the point of use**, separately for each of two purposes and **before any request** is sent to the providers:

- **Charts** (TradingView.com, Inc., USA): a box in the chart panel explains what happens and asks for your consent before the chart widget is loaded.
- **Online search** (CoinGecko = Gecko Labs Pte. Ltd., Singapore; Wikidata, the Wikidata query service and Wikimedia Commons = Wikimedia Foundation, Inc., USA): a box in the search dialog explains what happens and asks for your consent before the first online request. The search in the built-in catalog works without it.

You can give and withdraw your consent also at any time in the **"Privacy settings"** dialog (link in the app footer). It lists both purposes; you can allow or withdraw each one separately. A change takes effect immediately, also in all other open tabs and windows of the same browser: a withdrawn function is stopped there as well (for example an open chart is closed) and nothing further is loaded from the provider until you consent again.

**Legal bases:**

- Your explicit consent is the basis for the processing under **Art. 6(1)(a) GDPR**.
- For the transfer of your data to the providers in the USA and Singapore we rely on your explicit consent under **Art. 49(1)(a) GDPR** (see "Risks of the transfers" below).
- Where the TradingView widget stores or reads information in your browser (section 6), the basis is your consent under **section 25(1) TDDDG**.
- Storing your choice itself (`finplanr-consent`, section 4) is technically necessary for the function you requested (section 25(2) no. 2 TDDDG).

**Risks of the transfers (Art. 49(1)(a) GDPR):** For the providers listed above the European Commission has either not issued an adequacy decision (Singapore) or we cannot state a certification under the EU-US Data Privacy Framework (TradingView, Wikimedia Foundation), and we have no standard contractual clauses with them. This means: the level of data protection there may be lower than in the EU, public authorities in these countries may be able to access data without you having enforceable rights or effective legal remedies comparable to those in the EU, and the providers are not bound by our privacy policy. The consent boxes and this section tell you this before you decide. The consent is voluntary: without it the whole app keeps working, just without the embedded chart and without the online search.

**Withdrawal:** You can withdraw your consent at any time with effect for the future, for each purpose separately, in the "Privacy settings" dialog. Data that a provider has already received or stored in your browser is not deleted by the withdrawal; you can remove data in your browser (for TradingView under the site data for tradingview-widget.com) in your browser settings and ask the provider for deletion. The lawfulness of the processing carried out until the withdrawal is not affected (Art. 7(3) GDPR).

## 6. Price charts from TradingView

When you click the name of a position in the app, a price chart panel opens below it. For this we embed TradingView's "Advanced Chart" widget. Nothing is loaded from TradingView without your consent (section 5): the panel first shows a consent box; only after you confirm it (or have allowed charts in the "Privacy settings") is the widget loaded.

**Provider:** TradingView.com, Inc., 1330 Avenue of the Americas, 23rd Floor, New York, NY 10019, USA. According to its privacy policy TradingView has appointed a representative in the EU under Art. 27 GDPR in Barcelona (Spain). Privacy policy: https://www.tradingview.com/privacy-policy/

**Data processed:** After your consent, your browser connects to TradingView (in our test: s3.tradingview.com, www.tradingview-widget.com, widget-sheriff.tradingview-widget.com, scanner-backend.tradingview.com, s3-symbol-logo.tradingview.com and www.tradingview.com; TradingView may change these servers). In particular the following is transmitted:

- your IP address and technical connection data (such as browser and operating system),
- the address of the embedding page (for us finplanr.net or finplanr.net/de/, without parameters) and the chosen language,
- the widget type and the displayed symbol. The symbol is derived from the ticker you entered, for example "XETR:VWCE". Amounts, weights and the rest of your portfolio are not transmitted.

According to TradingView, the widget sets no cookies; in our test it set none. It does, however, store data in your browser's local storage under the domain tradingview-widget.com (a storage area separate from that of finplanr.net; in our test, settings of the chart). TradingView also states in its privacy policy that analytics data (for example with Google Analytics) may be collected through its widgets. We have no influence over this processing. TradingView's widget FAQ: https://www.tradingview.com/widget-docs/faq/general/

**Purpose:** Showing a price chart for the security or coin you selected.

**Legal basis:** Your consent, Art. 6(1)(a) GDPR and section 25(1) TDDDG (storing and reading information on your device by the widget). You can withdraw it at any time as described in section 5.

**Retention:** Nothing is stored on our side for this except your consent entry. TradingView states that for the widget the IP address is not stored together with identifiable data and is retained only short-term. Data in local storage under tradingview-widget.com remains until you delete it in your browser settings. See TradingView's privacy policy for more.

**Third-country transfer:** The data goes to TradingView in the USA. TradingView's privacy policy names no specific transfer mechanism. We therefore rely on your explicit consent after being informed of the risks (Art. 49(1)(a) GDPR; risks as described in section 5): the level of data protection in the USA may differ from that in the EU, and US authorities may under certain circumstances access data. If you do not want this, do not consent to charts.

**Attribution:** Below the chart TradingView shows the note "Track all markets on TradingView". It is part of the widget and shown unchanged.

## 7. Optional online search (CoinGecko, Wikidata, Wikimedia Commons)

In edit mode you can use a search for a position to find stocks, ETFs and cryptocurrencies, identifiers (ISIN, WKN, ticker) and suitable images. In the search dialog you choose the source ("Stocks & ETFs" or "Crypto"); it defaults to the category type and you can switch it at any time. Searching the **built-in catalog** takes place locally in your browser and needs no consent. The **online search** only runs after your explicit consent (section 5): the dialog shows a consent box first, and no request is sent to any provider until you have confirmed it (or allowed the online search in the "Privacy settings"). The box names the providers and links to this privacy policy.

**Logo offer after adding a holding:** When you apply a search result that comes without a logo (not for savings accounts), the dialog offers to look for a logo and shows a short second step. This logo search is an image search at Wikimedia Commons and is covered by the same consent as the rest of the online search: if you have not allowed it yet, the second step only shows the consent box with the choice "Allow online search" or "Skip", and nothing is requested before you confirm. Your search term is then the name of the holding without legal suffixes plus the word "logo" (for example "Apple logo"); you can change it before searching. Choosing "Skip", pressing Esc or closing the dialog keeps the holding without a logo. You can switch the offer off for good with the box "Don't offer a logo search when adding holdings" in that step or in Settings ("Offer a logo search when I add a holding"); the setting is stored in your browser together with your plan (section 4).

The following services may be queried after your consent:

- **CoinGecko** (api.coingecko.com), search for cryptocurrencies. Provider: Gecko Labs Pte. Ltd., Singapore (EU representative under Art. 27 GDPR: Euverify Ltd, Cork, Ireland). Privacy: https://www.coingecko.com/en/privacy
- **Wikidata** (www.wikidata.org and its query service query.wikidata.org), search for security and company data (source "Stocks & ETFs"; the query service only receives the identifiers of the Wikidata entries found, not your search term), and **Wikimedia Commons** (commons.wikimedia.org), image search. Provider of these services: Wikimedia Foundation, Inc., USA. Privacy: https://foundation.wikimedia.org/wiki/Policy:Privacy_policy

**Data processed:** Your browser sends your search term and the technically necessary data directly to the respective provider: your IP address, browser and operating system details, and, as the origin of the request, the address "https://finplanr.net" (Finplanr sends no referrer with these requests). Our server neither sees nor stores your search term. The result lists may contain preview images (for example coin logos from coin-images.coingecko.com or images from thumb.wikimedia.org or upload.wikimedia.org), which your browser also loads directly from there.

**Cookies:** Finplanr loads these preview images in a mode in which your browser sends no cookies to the image servers and accepts none from them (the HTML attribute `crossorigin="anonymous"`, which makes the browser fetch the image without credentials). The same applies to the search requests themselves and to the copy of a picked image (section 8). We measured the effect: if the preview images are loaded in the ordinary way, the Wikimedia image servers (thumb.wikimedia.org, upload.wikimedia.org) set the cookies `WMF-Uniq` (valid for up to about one year) and `NetworkProbeLimit` (about one hour). With the mode used by Finplanr, in our test (search, preview images, picking an image) no cookie of CoinGecko, Wikidata or Wikimedia was stored in the browser; the servers still send cookie headers, but the browser discards them. This can change if a provider changes its servers; we re-check it from time to time. The only exception is an image you hotlink yourself (section 8).

**Purpose:** Running the search function you requested and showing the results.

**Legal basis:** Your explicit consent, Art. 6(1)(a) GDPR. Because no information is stored on or read from your device by these providers (see "Cookies" above), section 25 TDDDG does not apply to the search. You can withdraw your consent at any time as described in section 5.

**Retention:** We do not store your search requests. The providers keep connection data under their own rules; for example the Wikimedia Foundation states that most personal data is deleted, aggregated or de-identified after 90 days. CoinGecko keeps data as long as needed for its purposes and legal obligations.

**Third-country transfer:** CoinGecko is based in Singapore and the Wikimedia Foundation in the USA. There is no European Commission adequacy decision for Singapore. The Wikimedia Foundation's privacy policy names no certification under the EU-US Data Privacy Framework, and we have no standard contractual clauses with either provider. We therefore base the transfer solely on your explicit consent after being informed of the risks (**Art. 49(1)(a) GDPR**; the risks are described in section 5 and in the consent box). If you do not want this, do not consent to the online search.

**Consequences:** If you do not consent, these connections do not occur. The app is fully usable without the online search (you can use the built-in catalog or enter identifiers and names by hand).

## 8. Logos and external images

The logos of the default entries (6 cryptocurrencies and 11 fund issuers) and the app's symbols are delivered from our own server. A normal visit to Finplanr loads **no** logos from third parties. A holding without a logo gets a small **letter badge** (ticker or initials on a coloured background), which your browser draws itself from the holding's name: it uses no image and makes no request.

A connection to a third party arises only if you yourself pick an external image source:

- an **image address (URL)** that you enter (the provider is then the operator of the server behind that address),
- an **image from Wikimedia Commons** that you pick in the image picker (thumb.wikimedia.org or upload.wikimedia.org, Wikimedia Foundation, Inc., USA),
- the **logo returned by CoinGecko** for a cryptocurrency you add via the search (coin-images.coingecko.com, Gecko Labs Pte. Ltd., Singapore).

Images from Wikimedia Commons and CoinGecko come from the online search and are covered by your consent to it (section 5). This includes the logo search that is offered after you add a holding (section 7): it only runs after that consent, and you can switch the offer off in Settings.

**What happens to the image you pick:** When you choose an external image, Finplanr tries to **copy it into your browser's local data** (as a data URL of at most 150 KB). Once that has worked, the image is shown from your own browser and your browser makes **no further requests** to the image server on later visits. Only the one-time retrieval at the time of picking contacts the provider (your IP address, browser details and, as the origin of the request, "https://finplanr.net"; Finplanr sends no referrer and no cookies with this retrieval and accepts none).

**If copying fails** (for example because the image is larger than 150 KB or the server does not allow the copy), the address is saved instead and your browser loads the image from its original server **on every later visit** ("hotlinking"). The provider then receives two or three requests already when you pick the image (the failed copy attempt and the display) and later sees your IP address and your browser details each time. Finplanr first requests the image without cookies and without referrer, stating "https://finplanr.net" as the origin of the request, so the provider can infer from this that you use Finplanr. If the server does not allow that kind of request (this is why the copy often fails), the app repeats the request once as a plain image request, still without referrer; in that case the server can set or read cookies of its own, which Finplanr cannot prevent. This is your own choice by picking that image; the app points it out with a notice when the copy was not possible. This applies to any site you enter there.

**How to avoid this:** Use symbols, an image you upload yourself (stored as data in your browser and not transmitted anywhere) or the bundled logos. To remove an external logo you already set, use "Use default logo" in edit mode.

**Legal basis:** For Commons and CoinGecko images: your consent, Art. 6(1)(a) and Art. 49(1)(a) GDPR (sections 5 and 7). For an image address you enter yourself: Art. 6(1)(b) GDPR (the presentation of your portfolio that you chose) and, alternatively, Art. 6(1)(f) GDPR (legitimate interest in letting you make the customisation you want; you make the selection yourself). If the server of an image you hotlink yourself sets or reads cookies of its own, this happens at your own request (section 25(2) no. 2 TDDDG, because the display of the image you chose requires the request) and under that provider's responsibility.

**Retention and third-country transfer:** The providers' own rules apply (section 7 or their privacy policies). For freely entered addresses you decide which server you contact; we cannot know its location.

## 9. Contact by email

If you email us at {{EMAIL}}, we process the data you send: your email address, your name (if given), the content of your message and technical delivery information.

**Technical flow:** {{EMAIL}} is a forwarding address through Cloudflare Email Routing (Cloudflare, Inc., USA, as processor). Cloudflare forwards the message to the operator's private mailbox. The provider of that mailbox is: {{MAILBOX_PROVIDER}}. Replies are sent from the same mailbox.

The contact form linked in the legal notice is operated by the provider of the Impressum page ({{IMPRESSUM_PROVIDER}}) and passes your message on to us. Its data processing is governed by the privacy information on that page.

**Purpose and legal basis:** Handling and answering your enquiry. The legal basis is Art. 6(1)(f) GDPR (legitimate interest in answering enquiries) or Art. 6(1)(b) GDPR if your enquiry relates to a service from us.

**Retention:** As long as needed to handle your request. After that we delete the correspondence unless statutory retention duties require longer storage.

**Obligation to provide data:** You are not obliged to write to us. Without your email address we cannot reply, however.

**Third-country transfer:** see section 11 (Cloudflare and mailbox provider).

## 10. Cookies and similar technologies

Finplanr itself sets no cookies of its own. There are no advertising, marketing or analytics cookies and no analytics services. For this reason there is no global cookie banner: consent is requested only at the point of use for the two functions described in section 5.

**Cookie from Cloudflare:** When our pages are loaded, Cloudflare currently sets the cookie `cf_clearance` (a bot-detection cookie, see section 3). It is an HttpOnly cookie, is only transmitted over HTTPS, remembers that the check was passed, and in our test is valid for up to about one year. Depending on the protection features enabled at Cloudflare, further technically necessary cookies may be added (for example `__cf_bm`). In our view these cookies are technically necessary for the secure operation of the service (section 25(2) no. 2 TDDDG). You can delete or block them in your browser settings at any time; the app keeps working, and the bot check is simply done again on a later visit. More: https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/

Your settings and your privacy choices are stored in your browser's local storage (section 4). After your consent, the TradingView widget stores data in local storage under tradingview-widget.com (section 6); the images of the online search are loaded in a way that stores no cookies of CoinGecko or Wikimedia in your browser (section 7). The only possible exception is an image you hotlink yourself (section 8).

**Google AdSense, Google Analytics and other advertising or analytics services are not integrated.** If advertising or additional services are added in future, this privacy policy will be updated before activation and, where required, your consent obtained beforehand.

## 11. Recipients and transfers to third countries

Depending on your use, personal data goes to:

- **Cloudflare, Inc.** (USA, with companies in the EU): DNS, forwarding (tunnel), caching, security and bot detection, email forwarding (processor, sections 3 and 9)
- **TradingView.com, Inc.** (USA): only after your consent, section 6
- **Gecko Labs Pte. Ltd. / CoinGecko** (Singapore): only after your consent to the online search (crypto search, CoinGecko logos), sections 7 and 8
- **Wikimedia Foundation, Inc.** (USA): only after your consent to the online search (Wikidata and its query service, Wikimedia Commons search and images), sections 7 and 8
- {{MAILBOX_RECIPIENT}}
- the provider of the Impressum page ({{IMPRESSUM_PROVIDER}}): when you use the contact form on that page
- **image servers you enter yourself**: when you enter an external image address, section 8

There are no other recipients. Data is not shared for advertising purposes.

**Third-country transfers and safeguards (Art. 13(1)(f) GDPR):**

- **Cloudflare, Inc. (USA):** Cloudflare states that it is certified under the EU-US Data Privacy Framework (DPF). For transfers to certified US companies, the European Commission found an adequate level of protection by decision of 10 July 2023 (Art. 45 GDPR). If the certification lapses, Cloudflare states that the EU Standard Contractual Clauses apply (Art. 46(2)(c) GDPR), which are part of the data processing agreement. Information: https://www.cloudflare.com/trust-hub/gdpr/
- **TradingView (USA):** its privacy policy names no transfer mechanism and we have no certification to rely on; no adequacy decision or other safeguard is stated. The basis is your explicit consent after being informed of the risks, Art. 49(1)(a) GDPR (sections 5 and 6).
- **CoinGecko (Singapore):** no adequacy decision and no safeguards stated; the basis is your explicit consent after being informed of the risks, Art. 49(1)(a) GDPR (sections 5 and 7). CoinGecko has also appointed an EU representative.
- **Wikimedia Foundation (USA):** no DPF certification known or stated and no other safeguards; the basis is your explicit consent after being informed of the risks, Art. 49(1)(a) GDPR (sections 5 and 7).
- {{MAILBOX_TRANSFER}}

You can view a copy of the safeguards mentioned (for example the Standard Contractual Clauses) via the providers' pages linked above; if you have questions, write to the address in section 1. The European Commission's Standard Contractual Clauses are at https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj

## 12. Retention periods at a glance

- **Access log on our server:** time, method, path, status and size only, no IP address; limited by automatic log rotation (3 files of 10 MB each); depending on traffic up to several months, at the latest until overwritten. The same rotation applies to the web server's error log and to the log of the tunnel connector.
- **Cloudflare cookie `cf_clearance`:** in your browser for up to about one year; you can delete it at any time.
- **Logs at Cloudflare:** no fixed period published; only as long as necessary, then deleted or anonymised (see its privacy policy).
- **Portfolio, reset point:** in your browser until you delete them. They are not on our server.
- **Privacy choices (`finplanr-consent`):** in your browser until you withdraw both consents or delete the site data.
- **Online search, charts and external images:** not stored by us. At the providers under their rules (Wikimedia: generally 90 days; TradingView: IP short-term; CoinGecko: as needed). No cookies of these providers are stored in your browser (sections 7 and 10).
- **Emails:** until your request is resolved, then deleted unless a statutory retention duty applies.

## 13. Obligation to provide data

Finplanr can be used without providing personal data. There is no statutory or contractual obligation to provide it.

On every page view, connection data such as your IP address must be transmitted for technical reasons, otherwise the page cannot be delivered. For the chart, the online search and external logos: if you do not use the function or do not give your consent, no connections to the third-party providers arise. The only consequence is that the chart or the online search results are not shown. If you write to us, we need your email address in order to reply.

## 14. External links

Finplanr contains links to external sites, for example product pages of fund issuers, Deutsche Börse, CoinGecko, TradingView and the file pages of Wikimedia Commons, and the Impressum at {{IMPRESSUM_PROVIDER}}. They open only when you click them, in a new tab. When you open one you leave Finplanr; the provider of the target page then receives your IP address and browser details (Finplanr sends no referrer with them; the exception is the attribution "Track all markets on TradingView" below the chart, which is part of the TradingView widget and may state "finplanr.net" as the origin). The respective provider is responsible for the processing of personal data there, under its own privacy information.

## 15. Your rights

Under the GDPR you have the following rights, where the respective conditions are met:

- access to your personal data (Art. 15 GDPR)
- rectification of inaccurate data (Art. 16 GDPR)
- erasure (Art. 17 GDPR)
- restriction of processing (Art. 18 GDPR)
- data portability (Art. 20 GDPR)
- **objection** to processing based on Art. 6(1)(f) GDPR, on grounds relating to your particular situation (Art. 21 GDPR)
- **withdrawal** of consent at any time with effect for the future (Art. 7(3) GDPR). You can withdraw each consent (charts, online search) separately in "Privacy settings" in the app footer; the withdrawal takes effect immediately in all open tabs of the same browser.

To exercise your rights, write to the address in section 1. Please note that we do not store portfolios of yours; you can view, export and delete your portfolio in your browser yourself (section 4). Providers that received data after your consent (section 11) are responsible for their own processing; please contact them for access or deletion there.

**Right to lodge a complaint:** You have the right to lodge a complaint with a data protection supervisory authority (Art. 77 GDPR), in particular in the Member State of your habitual residence, place of work or the place of the alleged infringement. The competent authority is generally the one in your place of residence or in the place where the controller is based; you can find the supervisory authorities of the Member States at https://www.edpb.europa.eu/about-edpb/about-edpb/members_en.

## 16. No automated decision-making

Finplanr calculates savings amounts and weights from the inputs you choose, directly in your browser. There is no automated decision-making including profiling within the meaning of Art. 22 GDPR.

## 17. Changes to this privacy policy

We adapt this privacy policy when Finplanr's functions, the service providers used or the legal requirements change. The current version is at https://finplanr.net/en/datenschutz.html (see the date above). It is also reachable via the "Privacy policy" link in the app footer.
