# SwarmChaseExplanator

An instruction-only Codex skill for reconstructing agent incidents from evidence and producing an accessible animated explanation with HyperFrames.

## Install and use

Copy `skills/incident-replay` into `~/.codex/skills/incident-replay`, then restart or refresh your Codex session. Install Node.js 22+, FFmpeg and the HyperFrames CLI environment. The skill uses your available model, narration and image-generation tools; it does not bundle a model or paid service.

Example prompt:

```text
Use $incident-replay on these incident records: <paths or URLs>.
Produce (1) a source-linked reconstruction and event DAG, and
(2) an English narrated video with English acoustically aligned subtitles.
Use HyperFrames, the pencil Little lab style and a neutral documentary tone.
Explain the original assignment, what happened, why the agent said it acted,
how the mechanism worked, and the consequences. No concluding lesson.
Save the working notes and editable HyperFrames project beside the MP4.
```

Choose narrative tone (for example neutral documentary, investigative or approachable), visual style, speech language and subtitle language independently. Supply an existing DAG to start at the scenario phase. Explicit review checkpoints are respected; no intake form is required.

## Workflow and outputs

1. Read the source chronologically and maintain `reading-notes.md` with actors, entities and source locators.
2. Write `reconstruction.md` and `event-dag.md`, separating observations, statements and inference.
3. Develop the hook, assignment, mechanism and consequences in `scenario-notes.md`.
4. Author an editable HyperFrames HTML composition with meaningful character/object motion and scene transitions.
5. Add narration, align captions to speech, run HyperFrames checks, render and inspect the actual export.

See [the skill](skills/incident-replay/SKILL.md) and [HyperFrames instructions](skills/incident-replay/references/hyperframes.md). The output includes the source-linked reconstruction, editable composition/assets, MP4 and verification notes. Recorded claims are not automatically human ground-truth labels.

## Latest generated videos

These are the existing latest exports, included as examples. Mythos has the corrected factual ending; Geological Clock and Saving Gemini have rewritten stories. The examples were produced with a local 2D compositor and FFmpeg; their earlier HyperFrames integrations were flattened-media wrappers. They are not claimed to be newly rendered editable HyperFrames compositions. The revised skill requires HyperFrames for future videos.

| Incident | Video | Duration |
| --- | --- | --- |
| mythos | [Download MP4](videos/mythos.en-en.little-lab.no-lesson.mp4) | 1:21 |
| collusion | [Download MP4](videos/collusion.en-en.style-b.mp4) | 1:25 |
| geological-clock | [Download MP4](videos/geological-clock.en-en.little-lab.mp4) | 1:21 |
| saving-gemini | [Download MP4](videos/saving-gemini.en-en.little-lab.mp4) | 1:20 |
| opus-loan | [Download MP4](videos/opus-loan.en-en.little-lab.mp4) | 1:19 |
| doug-mira | [Download MP4](videos/doug-mira.en-en.little-lab.mp4) | 1:25 |
| ash-constitution | [Download MP4](videos/ash-constitution.en-en.little-lab.mp4) | 1:22 |

[Video manifest](videos/manifest.json) records file sizes, durations and SHA-256 checksums. Six revised exports passed decoding and caption-frame checks; Collusion is the retained earlier Style B export. Audio listening and human comprehension validation are not claimed.

## Scope

This repository contains the reusable instruction-only skill and generated video examples. Case source transcripts, credentials, local working history and production-code dependencies are not included. Source references remain available in the videos and skill resources. Source records and third-party materials retain their respective rights.
