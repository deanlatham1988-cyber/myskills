# DeepTutor — Agent-Native Personalized Learning Assistant

**Repository:** [github.com/HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor)
**Version:** v1.0.0 (April 2026 — ground-up rewrite, ~200k lines)
**License:** Apache 2.0
**Tech stack:** Python 3.11+ / FastAPI, Next.js 16 / React 19
**LLM support:** 30+ providers including OpenAI, Anthropic, DeepSeek, Ollama

---

## What This Tool Does

DeepTutor is an open-source AI learning platform that combines intelligent tutoring with knowledge management. It functions as a self-hosted educational workspace where you can learn, write, research, and solve problems — all powered by AI agents working together.

Upload any document (PDFs, Markdown, text files) into a Knowledge Hub, then interact with the material through multiple modes: chat, deep research, quiz generation, guided learning, and collaborative writing.

---

## Key Features

### Unified Chat Workspace
Five distinct modes — Chat, Deep Solve, Quiz Generation, Deep Research, Math Animator — share a single thread and context, allowing seamless switching between learning approaches.

### Personal TutorBots
Autonomous tutors with individual workspaces, memories, and skills. These agents learn and evolve as you interact with them, powered by the nanobot framework. Each TutorBot maintains persistent memory across sessions.

### Quiz Generation
Auto-generates quizzes from your materials with duplicate prevention. Useful for self-testing on dense academic content or training materials.

### Diagram and Chart Rendering
Built-in visualisation support via Chart.js and SVG rendering. Useful for understanding data-heavy papers or creating visual summaries.

### Co-Writer
A Markdown editor treating AI as a first-class collaborator. Select text and request rewrites, expansions, or summaries while drawing from knowledge bases and web sources.

### Guided Learning
Converts materials into structured learning journeys with multi-step progression, visual HTML pages, and contextual Q&A at each step.

### Knowledge Hub
Manages RAG-ready collections of PDFs, Markdown, and text files organised in colour-coded notebooks.

### Persistent Memory
A user profile tracking study history, learning patterns, and progress — shared across all features and TutorBots.

### Agent-Native CLI
Every capability is accessible via command-line interface with structured JSON output for AI pipelines.

---

## Installation

**Docker (recommended):**
```bash
docker compose up -d
```
Supports both production and development modes with hot-reload.

**Guided setup:**
```bash
python scripts/start_tour.py
```
Interactive configuration with live connection testing.

**Manual install:**
Clone the repo, create a Python environment, install dependencies (`pip install -e ".[server]"` plus npm for frontend), configure `.env`, then start backend and frontend services separately.

**CLI only:**
```bash
pip install -e ".[cli]"
```
Terminal-only access without the web interface.

---

## Use Cases

- **Academic research:** Upload psychology papers or journal articles, use Deep Research to interrogate them, Quiz Generation to test comprehension, Guided Learning to break dense material into structured steps
- **Professional development:** Load training materials, competitor research, or internal docs into the Knowledge Hub for RAG-powered Q&A
- **Study companion:** TutorBots with persistent memory track your learning patterns and adapt over time
- **Document analysis:** Any PDF, Markdown, or text file becomes interactive — ask questions, generate summaries, create visual diagrams

---

## Integration Notes

DeepTutor is a standalone web application — it does not have native MCP integration and runs as its own service. It supports multiple LLM providers via API key configuration, including Anthropic's Claude models.

Search providers supported: Brave, Tavily, Jina, SearXNG, DuckDuckGo, Perplexity.

---

## Source

[DeepTutor — GitHub](https://github.com/HKUDS/DeepTutor)
