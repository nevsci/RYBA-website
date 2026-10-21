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
