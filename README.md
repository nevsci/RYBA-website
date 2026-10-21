# RYBA website

Static website for **https://ryba.nevesely.science**, published from the root of `main` with GitHub Pages. No build step or Jekyll theme is required.

- `index.html`: homepage, Features, Overview and Downloads.
- `assets/css/site.css`: layout and the palette/fonts shared with nevesely.science.
- `assets/js/site.js`: overview tabs, accessible mobile navigation, touch logo toggle and download-link synchronization.
- `assets/img/ryba-logo.png`: supplied original logo.
- `assets/img/ryba-logo-hover.png`: alternate logo with a larger turquoise fish.

## Downloads have one source

Application files live in **nevsci/nevsci.github.io**, under `assets/projects/RYBA/`. Do not copy application files to this repository.

The download buttons use absolute URLs to those same files. On page load, the site reads https://nevesely.science/downloads/ and refreshes recognized RYBA download URLs, filenames and version labels. If that request is unavailable, the verified links in the HTML keep working. When updating this site, check `downloads.md` in the main website repository and update the fallback links too.

## Editing

Replace the three explicitly labelled schematic previews with real RYBA screenshots when available. Keep their captions descriptive and retain useful alternative text. The logo frame is CSS, so it can be adjusted without modifying either image.

Preview locally with `python -m http.server 8000` from the repository root. The static page also renders without JavaScript; JavaScript adds the overview tabs and refreshes download links.

See `AGENTS.md` for the user's continuing requirements.

## Publishing the next RYBA release

The Older versions disclosure is initially empty and closed. Once a new compiled version is ready:

1. Record the currently published release's version and its platform URLs before changing the latest links.
2. Keep its original versioned files in nevsci/nevsci.github.io and upload the new files there once.
3. Update downloads.md on the main website and the latest-download fallback links/version labels in this website's index.html to the new canonical files.
4. Replace the archive's empty-state paragraph with an entry for the previous public release, retaining its original file URLs. Add later historical releases newest first.
5. Do not use data-download or data-release-for on archived entries; those attributes belong to the latest-release synchronization.

Do not create independent binary copies in this website repository. Historical files remain shared with the main website even when they are no longer listed on its latest-download page.

## Element sequence markers

Main sections use large H, He and Li tiles. Features use smaller H–C markers and the Overview tabs use H, He and Li. These are ordered element symbols, not scientific data. Preserve normal capitalization.

## GoatCounter

Both sites send to the existing nevesely.goatcounter.com dashboard. assets/js/analytics.js loads before the official count.js and prefixes pageviews with /ryba, so the dedicated homepage appears as /ryba/ and the personal site's historical paths stay unchanged.

Download events retain the same version/platform names used by the personal website, combining the click totals. The data-goatcounter-referrer attribute distinguishes the two source pages within each event's referrer breakdown. Current download-link synchronization leaves this source attribute intact.

Keep the native data-goatcounter-click binding; do not add a second click handler. The metrics measure download-link clicks, not completed file transfers.
