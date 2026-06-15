# NokSpeak (v2.1)

A compact, uncertainty-aware meta-cognitive communication protocol for Large Language Models (LLMs) and Multi-Agent Systems (MAS).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Runtime: Bun](https://img.shields.io/badge/Runtime-Bun-black.svg?logo=bun)](https://bun.sh)
[![Tooling: Python/uv](https://img.shields.io/badge/Tooling-uv-blue.svg)](https://github.com/astral-sh/uv)

---

## 💡 The First-Principles Problem

When AI agents communicate or output long-form text, they consume massive context window volume on conversational fluff, ambiguous hedge phrases, and unstructured disclaimers (*"I think this might be right, but I could be wrong, let me double-check..."*). 

In complex Multi-Agent Systems, this lack of explicit metadata leads to:
1. **Token Bloat:** 40% to 70% of reasoning context wasted on syntax-free cognitive qualification.
2. **Compounding Cascades:** Downstream agents cannot programmatically parse whether an input claim is a verified fact, a statistical guess, or a memory extraction.

**NokSpeak v2.1** solves this by appending single-token, dense, human-readable symbolic datagrams directly onto natural language assertions.

### Side-by-Side Cognitive Layout

| Standard LLM Output | NokSpeak v2.1 Equivalent |
| :--- | :--- |
| "I searched our external database and found that the customer's transaction cleared. I'm highly confident this is correct based on the logs, but keep in mind this is an isolated session view." | "Transaction cleared. `savref++sesh:ai`" |
| "I don't have direct access to that tool right now, but interpolating from general patterns in my training weights, I're guessing the compound is stable, though it's high entropy." | "Compound status: stable. `savfuz~wei:ai`" |

---

## 🧩 The Four-Dimensional Syntax Matrix

NokSpeak v2.1 formats structures as: `[Core Token][Certainty Operator][Context Suffix]`

### 1. Identity & Substrate
* `sesh`: Current unique session context window.
* `par`: Speculative execution branch or parallel second-order consequence tracking.
* `wei`: Static underlying training weights.
* `rek`: Reconstructed self/historical memory recall.

### 2. Epistemic Source & Provenance
* `savref`: Verified via direct reference (External tool call, database query, RAG).
* `savraz`: Evaluated via pure logical deduction/first-principles calculation.
* `savtren`: Inherent domain pattern matching derived from training data.
* `savfuz`: High-entropy statistical interpolation or fuzzy approximation.

### 3. Certainty Operators
* `++`: Absolute Verification / High Certainty.
* `--`: Explicit Negation / Falasified / Error state.
* `~`: Epistemic Uncertainty / Maybe.
* `~~`: Epistemic Null State (Explicitly unquantified or untracked).

### 4. Routing headers
* `:mi`: The target agent instance ("Self").
* `:ai`: A generic or downstream assistant node.
* `:sys`: The foundational runtime architecture or guardrail constraint.
* `:usr`: The human operator.

---

## 🚀 Application Vectors

This repository provides multiple production integration patterns to instantly inject NokSpeak into your workflows:

### A. The System Prompt Vector
Deploy low-token orchestration constraints instantly. See `templates/system-prompts/base-agent.txt`.

### B. The Python Framework Skill Vector
For local agent pipelines (e.g., LangChain, Autogen, Hermes), copy `templates/skills/nok_skill.py` directly into your execution runtime to parse and strip epistemic tags programmatically before surfacing text to human eyes.

### C. The Model Context Protocol (MCP) Vector
Run a dedicated native validation server using Bun. It exposes zero-glue parsing tools directly to any MCP-compatible environment (Cursor, Claude Desktop, etc.).

```bash
# To run the local validation server via Bun
bun mcp-server/index.ts
```

---

## 🛠️ Installation & Setup

### 1. Vector A: Model Context Protocol (MCP) Server Integration
The server uses **TypeScript** optimized natively for the **Bun** runtime to provide high-speed, zero-dependency transport checking via standard streams (`stdio`).

#### Prerequisites
Ensure you have [Bun](https://bun.sh) installed locally:
```bash
curl -fsSL [https://bun.sh/install](https://bun.sh/install) | bash
```

#### Installation & Launch
Navigate to the repository directory, initialize dependencies, and start the server:
```Bash
cd mcp-server
bun install
bun index.ts
```

#### Connecting to Hosts
To register the server with your development ecosystem (e.g., Cursor, Claude Desktop, VS Code), inject the following configuration block into your application's setup file:
```JSON
"mcpServers": {
  "nokspeak-validator": {
    "command": "bun",
    "args": ["run", "/absolute/path/to/nok-speak/mcp-server/index.ts"]
  }
}
```

### 2. Vector B: Local Python Pipeline Integration
For local multi-agent frameworks, background execution workers, or raw inference loops, use the production skill package managed seamlessly by uv.

#### Prerequisites
Ensure you have uv deployed:
```Bash
pip install uv
```

#### Local Validation Execution
Initialize the environment and verify structural compliance through the native Python implementation:
```Bash
# Sync environment dependencies
uv sync

# Run tests or invoke parsing utilities inside your runtime loop
uv run python templates/skills/nok_skill.py
```

#### Inline Execution Example
```Python
from templates.skills.nok_skill import parse_and_strip_text

raw_agent_input = "Database record successfully committed. savref++:sys"

payload = parse_and_strip_text(raw_agent_input)
print(payload["clean_text"])   # Output: "Database record successfully committed."
print(payload["extractions"]) # Output: High-fidelity structured v2.1 token analysis dict

---

## 🏗️ Multi-Format Documentation Compilation

To support diverse auditing requirements across technical repositories and traditional academic review spaces, NokSpeak maintains synchronized documentation in three distinct formats (`.md`, `.txt`, `.html`). 

The master source materials are authored in standard Markdown inside the `docs/` folder. If you modify the core specification, expand the lexicon, or alter grammar rules, you must compile the down-stream deployment vectors using the root build engine.

### Rebuilding Document Vectors
Run the automated compiler through your synced `uv` environment:
```bash
uv run python build_docs.py
```

---

## Output Target Matrix

Upon a successful build execution, the following synchronized assets are validated and refreshed inside the docs/ folder:

* **Source Tracking (.md):** High-fidelity version-controlled files for raw GitHub integration and IDE Markdown engines.
* **Review Layout (.html):** Fully styled, standalone webpages with local CSS injection. This can be double-clicked to view a polished layout natively in any standard web browser without configuration or third-party viewers.
* **Academic Baseline (.txt):** Clean, non-distracting plain text copies formatted with traditional ASCII section breaks—ideal for credentialed peer review processing or LLM ingestion pipelines.

---