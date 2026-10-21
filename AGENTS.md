# RYBA website

This repository publishes the static website at https://ryba.nevesely.science.

## User requirements

- Latest downloads must point to the exact same files as the main website, https://nevesely.science/downloads/, whose source is nevsci/nevsci.github.io, downloads.md. Never upload or maintain a separate copy of a RYBA application download in this repository. Never construct a new versioned download URL without checking that canonical page/source first.
- Keep the automatic download-link refresh in assets/js/site.js. The HTML links are a working, verified fallback and must also match the main website when edited.
- Match the main website palette: cream #F7F4EE, text #2B2B2B, teal #2F5D62, hover #163A40, navigation #af9d83, border #BFB4A5, footer #D9D0C3, muted #5E564D.
- Match its fonts: IBM Plex Sans for headings/navigation/buttons, IBM Plex Serif for body text.
- Preserve the supplied default RYBA logo and the alternate larger-fish logo. Swap to the alternate on hover and keyboard focus; keep the touch toggle.
- Features is primarily text, Overview is primarily visual, Downloads lists the shared application files. Overview uses the user-provided Geometry Workshop screenshot, UV–Vis screenshot and exported thermochemical diagram, plus data-derived GOAT and IR visualisations. Keep dedicated GOAT and IR feature entries.
- Keep CNAME set to ryba.nevesely.science and preserve .nojekyll. Hosting is GitHub Pages in this repository.

## Release history and numbering

- Use periodic-table symbols instead of sequence numbers: H, He, Li, Be, B, C, etc. Main section symbols are larger framed tiles; subordinate feature markers and Overview tab symbols remain smaller. Preserve correct chemical capitalization (He, Li, Be), including under text-transform rules.
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

- Keep Tutorials & Examples between Overview and Downloads, linked from the main navigation. Preserve periodic-table section order: H Features, He Overview, Li Tutorials, Be Downloads.
- The section is currently under construction. Keep the notice and planned-example wording until complete, verified guides and usable sample files are published.
- Initial topics are ORCA input preparation, UV–Vis spectrum generation from TD-DFT results, and thermochemical diagrams.
- Do not add dead tutorial/download links or present the outlines as finished guides. Real screenshots and sample files can replace the planned outlines when ready.

## Overview images

- Preserve the supplied scientific screenshots and exported graph without generative edits, altered values or redrawn molecular structures.
- The overview image assets retain the original uploaded bytes. CSS frames the previews and crops only the UV–Vis thumbnail to focus on the spectrum. Full originals are accessible through native image links and the accessible dialog.
- Preserve the full-size view, close button, Escape support and direct original-image links. Image links must still work when JavaScript is unavailable.

## Data-derived overview visualisations

- GOAT and IR images are scientific data illustrations, not application screenshots. Preserve that distinction in the visible captions/note.
- Regenerate with scripts/render-overview.py using the original local ORCA files; do not upload the raw outputs or ensemble here. assets/data/overview-provenance.json records hashes and rendering choices.
- GOAT uses the reported final populations at 298.15 K, checked against 39 XYZ frames and their energies. Selected conformers use source IDs 0 and 1; rigid alignment on file atoms 1–6 changes only the view. Hide hydrogens for readability.
- IR uses the last frequency job in TS1.out: 119 positive modes and a separate imaginary mode at −147.16 cm⁻¹. Keep scale/broadening and imaginary-mode disclosure visible; do not imply experimental data or a minimum.
