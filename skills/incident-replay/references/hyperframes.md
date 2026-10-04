# HyperFrames production workflow

Use HyperFrames for every new incident video unless the user explicitly chooses another framework. If installed, read the hyperframes entry skill and its general-video, core, animation and CLI references. Otherwise use the installed CLI help and official HyperFrames documentation. Record the CLI version and exact commands in production-notes.md. Node.js 22+ and FFmpeg are required for the local workflow.

1. Create a project with `npx hyperframes init <project>`. Keep index.html, hyperframes.json, local assets, narration and caption data with the case outputs.
2. Turn scenario-notes.md into timed scenes. Give each beat a visible action and consequence. Keep characters, objects, annotations and backgrounds separately editable; animate them with a deterministic, seekable timeline. Search `npx hyperframes catalog --query "<desired motion>"` before authoring a motion primitive from scratch.
3. Follow the HyperFrames composition contract: a sized root with data-composition-id, data-width, data-height and data-duration; one paused GSAP timeline registered under the same composition ID; timed media clips with unique IDs. No wall-clock animation, unseeded randomness or network requests during rendering. Animate inner scene elements, not clip visibility owned by the framework.
4. Place actual narration on the timeline. Derive scene duration from audio, acoustically align subtitles and preserve timing when editing. Keep narration language, subtitle language, tone and drawing style independently configurable.
5. Run `npx hyperframes lint` while authoring, then `npx hyperframes check` as the final runtime/layout gate. Inspect snapshots at meaningful action points with `npx hyperframes snapshot --at <seconds>`. Open `npx hyperframes preview --background` for requested review. Honor existing user authorization to render; do not create an extra approval stage.
6. Render using `npx hyperframes render --quality delivery --output renders/incident.mp4`. Verify the encoded MP4 with ffprobe and a complete FFmpeg decode, inspect moving sequences and captions, and report audio listening separately.

Deliver both the editable HyperFrames project and MP4. Keep reconstruction.md, event-dag.md, scenario-notes.md and reading-notes.md alongside it. End with observed outcomes and evidence limits; do not add a lesson unless requested.

For an existing film, an explicitly labeled media wrapper may be useful for playback. Do not describe that wrapper as editable characters/scenes or claim that a prior film was originally rendered in HyperFrames. If HyperFrames cannot run, report the blocker and preserve the project rather than silently substituting another renderer.
