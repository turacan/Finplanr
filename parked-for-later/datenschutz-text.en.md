# Privacy Policy for Finplanr

**Last updated: 14 October 2026**

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
- when you load a TradingView price chart (section 6, only with your consent),
- when you use the optional online search (section 7),
- when you choose a logo or image from an external provider (section 8),
- when you contact us by email (section 9).

On a normal page view without these actions, no data is sent to any third party other than Cloudflare (section 3). Scripts and the logos of the default entries are delivered from our own server.

## 3. Providing the website, hosting, Cloudflare and server logs

The website is served from a privately operated server of the operator, running an Nginx web server in a Docker container. The server is not directly reachable from the internet, only through a Cloudflare Tunnel.

We use Cloudflare for DNS, the encrypted HTTPS connection, forwarding requests to our server (Cloudflare Tunnel) and technical security functions. Your requests therefore pass through Cloudflare's servers. Cloudflare technically decrypts the connection in order to forward it to our server.

**Provider:** Cloudflare, Inc., 101 Townsend St., San Francisco, CA 94107, USA, and affiliated companies (including in the EU).

**Data processed:** Each request involves in particular:

- IP address
- date and time of access
- page or file requested and HTTP status code
- amount of data transferred
- referrer (the page you came from), if your browser sends it
- browser type, browser version and operating system (user agent)
- technical connection and security data used to detect and block abusive access

**Server logs on our server:** The web server writes an access log containing the data above. Under the current configuration, Cloudflare passes the visitor's IP address to our server in a header (X-Forwarded-For), so it can appear in the access log. We do not systematically evaluate the logs, do not combine them with other data and do not create user profiles. They are used only for troubleshooting and to investigate attacks.

**Purpose and legal basis:** The processing serves to provide the website securely, stably and functionally and to defend against attacks. The legal basis is Art. 6(1)(f) GDPR (legitimate interest in the secure and reliable operation of the website).

**Role of Cloudflare:** Where Cloudflare processes data on our behalf (in particular the traffic logs), it acts as a processor under Art. 28 GDPR. A data processing agreement (Data Processing Addendum, DPA) with Cloudflare is in place; according to Cloudflare it incorporates the EU Standard Contractual Clauses. For some data Cloudflare states that it is itself a controller; details are in Cloudflare's privacy policy: https://www.cloudflare.com/privacypolicy/

**Retention:** The logs on our server are rotated automatically by size by Docker (at most three files of 10 MB each); older entries are overwritten. Depending on traffic, the logs are generally kept for a few days to a few weeks, at the latest until they are overwritten by log rotation. Cloudflare's privacy policy gives no fixed period for traffic logs; data is kept there only as long as needed for the services and legal obligations and then deleted or anonymised. See Cloudflare's privacy policy linked above.

**Third-country transfer:** Cloudflare also processes data in the USA. Cloudflare, Inc. states that it is certified under the EU-US Data Privacy Framework (adequacy decision of the European Commission of 10 July 2023) and otherwise relies on the EU Standard Contractual Clauses. More in section 11.

## 4. Local storage in your browser, export and import

Finplanr saves your settings in your browser's local storage so that they are there the next time you visit. This data does not leave your browser and is not transmitted to us.

The following entries are created:

- `mein-sparplan-portfolio-v1`: your portfolio, i.e. monthly savings budget, categories and positions, weights and amounts, names, tickers, ISIN, WKN, colours, symbols, logos (including images you upload yourself), locked weights, sort order and display settings
- `mein-sparplan-reset-stand-v1`: a personal reset point that you saved
- `finplanr-lang`: your language setting (German or English)
- `finplanr-consent-tv`: an entry recording your consent for the TradingView chart, with the time (section 5)

Finplanr itself sets no cookies.

**Legal basis:** Storing and reading this data is covered by section 25(2) no. 2 TDDDG (Telecommunications Digital Services Data Protection Act), because it is strictly necessary for the function you explicitly requested (planning and restoring your portfolio). No consent is needed for it. Where personal data is processed in the process, the legal basis is Art. 6(1)(b) GDPR (providing the function you use) and, alternatively, Art. 6(1)(f) GDPR (legitimate interest in making the application usable).

