# Going to market: get found, get trusted, get heard

> The companion to [`PLAYBOOK.md`](PLAYBOOK.md) for the part after "it works": a landing page search can read,
> store listings that stay true, store search, screenshots, ratings, attribution, positioning and feedback. Most
> rules here were paid for by a live consumer app on iOS, Android and the web, and the date is when the lesson
> landed. Where a rule is a reviewed design that has not yet been through a store's review, it says so. Stack-agnostic,
> with React Native and Expo where an example needs a name.
>
> **Tags use the playbook's brackets but mark a go-to-market stage, not team size:** `[0]` from the first public web
> page, `[1]` from the first store release, `[2]` once you are spending money or effort on growth. Each rule has its
> **why**, and a **trap** where there was one. Store rules change, so each policy claim names its source: re-read it
> before you rely on it.

---

## 0. The order `[0]`

- **Proof before promotion.** Make the product findable and honest (sections 1 to 4) before you ask anyone to look.
  Posting about an app whose store page is wrong burns the attention you worked for.
- **Measure before you move.** Every change to a listing gets a baseline the same day (section 3) and a channel label
  (section 6), or you will never know whether it worked.
- **The store page is a contract with every reader and every reviewer.** Keep it in the repo and gate it like code.
  The console is where you paste, never where the copy lives.
- **The discipline of stopping applies here more than anywhere.** Store search moves for weeks after a change. Judge
  from data, never from the day after.

---

## 1. A front door search engines can read `[0]`

- **The root URL ships as real HTML, even when the app is a single-page app.** *Why:* an SPA root is an empty
  `<div>` to anything that runs no JavaScript. For four months a search for the app's own name found other apps, and
  crawlers saw the head tags and nothing else (found 2026-10-08). *What worked:* render the landing at build time from
  the app's own string catalogue and write it into the exported HTML, outside the app's mount node. *Traps:* whole-app
  static prerender crashed on a module that touched `window`. Bot-only prerender is cloaking. Static copy inside the
  mount node gets replaced on mount, so the page visibly jumps.
- **Patch the file that ships, and gate the patch.** A post-build script injects head tags, meta and the landing into
  the exported `index.html`, and CI greps the export for each one. *Why:* the framework's custom head file is ignored
  in SPA output mode, so every social tag in it was inert (2026-06-27). *Trap:* under `bash -e` only the last command
  in an `&&` chain fails the step, so write one assertion per line.
