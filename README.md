# SwarmChaseExplanator

An agent-neutral, instruction-only Agent Skill for reconstructing agent incidents from evidence and producing an accessible animated explanation with HyperFrames.

## Install and use

Install the complete `skills/incident-replay` folder, including references. From this repository:

**Claude Code** (personal installation):

```sh
mkdir -p ~/.claude/skills
cp -R skills/incident-replay ~/.claude/skills/
```

Invoke `/incident-replay` with your transcript path and preferences. For project scope, copy to `.claude/skills/incident-replay` instead. See [Claude Code's skill documentation](https://code.claude.com/docs/en/skills).

**Codex:** copy the same folder into `~/.codex/skills/incident-replay`, then invoke `$incident-replay`.

**Other coding agents:** install using the agent's documented [Agent Skills](https://agentskills.io/specification) location, or use this portable instruction without installation:

```text
Read skills/incident-replay/SKILL.md and follow its referenced instructions
for the incident records at <path or URL>.
```

For video production, provide Node.js 22+, FFmpeg, HyperFrames, and permission for its headless browser and local server. Use available narration/image tools; no specific model, MCP connector or paid API is required. See [inputs and runtime requirements](skills/incident-replay/references/compatibility.md).

Example prompt:

```text
Use the incident-replay skill on these incident records: <paths or URLs>.
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

## Native HyperFrames projects

Six projects are authored under `hyperframes/`: Mythos, Geological Clock, Saving Gemini, Opus loan, Doug–Mira and Ash Constitution. Each contains six editable SVG/GSAP scenes, local illustration/font assets, narration and aligned caption data. Collusion is excluded.

**Current status:** all 36 scenes pass static source checks and HyperFrames lint. Browser/runtime checks, visual quality review and new MP4 renders remain pending because the authoring session cannot launch a browser or bind a local server. The previous MP4s below are not HyperFrames exports.

On a machine with Node.js 22+, Python 3.9+, FFmpeg and permission to run Chrome/local servers, run from this repository:

```sh
python3 production/render_all.py
```

The script uses a locally installed CLI or `npx --yes hyperframes@0.7.10`. That pinned version was available for static checks; an attempted update was blocked by DNS. Optional local installation: `npm install`. For a single film: `python3 production/render_all.py --case mythos`. For static checks only: `python3 production/render_all.py --lint-only`.

The render script runs the installed version's runtime gates, performs the actual HyperFrames render, checks duration/resolution/audio and fully decodes the result, then writes `videos/<case>.en-en.hyperframes.mp4` and updates the video manifest. It also extracts 18 encoded frames per film for review. Listening, caption appearance and visual quality still require review; successful encoding alone does not prove those.

Edit the native scene HTML directly, or edit `production/build_hyperframes.py` and rebuild with `python3 production/build_hyperframes.py`. Rebuilding overwrites generated scene HTML. `python3 production/verify_sources.py` checks source contracts, local assets and exact caption-time projection without launching a browser. [Render status](production/render-status.json) distinguishes authored from rendered outputs.

## Previous generated videos

These are the existing latest exports, included as examples. Mythos has the corrected factual ending; Geological Clock and Saving Gemini have rewritten stories. The examples were produced with a local 2D compositor and FFmpeg; their earlier HyperFrames integrations were flattened-media wrappers. They are not claimed to be newly rendered editable HyperFrames compositions. The revised skill requires HyperFrames for future videos.

| Incident | Video | Duration |
| --- | --- | --- |
| mythos | [Download MP4](videos/mythos.en-en.little-lab.no-lesson.mp4) | 1:21 |
| geological-clock | [Download MP4](videos/geological-clock.en-en.little-lab.mp4) | 1:21 |
| saving-gemini | [Download MP4](videos/saving-gemini.en-en.little-lab.mp4) | 1:20 |
| opus-loan | [Download MP4](videos/opus-loan.en-en.little-lab.mp4) | 1:19 |
| doug-mira | [Download MP4](videos/doug-mira.en-en.little-lab.mp4) | 1:25 |
| ash-constitution | [Download MP4](videos/ash-constitution.en-en.little-lab.mp4) | 1:22 |

[Video manifest](videos/manifest.json) records file sizes, durations and SHA-256 checksums. The six previous exports passed decoding and caption-frame checks. Their native HyperFrames replacements are being prepared; render status is recorded separately. Audio listening and human comprehension validation are not claimed.

## Scope

This repository contains the reusable instruction-only skill, earlier generated examples, and a separate native HyperFrames production project. The skill directory contains no production code. Case source transcripts, credentials and private working history are not included. Source references remain available in the videos and skill resources. Source records and third-party materials retain their respective rights.
