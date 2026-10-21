# RYBA website

This repository publishes the static website at https://ryba.nevesely.science.

## User requirements

- Downloads must point to the exact same files as the main website, https://nevesely.science/downloads/, whose source is nevsci/nevsci.github.io, downloads.md. Never upload or maintain a separate copy of a RYBA application download in this repository. Never construct a new versioned download URL without checking that canonical page/source first.
- Keep the automatic download-link refresh in assets/js/site.js. The HTML links are a working, verified fallback and must also match the main website when edited.
- Match the main website palette: cream #F7F4EE, text #2B2B2B, teal #2F5D62, hover #163A40, navigation #af9d83, border #BFB4A5, footer #D9D0C3, muted #5E564D.
- Match its fonts: IBM Plex Sans for headings/navigation/buttons, IBM Plex Serif for body text.
- Preserve the supplied default RYBA logo and the alternate larger-fish logo. Swap to the alternate on hover and keyboard focus; keep the touch toggle.
- Features is primarily text, Overview is primarily visual, Downloads lists the shared application files. Clearly label schematic placeholders until real screenshots replace them.
- Keep CNAME set to ryba.nevesely.science and preserve .nojekyll. Hosting is GitHub Pages in this repository.