**Retention and deletion:** The data stays in your browser until you delete it. You can remove it at any time: with the app's reset functions (for example "Factory reset") or by deleting the site data for finplanr.net in your browser settings. Switching browser or device does not transfer the data automatically.

**Export and import:** Finplanr can export your portfolio as a JSON file and the current plan as a CSV table, and can import a JSON backup. These files are created and read entirely in your browser. They are saved to or read from your device and are not transmitted to us or anyone else. You are responsible for keeping these files safe.

## 5. Privacy settings and consent {#consent}

There is only one function in Finplanr for which we ask for your consent: loading the TradingView chart (section 6). There is no consent banner on page load, because nothing that requires consent is loaded on page load.

- The chart panel first shows you a notice about which data is sent to TradingView and that TradingView is based in the USA. Only when you click **"Load chart"** (or choose "Allow charts" in the "Privacy settings") is the TradingView widget loaded. This is your explicit consent (Art. 6(1)(a) GDPR, section 25(1) TDDDG, and for the transfer to the USA additionally Art. 49(1)(a) GDPR).
- Your decision is recorded as the entry `finplanr-consent-tv` (with the time of consent) in your browser's local storage so that you are not asked again for every chart. This entry is technically necessary to remember your choice (section 25(2) no. 2 TDDDG).
- **Withdrawal:** You can withdraw your consent at any time with effect for the future, via the **"Privacy settings"** link in the app footer (button "Withdraw consent"). After that open charts are closed and TradingView is no longer loaded until you consent again. Data that TradingView has already stored in your browser is not deleted by this; you can remove it in your browser settings under the site data for tradingview-widget.com. The lawfulness of processing before withdrawal is not affected (Art. 7(3) GDPR).
- Consent is voluntary. Without it, the whole app keeps working, just without the embedded chart.

## 6. Price charts from TradingView

When you click the name of a position in the app, a price chart panel opens below it. For this we embed TradingView's "Advanced Chart" widget. Nothing is loaded from TradingView without your consent (section 5).

**Provider:** TradingView.com, Inc., 1330 Avenue of the Americas, 23rd Floor, New York, NY 10019, USA. According to its privacy policy TradingView has appointed a representative in the EU under Art. 27 GDPR in Barcelona (Spain). Privacy policy: https://www.tradingview.com/privacy-policy/

**Data processed:** After you click "Load chart", your browser connects to TradingView (including s3.tradingview.com and other TradingView servers). In particular the following is transmitted:

- your IP address and technical connection data (such as browser and operating system),
- the address of the embedding page (for us, the address of finplanr.net),
- the widget type and the displayed symbol. The symbol is derived from the ticker you entered, for example "XETR:VWCE". Amounts, weights and the rest of your portfolio are not transmitted.

According to TradingView, the widget sets no cookies. It may, however, store data in your browser's local storage under the domain tradingview-widget.com. TradingView also states in its privacy policy that analytics data (for example with Google Analytics) may be collected through its widgets. We have no influence over this processing. TradingView's widget FAQ: https://www.tradingview.com/widget-docs/faq/general/

**Purpose:** Showing a price chart for the security or coin you selected.

**Legal basis:** Your consent, Art. 6(1)(a) GDPR and section 25(1) TDDDG (storing and reading information on your device by the widget). You can withdraw it at any time as described in section 5.

**Retention:** Nothing is stored on our side for this except your consent entry. TradingView states that for the widget the IP address is not stored together with identifiable data and is retained only short-term. Data in local storage under tradingview-widget.com remains until you delete it in your browser settings. See TradingView's privacy policy for more.

**Third-country transfer:** The data goes to TradingView in the USA. TradingView's privacy policy names no specific transfer mechanism. We therefore rely on your explicit consent (Art. 49(1)(a) GDPR). We inform you here and in the notice before loading (provider based in the USA): the level of data protection in the USA may differ from that in the EU, and US authorities may under certain circumstances access data. If you do not want this, do not click "Load chart".

