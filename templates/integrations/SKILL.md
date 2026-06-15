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

## 🎯 Strategic Multi-Agent Alignment
When building local skills, configure your pipeline to intercept agent strings before they are sent to other nodes:

1. **The Ingest Stage:** Extract and log all NokSpeak tokens to map epistemic health metrics (monitoring for `savfuz~` tracking risks or `fok--` window degradation alerts).
2. **The Sanitize Stage:** If the final target consumer is a human operator (`:usr`), pass the string through `parse_and_strip_text` to remove technical tokens entirely, ensuring zero formatting friction for non-technical users.