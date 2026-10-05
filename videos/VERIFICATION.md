# Export verification — 2026-10-05

The [video manifest](manifest.json) identifies the six checked MP4s by SHA-256. This compact record is retained with the deliverables; detailed run logs, frame samples and diagnostic JSON are local generated artifacts excluded by `.gitignore`.

| Check | Result |
| --- | --- |
| Native HyperFrames | Six real exports using HyperFrames 0.8.117; 36 editable SVG/GSAP scenes; no flattened video input. |
| Runtime and media | All six browser checks passed. Every 1920×1080, 30 fps MP4 fully decoded; durations and audio streams checked. |
| Visual review | 18 encoded scene samples per case. Overlapping Mythos notes and Saving Gemini's long heading were fixed and rerendered. Remaining layout warnings concern clipped illustration atlas bounds checked in the visible output. |
| Captions | All 145 cue midpoints checked using local OCR; five letter-recognition exceptions visually inspected. Existing acoustic alignment retained; no independent speech retranscription in this pass. |
| Audio timing | Three PCM comparisons per video: zero measured lag at 2 kHz, correlation above 0.9997. |
| Sources | 87 scene reference IDs resolve across six evidence indexes. 27 Mythos source substrings and three source hashes checked; detailed source verification is retained locally in the ignored case project. The approved selected reconstruction is reused, not a new full transcript review. |
| Skill | Agent-neutral, instruction-only package; format validated. Actual Claude Code execution not tested. Public Thimble prompts cited; no copied implementation dependency. |
| Publication | English narration and captions, no concluding lesson, six latest videos only; Collusion absent. |

Continuous viewing, subjective audio listening and human comprehension testing are not claimed. Automated checks and sampled inspection do not independently authenticate every upstream source. The videos remain available for user validation.