**Attribution:** Below the chart TradingView shows the note "Track all markets on TradingView". It is part of the widget and shown unchanged.

## 7. Optional online search (CoinGecko, Wikidata, Wikimedia Commons)

In edit mode you can use an optional online search for a position to find stocks, ETFs and cryptocurrencies, identifiers (ISIN, WKN, ticker) and suitable images. In the search dialog you choose the source ("Stocks & ETFs" or "Crypto"); it defaults to the category type and you can switch it at any time. The request is only sent when you click "Search" in the search dialog or press Enter. The dialog first tells you that your search term and IP address are sent to the respective provider and links to this privacy policy. Without this action there is no connection.

The following services may be queried:

- **CoinGecko** (api.coingecko.com), search for cryptocurrencies. Provider: Gecko Labs Pte. Ltd., Singapore (EU representative under Art. 27 GDPR: Euverify Ltd, Cork, Ireland). Privacy: https://www.coingecko.com/en/privacy
- **Wikidata** (www.wikidata.org and its query service query.wikidata.org), search for security and company data (source "Stocks & ETFs"; the query service only receives the identifiers of the Wikidata entries found, not your search term), and **Wikimedia Commons** (commons.wikimedia.org), image search. Provider of both services: Wikimedia Foundation, Inc., USA. Privacy: https://foundation.wikimedia.org/wiki/Policy:Privacy_policy

**Data processed:** Your browser sends your search term and the technically necessary data directly to the respective provider: your IP address, browser and operating system details, and the address of our website (only the main part, "https://finplanr.net/", as the referrer). Our server neither sees nor stores your search term. The result lists may contain preview images (for example coin logos from coin-images.coingecko.com or images from upload.wikimedia.org), which your browser also loads directly from there.

**Purpose:** Running the search function you requested and showing the results.

**Legal basis:** Art. 6(1)(b) GDPR, because the transmission is needed to provide the function you explicitly requested. Alternatively Art. 6(1)(f) GDPR: our legitimate interest is offering you this optional function. Your interests do not override it because you trigger the function yourself, it involves only the search term and technically necessary connection data, and we link no other data and build no profiles. No information is stored on or read from your device that would require consent under section 25 TDDDG.

**Retention:** We do not store your search requests. The providers keep connection data under their own rules; for example the Wikimedia Foundation states that most personal data is deleted, aggregated or de-identified after 90 days. CoinGecko keeps data as long as needed for its purposes and legal obligations.

**Third-country transfer:** CoinGecko is based in Singapore and the Wikimedia Foundation in the USA. There is no European Commission adequacy decision for Singapore. The Wikimedia Foundation's privacy policy names no certification under the EU-US Data Privacy Framework. The connections only arise through your action, after the dialog has pointed out the transmission. That Singapore and the USA are outside the EU is stated here. Where the connection amounts to a transfer to a third country without an adequacy decision, we rely on Art. 49(1)(b) GDPR (necessary for the service you requested) and, where you decide to search after the notice in the dialog, on Art. 49(1)(a) GDPR (explicit consent after being informed of the risks).

**Consequences:** If you do not use the search, these connections do not occur. The app is fully usable without the search (you can enter identifiers and names by hand).

## 8. Logos and external images

The logos of the default entries (6 cryptocurrencies and 11 fund issuers) and the app's symbols are delivered from our own server. A normal visit to Finplanr loads **no** logos from third parties.

A connection to a third party arises only if you yourself pick an external image source:

- an **image address (URL)** that you enter (the provider is then the operator of the server behind that address),
- an **image from Wikimedia Commons** that you pick in the image picker (upload.wikimedia.org, Wikimedia Foundation, Inc., USA),
- the **logo returned by CoinGecko** for a cryptocurrency you add via the search (coin-images.coingecko.com or assets.coingecko.com, Gecko Labs Pte. Ltd., Singapore).

