# Public design references: Thimble

These ideas come from two public prompts at commit `6cee6e02b3a384bdf0e56c9e7b639ad9ad634635`. They inform presentation; Thimble is not a runtime dependency, and this skill contains no copied implementation.

- [Story prompt](https://github.com/safety-research/thimble/blob/6cee6e02b3a384bdf0e56c9e7b639ad9ad634635/prompts/report-story.md): develop the account through focused beats, connect claims to evidence, and revisit a figure with different highlights as the explanation develops. Keep the limits of the evidence visible. Here, preserve actor/event IDs across the reconstruction and scene notes while choosing visuals appropriate to the incident.
- [Video prompt](https://github.com/safety-research/thimble/blob/6cee6e02b3a384bdf0e56c9e7b639ad9ad634635/prompts/report-video.md): coordinate narration and picture, support repeatable seeking, and inspect actual frames for mismatches and overlaps. Here, use HyperFrames' composition contract and measured speech with acoustic caption alignment; do not copy Thimble's runtime API or estimate final caption timing from word counts.

Choose scene count, pacing and style for the supplied evidence and audience. These public patterns are existing prior work, not claims of novelty. A visually persuasive scene still needs a supported claim and a resolvable source reference.
