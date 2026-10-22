# RYBA website

Static website for **https://ryba.nevesely.science**, published from the root of `main` with GitHub Pages. No build step or Jekyll theme is required.

- `index.html`: homepage, Features, Overview, Tutorials & Examples and Downloads.
- `assets/css/site.css`: layout and the palette/fonts shared with nevesely.science.
- `assets/js/site.js`: overview tabs, accessible mobile navigation, touch logo toggle and download-link synchronization.
- `assets/img/ryba-logo.png`: supplied original logo.
- `assets/img/ryba-logo-hover.png`: alternate logo with a larger turquoise fish.

## Downloads have one source

Application files live in **nevsci/nevsci.github.io**, under `assets/projects/RYBA/`. Do not copy application files to this repository.

The download buttons use absolute URLs to those same files. On page load, the site reads https://nevesely.science/downloads/ and refreshes recognized RYBA download URLs, filenames and version labels. If that request is unavailable, the verified links in the HTML keep working. When updating this site, check `downloads.md` in the main website repository and update the fallback links too.

## Editing

The Overview section uses five scientific visualisations from real RYBA project and ORCA data, with a consistent dark frame. Select an image to open the full-size dialog or follow its original-image link. Keep captions descriptive and preserve useful alternative text. The original screenshots remain unchanged as source references. The logo frame is CSS, so it can be adjusted without modifying either image.

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

Main sections use large H, He and Li tiles. Features use smaller H–O markers and the Overview tabs use H, He, Li, Be and B. These are ordered element symbols, not scientific data. Preserve normal capitalization.

## GoatCounter

Both sites send to the existing nevesely.goatcounter.com dashboard. assets/js/analytics.js loads before the official count.js and prefixes pageviews with /ryba, so the dedicated homepage appears as /ryba/ and the personal site's historical paths stay unchanged.

Download events retain the same version/platform names used by the personal website, combining the click totals. The data-goatcounter-referrer attribute distinguishes the two source pages within each event's referrer breakdown. Current download-link synchronization leaves this source attribute intact.

Keep the native data-goatcounter-click binding; do not add a second click handler. The metrics measure download-link clicks, not completed file transfers.

## Tutorials and examples

The Tutorials navigation link opens the under-construction section on the homepage. It outlines three planned guides: preparing an ORCA input, generating a UV–Vis spectrum and building a thermochemical diagram. There are no unfinished guide pages or placeholder download links. Add real screenshots and verified example files as the full guides are completed; update the construction notice accordingly.

The homepage anchors are not separate sitemap URLs.

## Overview image provenance

- assets/img/overview-geometry-workshop.png: supplied obrazek(20261021-203939).png (2048 × 1240).
- assets/img/overview-uvvis-spectrum.png: supplied obrazek(20261021-204130).png (1765 × 1766).
- assets/img/overview-thermochemical-profile.png: supplied Reaction_thermochemistry(1).png (2048 × 1399).

Original image bytes are retained. No scientific values, axes or structures were changed. The Tutorials section remains under construction.

## GOAT and IR visualisations

The dedicated feature entries and two additional Overview tabs use real supplied ORCA data, rendered as scientific illustrations rather than interface screenshots:

- `assets/img/overview-goat-ensemble.png`: source conformers 0 and 1, rigidly aligned on the six-carbon aromatic ring (file atoms 1–6), with all 39 populations from the final GOAT table at 298.15 K. Hydrogen atoms are hidden. Alignment does not modify the geometries or imply a constrained calculation.
- `assets/img/overview-ir-spectrum.png`: the last IR table in TS1.out, with 119 positive modes. Lorentzian broadening uses FWHM 12 cm⁻¹, frequency scale 1.000 and a normalised intensity axis. The single imaginary mode at −147.16 cm⁻¹ is disclosed separately.

`assets/data/overview-provenance.json` records original-file hashes and processing choices. Original ORCA files remain local. To regenerate (Python with numpy, scipy and matplotlib):

```sh
python scripts/render-overview.py --ir /path/to/TS1.out --goat /path/to/SP_171.out --ensemble /path/to/SP_171.finalensemble.xyz
```

Keep the full-size image viewer and the visible distinction between application screenshots and data visualisations.

## Figures from the saved RYBA project

The first three active Overview figures are now rendered from the supplied saved project:

- `assets/img/overview-geometry-render.png`: the 23-atom Fum_ketone structure from the input Geometry Workshop, including saved bond orders and hydrogens. No optimisation or geometry changes are applied.
- `assets/img/overview-uvvis-render.png`: all ten singlet transitions in TTT-wHPBE, checked against the embedded ORCA length-gauge table. Gaussian broadening retains the saved 0.30 eV FWHM; the profile is normalised and plotted over 250–800 nm, with oscillator strengths on a separate axis.
- `assets/img/overview-thermochemistry-render.png`: Closed form → TS1 → CCC → TS2 → CTC → TS3 → CTT, using final printed Gibbs energies at 298.15 K relative to Closed form, with the saved geometry assignments. Independent rigid camera rotations accommodate different source atom orders. Hydrogens are hidden in the small structure views.

All three figures are 2400 × 1500 PNGs, with no thumbnail crop. `assets/data/project-overview-provenance.json` records the archive/state hashes and exact rendering choices. The project ZIP, extracted state and embedded outputs remain local. To regenerate:

```sh
python scripts/render-project-overview.py /path/to/saved-project.ryba.zip
```

The earlier supplied screenshots and thermochemical export keep their original filenames and bytes as source references. They are no longer the active website previews.