This address is then stored in your local settings (section 4), and your browser loads the image from the respective provider again on every later visit ("hotlinking"). The provider sees your IP address, your browser details and the address of our website (referrer, main part only), and can infer from this that you use Finplanr. This applies to any site you enter there.

**How to avoid this:** Use symbols, an image you upload yourself (stored as data in your browser and not transmitted anywhere) or the bundled logos. To remove an external logo you already set, use "Use default logo" in edit mode.

**Legal basis:** Art. 6(1)(b) GDPR (the presentation of your portfolio that you chose) and, alternatively, Art. 6(1)(f) GDPR (legitimate interest in letting you make the customisation you want; you make the selection yourself).

**Retention and third-country transfer:** The providers' own rules apply (section 7 or their privacy policies). Wikimedia Commons and CoinGecko are treated as in section 7. For freely entered addresses you decide which server you contact.

## 9. Contact by email

If you email us at {{EMAIL}}, we process the data you send: your email address, your name (if given), the content of your message and technical delivery information.

**Technical flow:** {{EMAIL}} is a forwarding address through Cloudflare Email Routing (Cloudflare, Inc., USA, as processor). Cloudflare forwards the message to the operator's private mailbox. The provider of that mailbox is: {{MAILBOX_PROVIDER}}. Replies are sent from the same mailbox.

The contact form linked in the legal notice is operated by the provider of the Impressum page ({{IMPRESSUM_PROVIDER}}) and passes your message on to us. Its data processing is governed by the privacy information on that page.

**Purpose and legal basis:** Handling and answering your enquiry. The legal basis is Art. 6(1)(f) GDPR (legitimate interest in answering enquiries) or Art. 6(1)(b) GDPR if your enquiry relates to a service from us.

**Retention:** As long as needed to handle your request. After that we delete the correspondence unless statutory retention duties require longer storage.

**Obligation to provide data:** You are not obliged to write to us. Without your email address we cannot reply, however. **Third-country transfer:** see section 11 (Cloudflare).

## 10. Cookies and similar technologies

Finplanr itself sets no cookies. There are no advertising, marketing or analytics cookies and no analytics services.

Your settings are stored in your browser's local storage (section 4). After your consent, the TradingView widget writes data to local storage under tradingview-widget.com (section 6).

When its protection features are enabled, Cloudflare may set technically necessary cookies (for example for bot detection, such as `__cf_bm` or `cf_clearance`). These serve solely security and operation (section 25(2) no. 2 TDDDG). More: https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/

**Google AdSense, Google Analytics and other advertising or analytics services are not integrated.** If advertising or additional services are added in future, this privacy policy will be updated before activation and, where required, your consent obtained beforehand.

## 11. Recipients and transfers to third countries

Depending on your use, personal data goes to:

- **Cloudflare, Inc.** (USA, with companies in the EU): hosting infrastructure, forwarding, security, email forwarding (processor, sections 3 and 9)
- **TradingView.com, Inc.** (USA): only after your consent, section 6
- **Gecko Labs Pte. Ltd. / CoinGecko** (Singapore): only when you use the crypto search or use a CoinGecko logo, sections 7 and 8
- **Wikimedia Foundation, Inc.** (USA): only when you use the Wikidata/Commons search or use a Commons image, sections 7 and 8
- {{MAILBOX_RECIPIENT}}
- the provider of the Impressum page ({{IMPRESSUM_PROVIDER}}): when you use the contact form on that page
- **image servers you enter yourself**: when you enter an external image address, section 8

There are no other recipients. Data is not shared for advertising purposes.

**Third-country transfers and safeguards (Art. 13(1)(f) GDPR):**