- **Pick the page before first paint.** One inline `<head>` script sets a class on `<html>`: a fresh visitor at `/`
  gets the landing, and everyone else gets the app. It can also stamp the platform, so the page shows one action per
  device (that phone's store badge, or "Begin" on a laptop). *Traps:* the script is inlined, so it can have no imports
  or module constants, and a test must hold its literals equal to the app's. If storage is unreadable, send the
  visitor to the app.
- **Test the boot that ships, not its source.** CI pulls the inline script out of the export and runs it against fake
  phones, tablets, laptops, returning visitors and blocked storage. A grep proved nothing, because the stylesheet
  contains the same strings whether or not the boot sets them (2026-10-18).
- **Make the landing the default when no script runs.** Show it under `html:not(.app)`, so it appears and scrolls with
  JavaScript off, rather than under a `.landing` class that only JavaScript can add. Strip the template's bare "enable
  JavaScript" line too.
- **If the landing and the app share one HTML file, hide the landing when the root screen loses focus, not when it
  unmounts.** Stack routers keep `/` mounted under pushed screens, so an unmount cleanup never ran and the landing sat
  over the app. Re-read the first-run flag on every focus, or Back from a finished welcome shows the sales page again.
- **Privacy, terms and support are static files at their own URLs.** *Why:* the policy URL returned a 2 KB app shell
  to a non-JavaScript fetch, which is how a store's policy check reads it (2026-06-24).
- **Clean-URL redirects make deploy checks lie.** The host 308-redirects `/privacy.html` to `/privacy`, so a `curl`
  without `-L` read nothing and a "did it deploy" check said no. Check the clean URL for a known string, and confirm
  the deploy run. *Trap:* a `/privacy -> /privacy.html` rewrite on a clean-URL host loops.
- **robots.txt names the sitemap by its full URL.** The sitemap lists only the public pages. The shell's canonical is
  the root, so app routes that serve the same HTML never compete with the landing.
- **Structured data says only what is true.** Use `WebSite` with the name and an `alternateName`. Skip
  `SoftwareApplication`, which wants a rating you may not have. Escape `<` as `\u003c` inside the JSON, so a
  `</script>` in any value cannot close the tag.
- **The title names the audience, and the description puts the audience and the promise in its first 115 or so
  characters,** because phone results cut it off near 120. Ship a 1200x630 social image and re-check it in a sharing
  debugger after deploy.
- **Search Console: a Domain property, a TXT record you never delete, the full sitemap URL.** *Traps:* the automatic
  "verify through your domain provider" route failed silently, and the record went in by hand. A Domain property
  rejects a bare `sitemap.xml`. The TXT record sits beside the email SPF record, and both must stay. Mark it NEVER
  DELETE in your resource table (2026-10-18).
- **Every third-party request on the page is a disclosure.** A font `@import` from a font CDN sends every visitor's IP
  address to that CDN, which the privacy policy must then name, and a German court awarded damages against a site for
  exactly this in 2022. Self-host fonts, and fail CI if the export calls a font CDN.
- **Keep one cookieless analytics for the page, named in the privacy policy in the same change.** Record which layer
  injects it (here it came from the DNS zone, not the hosting project's switch). The app's own telemetry cannot see a
  landing page at all.
- **Collect an email only for something you will send.** A complete mailing list was built and removed the same day
  (2026-10-18), because a list with nothing to send is a legal duty with no use. Write the rule down so nobody
  rebuilds it.
- **Anything crawlable is permanent, so check every claim against the code before it ships.** A truth pass on a
  landing redesign checked 127 claims and found 37 wrong, and its skeptics found about 25 more (2026-10-18). A founder
  story is a claim too: naming a small group you know (a team you managed, a workplace) next to a health condition
  discloses their health, so name a wide group or none.

---

## 2. Store listings as code `[1]`

- **One repo file per store field. The console is a paste target.** *Why:* a live localised listing turned out to
  exist in no repo file, so no check had ever read it (2026-10-19). Put a "do not paste" banner on retired docs.
- **Read the live store, in more than one country, before any rewrite,** and write the live values and the date into
  the source file. An agreed rewrite can sit unpasted for months while the docs say it shipped. Some values live only
  in the console (the primary language, the live keyword field), so read and record them first.
- **A listing gate runs in CI.** It fails on: measured caps (bytes for keyword fields, and any count the doc records
  must match), any price pattern in any language, features named on the wrong store (an Android-only widget on the App
  Store, a web-only button anywhere), another payment method or trial wording on Google Play, unearned accessibility
  claims ("accessible", "WCAG"), claims the code disproved (banned by name), protected lines that must stay (privacy
  and terms URLs, medical sentences, a free-forever promise), and typography (diacritics present, French no-break
  spaces). *Why:* copy that no check reads drifts. A price, a privacy claim or a feature line goes stale the day the
  code changes, and nobody notices until a reader or a reviewer does. *Trap:* ban the family of a phrase with a pattern
  per language, not one wording of it.
- **Break-test the gate after every change to it.** A script copies the sources, breaks one rule at a time, and passes
  only when the gate fails for that reason. *Why:* three rules had always passed, one because a bare number elsewhere
  in the text satisfied it, and an older gate let 15 of 16 probes through in one group (2026-10-19). It proves the
  gate, not the copy, so it runs with gate edits rather than in CI.
- **Re-check every privacy line in a listing whenever you add an SDK.** A billing or analytics SDK that starts at
  launch can make "no third-party trackers" false overnight.
- **Paste by print and diff, never by retyping.** A hand-retyped Italian listing went live with a typo. *Trap:*
  non-English copy was once silently stripped of its accents, most likely by a shell heredoc on a non-UTF-8 codepage.
  Write translations with a UTF-8 tool, and make the gate fail when a translation has no accented characters at all.
- **Release notes: one What's New per App Store localisation, one tagged box on Play.** App Store localisations do not
  inherit What's New, promotional text, keywords or the privacy URL, and a new one starts empty. Play takes one box
  with a tag per locale and at most 500 characters each. *Trap:* French ran a fifth to a third longer, so keep the Play
  English near 375 characters (at one release, 390 of English became 477 of French). Paste one neutral Spanish text
  under both Spanish tags.
- **On Google Play, the store sells and the store sets the price, and the listing counts as a payment surface.** Show
  prices only from the store's own localised price string. Never lead an Android user to another payment method, in
  the app or the listing, unless you have enrolled in one of Google's alternative billing or external links programs
  for that country. Use trial wording only for a real Play trial. *Why:* Play rejects an update that shows a reviewer
  abroad a fixed home-currency price, and a link out to web checkout breaks the same Payments policy, so sweep the
  app and the listing for both. *Traps:* Google's own violation examples include a subscription named "Free
  Trial", or "Try Premium membership - 3 days for free", that carries an auto-recurring charge. A fixed "save N%" is
  false in countries where the store rounds prices differently. On iOS
  the same house rule is worth keeping by choice: your own price appears only where no store sells.
- **A health-adjacent app carries three not-a-medical-device sentences in every language, pinned word for word:** it
  is not a medical device, it does not diagnose, treat, cure or prevent any condition and is no substitute for
  professional care, and medical advice comes from a health professional. Ban clinical nouns in every field
  (treatment, therapy, symptom). *Trap:* the first gate pinned only two of the three.
- **Privacy declarations come from the code, and are read back from the console every submission.** A usage counter is
  easy to add in code and forget in the console, and a label that misses it is a false statement to every reader.
  Apple counts data as collected when you or a partner keep it longer than it takes to answer the request, and as
  linked when it is tied to an account or device. Read it conservatively: we treat a photo that reaches an AI provider
  that keeps inputs, in a request tied to an account, as collected and linked, even though we store nothing. Declare a new collection before the build that introduces it ships.
- **Consoles move their menus.** Read the console's own help, confirm the path in the console, and record it "as of
  <month>". Help pages lag the console too.

---

## 3. Being found in store search `[1]`

- **Put the category in the App Store name: `Brand: Category`.** The name is the heaviest ranking field. *Why:* the
  bare brand spent 10 of 30 characters on a word nobody searched. A first baseline six days after the rename already
  had the app inside the top 50 for its category phrase in three English storefronts (2026-10-25). There was no
  earlier baseline and the four-week rerun is still to come, so read that as a sign, not a result. The home-screen
  label comes from the build config, so the icon stays clean. Pre-decide a softer fallback name in case review
  objects.
- **The subtitle carries the promise nobody else makes,** plus the one category word the name lacks. Re-run the
  no-repeat check after any subtitle edit. When a competitor starts using your word, it stops being yours.
- **Keyword field: at most 100 bytes, commas, no spaces, singular forms, never a word already in the name or
  subtitle.** Apple names the app name, subtitle, keywords, category and company name as searched, and the description
  is not among them. That words combine across fields within a localisation is ASO observation, not Apple's
  statement. Gate the field in CI, and keep the old live value as your baseline.
- **A second keyword set can come from a second localisation.** Apple's localisation table lists English (U.K.) in
  every storefront except the United States, Canada and Japan, and ASO practice (not Apple) holds that each listed
  localisation's keywords are searched there. So an English (Australia) primary can carry a second set of new words in
  English (U.K.), while a US-primary app gets its second US set from Spanish (Mexico). Unproven for the source app so
  far. *Trap:* every localisation has its own What's New and privacy URL to fill every release.
- **Rank only for people you will keep.** A word that brings the wrong installs costs you reviews, so leave out words
  like "habit" and "streak" that would rank a no-streaks app for streak trackers. No competitor names (Apple 2.3.7),
  no clinical words, no bare word that is also a big brand's name.
- **Each language gets a native name and keyword set, measured per storefront.** Never pad one language's field with
  English to rank somewhere else.
- **Google says Play ranks on ratings, reviews, downloads and user behaviour, while the listing text helps people find
  you.** Once the title and short description name the category, stop rewording. For a new app, the levers are a
  well-timed rating ask (section 5) and installs.
- **Baseline search ranks the day a listing changes, rerun at about one and four weeks, and judge only from the second
  rerun.** [`scripts/store-ranks.py`](scripts/store-ranks.py) reads Apple's iTunes Search API, which Apple publishes for
  programmatic use (about 20 calls a minute), for a fixed term list and fixed countries, and appends a dated table to
  a doc. *Traps:* it is a proxy (unpersonalised, up to 200 iPhone apps), so never change the terms between runs.
  Google Play has no search API and its robots.txt disallows automated reads of its search pages, so read the
  Console's acquisition report by search term instead.

---

## 4. Screenshots and store art `[1]`

- **Generate store screenshots with a script from the real web build,** in headless Chrome, seeding state with an init
  script before any app code runs. Deterministic, and redone in any language for nothing.
- **Seeding must bypass every render gate, not just supply data.** *Why:* a first-run redirect silently turned every
  main-screen shot into the welcome screen. Set every first-run, what's-new and coachmark flag.
- **Stub the network, refuse the AI host, and never put a real session token in a public repo.**
- **Pin the clock, randomness, locale and timezone. Wait on test ids or catalogue strings, never English copy.** A
  localised run died clicking the English word on a German screen.
- **Strip what the target device does not have, and assert it is absent.** A web render shows web-only features.
- **Check every image's own size header, and throw when a crop passes the viewport.** Playwright silently trims a clip
  at the viewport edge (a file came out 3px short). iPad sizes do not divide by 3, so iPad needs scale 2.
- **Fill every slot of the same shape from one capture, as JPEG (no alpha).** A 1320x2868 capture (440x956 CSS px at
  scale 3) scales into the medium-display slot Apple marks required today. A slot of another shape, such as iPhone Duo
  (required for apps built with the iOS 27.1 SDK from April 2027), gets its own capture at its own aspect. Apple
  renames slots too (by device, not inches, by October 2026), so read which slot is marked required at every
  submission. Upload iPad shots only if the app supports iPad.
- **Captions are data, gated before the browser starts** (no dash, exclamation, digit, price or other platform), and a
  line that wraps fails the run.
- **The first three slides carry the pitch: the promise, the stuck moment, the payoff.** No title art (2.3.3), no
  paywall that shows another way to pay, no generic phone bezel.
- **A new screen adds its slide to every set in the same commit,** with one generator that has modes. A screen shipped
  in August was missing from every listing two weeks later.
- **The harness doubles as a reachability check.** When a script cannot walk to a screen, find out why. Sometimes the
  harness lacks a stub, and sometimes a person cannot get there either.
- **App Store header and search images (iOS 27 and later) are stills first.** The header is 21:9 at 3840x1646 and the
  search card 3:2 up to 3840x2560, opaque PNG or JPEG. Apple's spec lists `.jpeg`, `.jpg` and `.png`, but in October
  2026 the header slot refused a `.jpeg` file, so name it `.jpg`. They are reviewed under 2.3.14 and Apple's asset
  best practices (no specific prices or discounts, URLs, other platforms, Apple's own badges, or awards the app has
  not received). They ship with a version first, then alone from the Asset Library once a version is approved, and
  they carry over to the next version: check, never re-add. A generated video came back muddy and was scrapped.

---

## 5. Ratings without buying them `[0→1]`

- **Use the store's own rating card, with zero words of yours before, on or after it.** A custom "if the app is
  helping, a review helps" line was caught before shipping: it is a custom prompt, and sentiment filtering.
- **Never wire a Rate button to the review API.** Both stores cap the card silently, so the button would look broken.
  A plain link to the listing is fine if you ever want one.
- **Earn the ask by use, never by mood.** Several separate days of the core loop, the first two or more weeks ago,
  counted from the build that adds the ask. Never show the count and never reset it, so it cannot become a streak.
- **Ask at a calm pause after a genuinely good moment.** Something finished, not a hard day, nothing else on offer,
  the natural end of the loop. Never on launch or mid-flow. Each gate is a pure function with a test.
- **Cap it harder than the store does:** once per version, about 180 days apart, recorded before the call so an error
  can never loop.
- **A delayed ask re-checks when its timer fires,** with one timer and one ask in flight. A double tap once queued two.
- **Count your asks anonymously, and claim nothing you are not told.** Stores never say whether the card appeared.
- **Native review modules can crash at import, and can quietly open the store page.** Import lazily inside try/catch
  at the moment of asking, check only "is available", and never configure a store-URL fallback. Pin the exact version:
  a patch release once broke the iOS build, because CI never compiles native code.
- **Test only where the card can show.** On Android, install from Play's Internal testing track as a tester with no
  existing review. On iOS, use a development build, where StoreKit always shows the card. TestFlight never shows it.
- **Never reward a rating, and keep any feedback thank-you visibly apart from one (section 9).** Both stores forbid
  incentivised reviews, consumer law treats undisclosed rewarded reviews as misleading, and it is bought social proof.
- **Never fake social proof:** no stars, testimonials, counts, "loved by", press logos or awards you do not have, on
  the site or the listing.

---

## 6. Knowing where installs come from `[1]`

- **Tag the website's store badges by channel, never by person.** App Store: a campaign link
  (`?pt=<provider token>&ct=<campaign>&mt=8`, where the provider token is public because it is in every campaign
  link). Google Play: `utm_source`, `utm_medium` and `utm_campaign`, URL-encoded inside one `referrer`. Keep both in
  one shared constants file, and HTML-escape them where they are written into markup. *Why:* Apple credits a website
  only for Safari visitors, and Play files an untagged link under ads and referrals with no source, so the website
  cannot be told apart from any other link (2026-10-25).
- **One label for the website first.** Apple's help says a campaign appears after 24 hours and shows a metric only
  once it reaches five, so a label per post buys precision the numbers cannot show yet. Point posts at the website and
  read the referrer there. *Trap:* the console's "generate a campaign link" button saves nothing, and the campaign
  appears in the list only once it has data (2026-10-25).
- **Links that send existing users stay untagged** (an update prompt, a rate-us link), or they read as acquisition.
  Hold it in a test.

---

## 7. One name, one face `[1]`

- **Use the same developer name on both stores.** Readers decide trust in a second, and two names read as two
  companies.
- **A trading name you have not registered cannot stand where an owner's name goes** (seller, copyright, terms). An
  individual Apple account always shows the person's legal name, so until you incorporate, your own name is the only
  one both stores can share.
- **The public developer email is account-wide, and support emails are per app.** On Play the developer email shows
  on every app you will ever publish, so it belongs to the person or the studio, while each app's own support address
  goes in that app's store settings.

---

## 8. Positioning against the field `[2]`

- **Map the lanes before the rivals.** List the few approaches the category splits into (in a planner category: visual
  timeline, coach, game or pet, AI breakdown, plain list) and the cost of each. Your position is a lane, not a
  feature list.
- **Research from primary sources, and say what is unconfirmed.** Store pages and their lookup APIs, the stores'
  recent-review feeds per country, the rivals' public feedback boards and roadmaps, and their own help pages. Dated,
  sourced, and marked "unconfirmed" when it is.
- **Lead with a claim a reviewer can check in seconds, that the apps people actually use cannot make.** "Calm" and "no
  guilt" stopped being differentiators once the category leader and several newer apps said them. A structural fact
  ("nothing is ever overdue") can be checked.
- **Use their users' top requests honestly.** List the most-voted requests you already answer and, beside them, the
  big ones you do not. A one-sided list reads as cherry-picked to anyone who opens the board.
- **Write "where we lose" with a "do" for each,** including revenue, and a "never lead with" list of things that are
  true but anyone can say.
- **Then fact-check and red-team it before you trust it.** The first headline failed the moment a reviewer opened the
  leader's list view, and three of the product's own claims went further than the code (2026-10-25). Keep rivals'
  prices out of anything public.
- **Say it at three lengths:** a bio, one breath, thirty seconds. The thirty-second version names the trade-off you
  chose on purpose, which is the part a hiring manager or an investor listens for.

---

## 9. Hearing from users `[1→2]`

> A reviewed design (2026-10-25), not yet built or through either store's review. Re-read the cited rules first.

- **A feedback channel ships before you announce** (the playbook's Day-0 list), and it stays one tap from Settings.
- **Thank people for feedback, never pay for a review, a rating or a contest win.** Both stores' words need reading
  closely. Apple's section 3 introduction warns against attempts to "manipulate reviews, inflate your chart rankings
  with paid, incentivized, filtered, or fake feedback", and its 3.2.2(x) bars forcing people to rate, review or take
  other store actions, then says apps "may otherwise incentivize users to take specific actions within apps".
  Google's policy summary says it "includes incentivizing feedback", inside a policy about store ratings and reviews
  whose full text speaks of incentivized reviews and ratings. Both sentences are about store ratings and rankings, so
  this design's reading is that a private in-app note, rewarded with no link to the store, sits outside both. That
  reading is not yet tested in review. Keep the gift visibly apart from any store action. A contest tells most entrants every month that their note lost, which drives
  away the people whose feedback you wanted.
- **On iOS, unlock any gift through the account on your server, never through a code box of your own** (the 3.1.1
  rejections found were code-shaped). If App Review has already approved a server-granted, card-free free period in
  your app, cite it in the review notes as the precedent. Pre-decide the escalation: say it in the review notes, reply
  once if rejected, then fall back to Apple's own Free offer code with auto-renew off.
- **People already paying get their next charge moved, not a free month they cannot use.** Play's subscription defer
  (Google's own docs give six free weeks for an online survey as an example), a shifted charge date on the web, and Apple's renewal-date
  extension, which Apple documents for outages and other service interruptions (up to 90 days, at most twice a year
  per customer, only after one paid period), so name the use in the review notes before relying on it. Never a
  percentage coupon, which on an annual plan gives away a year.
- **Show an offer only to people who can get it right now.** Gate every offer surface on one server answer, so nobody
  is promised a thank-you that does not arrive. A silent "thanks" after a visible promise reads as "your words did not
  count".
- **A spam floor the person can see, not a verdict they cannot.** A visible minimum on Send ("a sentence or two is
  plenty"), then a check that stops only spam. Every note gets the same reply, whether it passed or not, and the floor
  means only spam ever fails.
- **If an AI reads the note, say so before Send, every time, and never send it when AI is off.** Apple's 5.1.2(i) wants
  explicit permission before personal data goes to a third-party AI, and the privacy policy gains a line.
- **Hold the store's rating ask until the gift period ends,** with a stored date rather than a session, because a phone
  app can live for days. Never quote rewarded feedback publicly: that is an incentivised testimonial.
- **Make research calls easy to say yes to, and capped.** A booking page outside the app (so the app collects
  nothing), 20 minutes, video with the camera optional, a small gift card afterwards, and only a few windows a week so
  the budget cannot run away.

---

## The go-to-market checklist

```
[0] Root, privacy, terms and support are real HTML on a plain fetch (curl -L | grep a known line)
[0] Post-build script patches the EXPORTED html. CI greps each tag, one assertion per line
[0] robots.txt (full sitemap URL), sitemap of public pages only, one canonical on the shell
[0] Title names the audience, description's first ~115 characters carry it. Social image re-checked after deploy
[0] No email collection beyond sign-in, written down as a rule
[0] No fake social proof, and no reward of any kind tied to a rating or review
[1] Pre-paint boot picks landing or app. CI runs the shipped boot against fake browsers
[1] Search Console Domain property via a TXT record marked NEVER DELETE. Full sitemap URL submitted
[1] Fonts self-hosted. Cookieless page analytics named in the privacy policy
[1] Every store field has one repo source. The listing gate runs in CI, its break test after every gate change
[1] Live listing read before any rewrite. Every paste printed from the gated file and diffed
[1] What's New in every App Store localisation. Play: one box, 500 per tag, English written for French
[1] Play: no price of yours, no other payment method (unless enrolled), no trial wording, in the app or listing
[1] Health-adjacent: three not-a-medical-device sentences pinned in every language
[1] Privacy declarations traced to code and read back from the console every submission
[1] App Store name = brand + category. Keyword field gated. Second keyword set only where the table allows
[1] Search-rank baseline the day a listing changes. Reruns at ~1 and ~4 weeks. Judge from the second
[1] Screenshot harness seeds every render gate, stubs the network, checks image headers, gates captions
[1] Store rating card only: earned by use, calm moment, capped, lazily imported, tested where it can show
[1] Website store badges tagged by channel. Update and rate links untagged, held by a test
[1] One developer name on both stores. Account-wide developer email, per-app support emails
[2] Positioning one-pager: lanes, sourced rivals, a checkable lead claim, honest losses, fact-checked
[2] Feedback thank-you: server grant on every platform, offer gated on eligibility, a visible spam floor,
    the same reply either way, AI named before Send, rating ask held during the gift, never quoted publicly
[2] Research calls: booking page outside the app, camera optional, capped windows
```

*Distilled from DoubleDone, a live calm to-do app on iOS, Android and the web. The lessons are its own, the words are
authored fresh, and `scripts/store-ranks.py` is adapted from its script with every id removed. MIT, like the rest of
this repo.*
