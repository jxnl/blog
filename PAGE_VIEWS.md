# Blog view counts

The site publishes approximate per-post view counts from Google Analytics 4. Counts are fetched during the Cloudflare Pages build and written to the static `/assets/page-views.json` asset. No Google credentials are sent to browsers.

## Cloudflare Pages configuration

Grant a Google service account Viewer access to the GA4 property, then add these encrypted build variables to the Cloudflare Pages project:

- `GA_PROPERTY_ID`: the numeric GA4 property ID, not the `G-...` measurement ID
- `GOOGLE_SERVICE_ACCOUNT_JSON`: the complete service-account credentials JSON

Both variables are optional for local development. When neither is present, MkDocs writes an empty snapshot and the site omits view counts. Supplying only one variable fails the build so a production configuration error is visible.

## Daily refresh

Create a Cloudflare Pages deploy hook and save its URL as the GitHub Actions secret `CLOUDFLARE_DEPLOY_HOOK`. The `Refresh page views` workflow invokes it daily and can also be run manually.

The report uses GA4's `screenPageViews` metric from January 1, 2020 through yesterday. It combines `jxnl.co` and `www.jxnl.co`, normalizes trailing slashes and `index.html`, and includes only dated `/writing/YYYY/MM/DD/slug/` post routes.
