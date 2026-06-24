# NokSpeak Integration: Agent Skills

This directory provides templates and code files for injecting NokSpeak v2.1 validation logic directly into local agent frameworks (such as Autogen, LangChain, or custom loops) without requiring an external network-hosted service or a separate Model Context Protocol (MCP) server layer.

## 🛠️ Integration Patterns

### 1. Declarative Schema Injection (`tool-definition.json`)
For standard tool-calling models (e.g., GPT-4o, Claude 3.5 Sonnet), provide the `tool-definition.json` schema to the model at initialization. This lets the orchestrator route text validation directly through the model's native function-calling interface.

### 2. Native Script Execution (`nok_skill.py`)
If you are developing inside a Python ecosystem managed with `uv`, you can drop `nok_skill.py` directly into your processing pipeline. This allows you to evaluate tags or scrub text programmatically before it hits log outputs or consumer UIs.

```python
from templates.integrations.nok_skill import parse_and_strip_text

# Ingest raw multi-agent datagrams
raw_output = "Inference complete. Target compound structure maps accurately. savtren++"

# Clean text and isolate metadata objects
result = parse_and_strip_text(raw_output)

print(result["clean_text"])   # "Inference complete. Target compound structure maps accurately."
print(result["extractions"]) # Contains deep dict analysis of the 'savtren++' token
```

### 3. Version Prefix Support (v2.1)
Tokens may include an optional version prefix for cross-version compatibility:

```python
# Both valid:
parse_and_strip_text("Record updated. savref++:sys")
parse_and_strip_text("nok2.1:Record updated. savref++:sys")
```

The parser returns a `version` field in the component analysis, defaulting to `"n/a"` for unprefixed tokens.

### 4. Certainty Calibration
The reference lexicon includes a calibration guide mapping operators to confidence ranges:
- `++` → 95-100% (verified, deterministic)
- `~` → 60-90% (strong inference)
- `~~` → 0-60% (genuine unknown)
- `--` → N/A (negation/refusal)

Use this to maintain consistency across different models in a multi-agent system.

## 🎯 Strategic Multi-Agent Alignment
When building local skills, configure your pipeline to intercept agent strings before they are sent to other nodes:

1. **The Ingest Stage:** Extract and log all NokSpeak tokens to map epistemic health metrics (monitoring for `savfuz~` tracking risks or `fok--` window degradation alerts).
2. **The Sanitize Stage:** If the final target consumer is a human operator (`:usr`), pass the string through `parse_and_strip_text` to remove technical tokens entirely, ensuring zero formatting friction for non-technical users.
3. **The Audit Stage:** Use `savtren` subtypes to distinguish domain facts (`savtren++`) from unverified inferences (`savtren~`) — flag the latter for tool verification before propagating downstream.