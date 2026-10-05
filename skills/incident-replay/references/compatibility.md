# Inputs and agent compatibility

Required input: incident records supplied as accessible local files, URLs or pasted text. Typical records include JSON/JSONL transcripts, Markdown notes, actor messages, timestamps and tool results. There is no mandatory case JSON schema. If only a retrospective account exists, state that coverage and do not invent a raw transcript.

Optional input: an existing reconstruction/DAG (skip completed reconstruction), an output directory, target duration, visual style, narrative tone, narration language and subtitle language. Preserve user choices. English and a neutral documentary tone are defaults, not requirements.

Use the same SKILL.md and references in Claude Code, Codex or another coding agent. The name and description frontmatter is portable. agents/openai.yaml is optional Codex UI metadata and may be ignored or omitted by other agents. The workflow does not use host-specific prompt substitutions, dynamic shell injection, required MCP tools, model IDs or subagent APIs.

If the host supports Agent Skills discovery, install the complete incident-replay directory in its documented skill location. Otherwise ask it to read SKILL.md and the referenced files directly. A chat-only assistant can draft notes, but cannot claim to have rendered a video without execution and file access.

Required for full local video production: file read/write, shell execution, Node.js 22+, FFmpeg, a working HyperFrames CLI, and permission to launch its headless browser and local server. Narration/image providers can be local or host-provided, within the user's authorization. Reuse approved assets and aligned speech when suitable. No proprietary image or speech API is mandatory.

Probe the installed HyperFrames version and command help. Follow the documented commands for that version: recent versions provide check and delivery quality; older versions may require lint plus validate/inspect and high quality. Record the exact version and gates used. Do not claim equivalent runtime checks when only static lint ran. Do not bypass sandbox denials; leave a runnable project and state the missing capability.

Claude Code installation and invocation: https://code.claude.com/docs/en/skills
Portable format specification: https://agentskills.io/specification
