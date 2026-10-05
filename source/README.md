# Vision Iconic

A complete static landing page with Tailwind CSS, supplied architectural imagery and traced SVG branding. English is the default; French, Spanish, Dutch, German and Portuguese have individual routes and country-specific buyer content.

## Preview

Serve the `dist` directory over HTTP. Opening index.html directly as a local file will not resolve root-relative asset and language URLs.

    python3 -m http.server 8924 --directory dist

Then visit http://localhost:8924.

## Tally connection

Set `tallyUrl` in `dist/assets/config.js` to the actual HTTPS Tally form URL. Calls to action send language, residence, currency, source path and existing UTM parameters to the form. Configure matching hidden fields in Tally. The supplied Tally form VLk0NJ is now connected and opens inside the light enquiry modal. It was checked visually without sending any test submission. With no URL, the site displays that enquiries are not yet available.

Each translated page needs a Tally form that supports its visitor language; passing a language field alone does not translate a Tally form. Tally's privacy terms and the receiving business's privacy notice need to be supplied before live collection. The current privacy text describes the preview only.

## Production domain and SEO

After obtaining the real production origin, regenerate HTML and sitemap with:

    python3 build.py https://YOUR-ACTUAL-DOMAIN

Replace the example argument with the real domain. This sets absolute canonical URLs, hreflang alternatives, Open Graph URLs, project schema URLs, sitemap.xml and robots.txt. Until then, preview canonical URLs are relative and there is no production sitemap. Optionally set siteOrigin in config.js for browser metadata; static regeneration is preferred for search crawlers.

To rebuild the Tailwind stylesheet after editing styles.css:

    node compile-css.mjs

Dependencies are recorded in package.json and pnpm-lock.yaml. Existing compiled HTML/CSS requires no Node runtime or build to host.

## Assets and source accuracy

- Images extracted from the supplied image folder associated with Vision Iconic Digital Brochure-1.pdf and converted to optimised WebP.
- Brand SVG vectorised from the white logo contours on PDF page 1. This is a faithful trace of a raster source, not the original brand master vector.
- Floor plans extracted from PDF pages 10–14 and displayed in labelled dialogs. Areas are illustrative, tied to the shown plan, not a promised minimum for every residence. Royal Suite and retail plans were not supplied, so none are fabricated.
- Starting AED and USD prices transcribed from the raster price table on PDF page 15. USD values follow the brochure rather than a live exchange feed. The brochure mentions an October 6 launch without establishing the year, so no dated launch promise is shown.
- Commission is presented as an offer requiring written confirmation; full charges are not implied to be zero.
- Payment-plan percentages, completion dates, rental yields and live availability were not supplied and are not invented.
- Presentation is project-led; no agent name is invented. The footer avoids claiming official authorisation from Mercedes-Benz or Binghatti.

## Official sources consulted, 5 October 2026

- Mercedes-Benz: world's first branded city announcement: https://media.mercedes-benz.com/en/article/d9b4aab7-a355-4be3-b952-c151800e5dbc
- Binghatti project overview: https://www.binghatti.com/en/branded-projects/mercedes-benz-places-binghatti-city
- UAE personal taxation: https://u.ae/en/information-and-services/finance-and-investment/taxation
- Federal Tax Authority, personal real estate investments: https://tax.gov.ae/en/content/real.estate.investment.for.natural.persons.ctgrei1.aspx
- Official Golden Visa conditions: https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/golden-visa
- ICP Golden Residency guide: https://icp.gov.ae/en/services/uae-golden-residency/
- Dubai Land Department property registration: https://backoffice.dubailand.gov.ae/en/eservices/property-sale-registration/

## Verification

All seven HTML pages (English root plus six language routes) have valid local asset and route references. Locale keys are complete. Browser checks passed for USD selection, floor-plan dialogs, unavailable-enquiry state, language navigation, desktop/mobile overflow and JavaScript errors. Hero layouts were visually checked at desktop and mobile sizes.

## Publication status

Sites creation was refused because the account has reached its hosting usage limit. No Site ID was issued and no version was published. This package preserves the finished implementation and assets. Tally is connected. Regenerate SEO for the eventual domain, then publish when hosting becomes available.

## Follow-up corrections

Replaced the native language selector, centered dialogs, added explicit paragraph-to-button spacing, separated mobile hero image and text, removed the header separator, and embedded Tally on a light background. All six routes passed overflow checks at 320 CSS pixels. The supplied Tally form currently displays its own English field labels. Language parameters are forwarded but do not translate its fields.

## SEO expansion and Hostinger delivery

Production origin configured: https://vision-iconic-residences.com (chosen domain, not a registration or deployment confirmation).

90 canonical pages: six project pages, six category directories, 48 category pages and 30 buyer guides. The root English duplicate is canonically consolidated, and Hostinger redirects the root to /en/invest-in-dubai/. Dedicated content covers eight brochure categories: 1/2/3-bedroom apartments, 2/3-bedroom Royal Suites, 4/5-bedroom duplex layouts and retail. No inventory or missing Royal Suite plans were fabricated.

SEO checks passed for all 90 unique titles, descriptions, canonical URLs, reciprocal page-specific hreflang alternatives, schema JSON, local asset/route links and sitemap entries. The XML sitemap lists 90 URLs and seven language alternatives per URL, including x-default. Browser layout checks visited all 90 routes twice without detected horizontal/text overflow at the rendered viewport sizes; language equivalence, plan dialogs and Tally context parameters were checked on a representative category page. No enquiry was submitted. Server-side Hostinger redirects and HTTPS need verification after upload because the local preview does not execute .htaccess.

`site-settings.json` preserves the chosen origin for future builds. `seo_pages.py` and `seo-data.json` hold the additional route generation and translated content. `check_seo.py` validates the static SEO output.

The Hostinger deployment ZIP contains only dist contents at its root, including .htaccess. Extract into public_html on a Web Hosting plan; it is not a WordPress theme or a Hostinger Website Builder template. DNS, domain registration, HTTPS activation and Google Search Console verification have not been performed.

References:
https://developers.google.com/search/docs/specialty/international/localized-versions
https://developers.google.com/search/docs/fundamentals/seo-starter-guide
https://www.hostinger.com/support/1869114-how-to-upload-backups-with-file-manager-in-hostinger/
