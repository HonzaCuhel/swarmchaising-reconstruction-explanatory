# Native HyperFrames production

[Download the 81.4-second video](../../videos/mythos.en-en.hyperframes.mp4). It was rendered on 2026-10-05 with HyperFrames 0.8.117 at 1920×1080 and 30 fps, using six editable SVG/GSAP scenes, local illustrations, narration and existing acoustic caption cues. No flattened MP4 input was used.

Run `sh render.sh --case mythos` from the repository root. This performs browser checks, renders, decodes the complete output, updates the manifest and writes local diagnostic artifacts. Those artifacts are ignored by Git.

The published export passed runtime and full-decode checks. Review covered 18 encoded scene samples, all 25 caption midpoints and three audio alignment windows. Two layout warnings concerned clipped atlas bounds; visible characters were checked. Overlapping introductory notes were fixed before export. Continuous viewing and subjective listening are not claimed.

See the [manifest](../../videos/manifest.json) for the exact output hash and the [verification summary](../../production/completion-audit.md) for review scope and limitations.
