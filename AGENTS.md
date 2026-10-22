# RYBA website

This repository publishes the static website at https://ryba.nevesely.science.

## User requirements

- Latest downloads must point to the exact same files as the main website, https://nevesely.science/downloads/, whose source is nevsci/nevsci.github.io, downloads.md. Never upload or maintain a separate copy of a RYBA application download in this repository. Never construct a new versioned download URL without checking that canonical page/source first.
- Keep the automatic download-link refresh in assets/js/site.js. The HTML links are a working, verified fallback and must also match the main website when edited.
- Match the main website palette: cream #F7F4EE, text #2B2B2B, teal #2F5D62, hover #163A40, navigation #af9d83, border #BFB4A5, footer #D9D0C3, muted #5E564D.
- Match its fonts: IBM Plex Sans for headings/navigation/buttons, IBM Plex Serif for body text.
- Preserve the supplied default RYBA logo and the alternate larger-fish logo. Swap to the alternate on hover and keyboard focus; keep the touch toggle.
- Features is primarily text, Overview is primarily visual, Downloads lists the shared application files. Overview uses five user-supplied RYBA images: geometry/input, combined IR–UV–Vis–NMR spectra, thermochemistry, GOAT, and coordinate scans. Keep the spectra and force-field scan capabilities explicit.
- Keep CNAME set to ryba.nevesely.science and preserve .nojekyll. Hosting is GitHub Pages in this repository.

## Release history and numbering

- Use Roman numerals for all website sequence markers. Main sections use larger framed I–IV tiles; features use smaller I–VIII markers, Overview tabs I–V, and tutorial outlines I–III. Preserve the existing square frames, palette and typographic hierarchy. Do not change chemical symbols or numeric scientific data inside images or prose.
- Keep the native, initially collapsed Older versions disclosure below the latest downloads. It currently has no release entries; do not list the current release as an older version.
- When publishing a new compiled RYBA release, preserve the currently published version's immutable, versioned files in nevsci/nevsci.github.io. Do not overwrite or delete them.
- Upload new binaries once, to the main website repository. Update its downloads.md and this website's latest HTML links/version labels to those same new files.
- Add the previous public release (version and original platform links) to Older versions on the dedicated RYBA website. The personal website can continue to show only the latest release. The archive stores links/metadata, not separate binary copies.
- Archived links must not carry data-download or data-release-for attributes: assets/js/site.js refreshes only the latest-release controls. Never replace historical links with the current release during synchronization.

## Analytics

- Both websites use https://nevesely.goatcounter.com/count. RYBA pageviews are prefixed with /ryba via assets/js/analytics.js so its homepage remains distinct from the personal homepage.
- Keep the ordered defer script loading: analytics.js before the official GoatCounter count.js. Do not add a second event handler or send duplicate click events.
- Download clicks on both websites must use the same version/platform data-goatcounter-click event names and data-goatcounter-title values, so totals aggregate in the existing dashboard.
- Use data-goatcounter-referrer to identify the clicked page: https://ryba.nevesely.science/ for RYBA, https://nevesely.science/downloads/ for the personal website. Keep this source attribute when refreshing latest download links.
- Archived download links also retain the original version/platform GoatCounter event names and the RYBA source referrer. Archived links must not use the latest-release synchronization attributes.

## Tutorials and examples

- Keep Tutorials & Examples between Overview and Downloads, linked from the main navigation. Preserve section order and Roman numerals: I Features, II Overview, III Tutorials, IV Downloads.
- The section is currently under construction. Keep the notice and planned-example wording until complete, verified guides and usable sample files are published.
- Initial topics are ORCA input preparation, UV–Vis spectrum generation from TD-DFT results, and thermochemical diagrams.
- Do not add dead tutorial/download links or present the outlines as finished guides. Real screenshots and sample files can replace the planned outlines when ready.

## Overview images

- Use the supplied images as-is; preserve original PNG bytes, scientific structures, data, units, axes and labels. CSS may frame and scale them without cropping their scientific content.
- Geometry/input uses assets/img/overview-geometry-workshop.png, the earlier supplied Geometry Workshop screenshot. The four newer images are listed in assets/data/supplied-overview-images.json.
- The spectra tab combines IR, UV–Vis and NMR in the supplied portrait composite. Mention all three in the feature and Overview copy. Preserve its natural portrait aspect ratio and the full-size image viewer.
- Coordinate scans replace the separate IR Overview tab because IR is included in the combined spectra tab. Describe scans as integrated force-field scans; the supplied example is a relaxed MMFF94 dihedral scan, not an ORCA quantum calculation.
- The new thermochemistry export uses kJ/mol; do not carry over kcal/mol descriptions from previous figures.
- The supplied GOAT image shows filtered conformers, with populations renormalised within the selected subset. Do not describe it as a two-conformer ghost overlay or a complete unfiltered population distribution.
- Preserve the full-size dialog, close button, Escape support, focus restoration and direct image links. Links must still work without JavaScript.
- Earlier rendered figures and their scripts/provenance are historical assets, not active previews. Do not overwrite the user's supplied images with generated replacements unless explicitly asked.