- **Cloudflare, Inc. (USA):** Cloudflare states that it is certified under the EU-US Data Privacy Framework (DPF). For transfers to certified US companies, the European Commission found an adequate level of protection by decision of 10 July 2023 (Art. 45 GDPR). If the certification lapses, Cloudflare states that the EU Standard Contractual Clauses apply (Art. 46(2)(c) GDPR), which are part of the data processing agreement. Information: https://www.cloudflare.com/trust-hub/gdpr/
- **TradingView (USA):** its privacy policy names no transfer mechanism; the basis is your explicit consent, Art. 49(1)(a) GDPR (section 6).
- **CoinGecko (Singapore):** no adequacy decision; basis Art. 49(1)(b) or (a) GDPR (section 7). CoinGecko has also appointed an EU representative.
- **Wikimedia Foundation (USA):** no DPF certification known or stated; basis Art. 49(1)(b) or (a) GDPR (section 7).
- {{MAILBOX_TRANSFER}}

You can view a copy of the safeguards mentioned (for example the Standard Contractual Clauses) via the providers' pages linked above; if you have questions, write to the address in section 1. The European Commission's Standard Contractual Clauses are at https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj

## 12. Retention periods at a glance

- **Server logs on our server:** limited by automatic log rotation (3 files of 10 MB each); generally a few days to a few weeks, at the latest until overwritten.
- **Logs at Cloudflare:** no fixed period published; only as long as necessary, then deleted or anonymised (see its privacy policy).
- **Portfolio, reset point, language setting:** in your browser until you delete them. They are not on our server.
- **Consent entry (TradingView):** in your browser until you withdraw or delete the site data.
- **Online search and external images:** not stored by us. At the providers under their rules (Wikimedia: generally 90 days; TradingView: IP short-term; CoinGecko: as needed).
- **Emails:** until your request is resolved, then deleted unless a statutory retention duty applies.

## 13. Obligation to provide data

Finplanr can be used without providing personal data. There is no statutory or contractual obligation to provide it.

On every page view, connection data such as your IP address must be transmitted for technical reasons, otherwise the page cannot be delivered. For the chart, online search and external logos: if you do not use the function or do not give your consent, no connections to the third-party providers arise. The only consequence is that the chart or search results are not shown. If you write to us, we need your email address in order to reply.

## 14. External links

Finplanr contains links to external sites, for example product pages of fund issuers, Deutsche Börse, justETF, Finanzfluss, CoinGecko and TradingView, and the Impressum at {{IMPRESSUM_PROVIDER}}. They open only when you click them, in a new tab. When you open one you leave Finplanr. The respective provider is responsible for the processing of personal data there, under its own privacy information.

## 15. Your rights

Under the GDPR you have the following rights, where the respective conditions are met:

- access to your personal data (Art. 15 GDPR)
- rectification of inaccurate data (Art. 16 GDPR)
- erasure (Art. 17 GDPR)
- restriction of processing (Art. 18 GDPR)
- data portability (Art. 20 GDPR)
- **objection** to processing based on Art. 6(1)(f) GDPR, on grounds relating to your particular situation (Art. 21 GDPR)
- **withdrawal** of consent at any time with effect for the future (Art. 7(3) GDPR). You withdraw the TradingView consent via "Privacy settings" in the app footer.

To exercise your rights, write to the address in section 1. Please note that we do not store portfolios of yours; you can view, export and delete your portfolio in your browser yourself (section 4).

**Right to lodge a complaint:** You have the right to lodge a complaint with a data protection supervisory authority (Art. 77 GDPR), in particular in the Member State of your habitual residence, place of work or the place of the alleged infringement. The competent authority is generally the one in your place of residence or in the place where the controller is based; you can find the supervisory authorities of the Member States at https://www.edpb.europa.eu/about-edpb/about-edpb/members_en.

## 16. No automated decision-making

Finplanr calculates savings amounts and weights from the inputs you choose, directly in your browser. There is no automated decision-making including profiling within the meaning of Art. 22 GDPR.

## 17. Changes to this privacy policy

We adapt this privacy policy when Finplanr's functions, the service providers used or the legal requirements change. The current version is at https://finplanr.net/en/datenschutz.html (see the date above). It is also reachable via the "Privacy policy" link in the app footer.
