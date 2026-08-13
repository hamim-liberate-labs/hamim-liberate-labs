<div align="center">
  <img src="assets/header.svg" alt="Asik Ifthaker Hamim, Associate AI Engineer at Liberate Labs" width="900">
</div>

<div align="center">

[![Email](https://img.shields.io/badge/hamim%40liberate--labs.com-22D3EE?style=for-the-badge&logo=maildotru&logoColor=white&labelColor=0E1428)](mailto:hamim@liberate-labs.com)
[![Repos](https://img.shields.io/badge/what_i_ship-below-A78BFA?style=for-the-badge&logo=github&logoColor=white&labelColor=0E1428)](#selected-work)

</div>

<img src="assets/divider.svg" width="100%" alt="">

## Hello

I am an Associate AI Engineer at Liberate Labs. I build LLM agents and the unglamorous
scaffolding around them: the tool layer, the retrieval, the evals that tell you whether
last week's prompt change actually helped or just felt better.

Most of my work is the gap between a demo that works once and a system that works on a
Tuesday afternoon with real data and a user in a hurry.

<img src="assets/divider.svg" width="100%" alt="">

## The loop I work in

<div align="center">
  <img src="assets/loop.svg" alt="The agent loop: prompt, reason, tool call, observe" width="900">
</div>

Every project I touch is some version of this circuit. The interesting engineering is
almost never in the model call. It is in what the tools return, how failures get
observed and what happens on the retry.

<img src="assets/divider.svg" width="100%" alt="">

## Toolkit

<div align="center">
  <img src="assets/stack.svg" alt="Toolkit: Python, LangGraph, LangChain, Claude, AssemblyAI, Playwright and more" width="900">
</div>

<img src="assets/divider.svg" width="100%" alt="">

## Selected work

<div align="center">
  <img src="assets/status.svg" alt="Featured project status" width="900">
</div>

### [standup-sync](https://github.com/hamim-liberate-labs/standup-sync)

A [Claude Code](https://claude.com/claude-code) plugin for the daily async standup. It
drafts from what you tell it, asks where the update goes, lets you edit it and sends
nothing without an explicit yes. Slack posts come from your own account rather than a bot,
so a standup reply reads as though you typed it.

```
*What have you completed (since last update)?*
• Compared 12 PII detection models on our test data.

*What are you planning on next (include timeline)?*
• Writing up the findings, today.
```

`Python 3.9+` · `Claude Code` · `Slack API` · `ClickUp API` · zero runtime dependencies · tested, CI green

### Not public

Most of what I build day to day lives in private repos. The shape of it:

- **Domain copilots.** Retrieval-backed assistants over messy internal corpora, with the
  routing, guardrails and citation plumbing that decides whether anyone trusts the answer
- **Speech benchmarking.** Multilingual transcription compared across five providers in
  English, Arabic and Bangla, scored on WER and CER rather than on how good the demo felt
- **Browser-driving agents.** LangGraph state machines wrapped around real browser
  automation, which is mostly an exercise in handling everything that goes wrong
- **Document extraction.** OCR pipelines and the evaluation harness that tells you when a
  model swap actually helped

Happy to talk through any of it.

<img src="assets/divider.svg" width="100%" alt="">

## Currently

```yaml
role:      Associate AI Engineer @ Liberate Labs
building:  agent tooling, retrieval pipelines, evaluation harnesses
learning:  making evals boring enough that people actually run them
opinion:   an agent without observability is a rumour
open_to:   collaboration on agent infrastructure and speech work
```

<div align="center">
  <img src="assets/divider.svg" width="100%" alt="">
  <sub><b>Thanks for scrolling.</b> The animations above are hand-written SVG, no third-party image services.</sub>
</div>
