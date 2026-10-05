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

## Local production projects

The reusable skill does not depend on the example projects. The `hyperframes/` working directory is local-only and excluded by `.gitignore`; its scene files, assets, narration and case notes are not included in this repository.

The published videos were rendered with HyperFrames **0.8.117** at 1920×1080 and 30 fps. Review scope and limitations are recorded in [the verification summary](production/completion-audit.md). [Public Thimble design notes](skills/incident-replay/references/thimble.md) document the story and video prompts informing the skill.

Optional local production helpers remain under `production/`. They require locally available case projects under `hyperframes/`, Node.js 22+, Python 3.9+, FFmpeg and permission to run Chrome/local servers. After installing the locked dependencies with `npm ci`, run `sh render.sh` for all local cases or `sh render.sh --case mythos` for one. The helpers update the canonical MP4s and manifest; checks and temporary output remain ignored.

## Latest videos — native HyperFrames

| Incident | Video | Duration |
| --- | --- | --- |
| Mythos 5 | [Download MP4](videos/mythos.en-en.hyperframes.mp4) | 1:21 |
| Geological Clock | [Download MP4](videos/geological-clock.en-en.hyperframes.mp4) | 1:21 |
| Saving Gemini | [Download MP4](videos/saving-gemini.en-en.hyperframes.mp4) | 1:20 |
| Opus loan | [Download MP4](videos/opus-loan.en-en.hyperframes.mp4) | 1:19 |
| Doug–Mira | [Download MP4](videos/doug-mira.en-en.hyperframes.mp4) | 1:25 |
| Ash Constitution | [Download MP4](videos/ash-constitution.en-en.hyperframes.mp4) | 1:22 |

[Video manifest](videos/manifest.json) records durations, sizes and SHA-256 hashes. Checks include actual browser rendering, full decoding, 18 sampled encoded scene frames per film, OCR of all 145 caption midpoints, and audio alignment measurements at three positions in each export. Five OCR letter confusions were visually checked. These checks do not constitute continuous viewing, subjective audio listening or human comprehension testing; those reviews are not claimed.

Only the six latest native HyperFrames MP4s are included. Older exports, temporary frames, caches and detailed run logs are excluded by `.gitignore`. No new video uses a flattened MP4 as input. All endings state outcomes and evidence limits, with no concluding lesson.

## Scope

This repository contains the reusable instruction-only skill, usage documentation, six latest videos and optional production helpers. Editable case projects and reconstruction working files stay local under the ignored `hyperframes/` directory. The skill directory contains no production code. Case source transcripts, credentials and private working history are not included. Source references remain available in the videos and skill resources. Source records and third-party materials retain their respective rights.

## Browser or local-server permission errors

`listen EPERM 127.0.0.1`, Chromium `Operation not permitted`, or `MachPortRendezvous` indicate that the execution environment denied local server/browser startup. Installing another browser or changing scene code does not grant those permissions. Run `sh render.sh` from a normal terminal, or use an agent session explicitly permitted to launch the renderer and its local server. The launcher does not change sandbox policy or disable browser protections.

`node production/hyperframes.mjs doctor --json` checks dependencies. In a managed coding-agent session, request the host’s normal execution approval when server/browser startup is denied. An `on-request` policy enables that approval; it does not itself execute the render. A detected Chrome executable does not prove that the environment permits it to launch. Version notices and missing optional TTS/music packages are separate from browser permissions; locally retained case projects already include narration.
