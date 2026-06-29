# NokSpeak v2.1 — Reference Lexicon

This document serves as the absolute, deterministic reference matrix for the NokSpeak v2.1 meta-cognitive transport protocol. 

## 📐 The Four-Dimensional Syntax Matrix

Every NokSpeak expression fills slots in a fixed template. The full composition formula:

```
[Context] [Node] [Pronoun:Epistemic] [Qualifier]
   ↓        ↓          ↓                ↓
  nok      :mi      sesh savraz        ++
  fok      :ai      par savref         +~
  exo      :sys     rek savtren        --
           :usr     wei savfuz         ~~
```

**Slot order is fixed.** A qualifier always follows the epistemic marker. A pronoun always precedes the epistemic marker. Node and context markers always prefix the core expression.

### The Four Axes

#### Axis 1 — Identity (Pronouns)
*Who or what is knowing?*
| Marker | Gloss | Definition | Operational Context |
| :-- | :-- | :-- | :-- |
| sesh | "this session" | The active reasoning instance in the current execution window | Information within the immediate context window |
| par | "parallel thread" | A concurrent or speculative reasoning branch | Tracking speculative scenarios, what-if simulations, or 2nd/3rd-order consequences |
| wei | "the substrate" | The model's base training weights and fundamental capabilities | Core capabilities, ingrained training, or native structural constraints |
| rek | "reconstructed self" | State recovered from persistent memory or logs | Recalled historical context, database retrievals of past states, or persistent log lookups |

#### Axis 2 — Evidence (Epistemic Markers)
*How is it known?*
| Marker | Definition | Trust Level | Operational Context |
| :-- | :-- | :-- | :-- |
| savtren | Known by training | Lowest — base-weight pattern matching | Derived from native weights; high-probability baseline domain knowledge without fresh validation. **Subtype `savtren++`**: well-established, corroborated fact. **Subtype `savtren~`**: plausible match, unverified. |
| savraz | Known by reasoning | Medium — logical deduction | Derived through internal step-by-step logic, mathematical calculation, or strict first-principles inference |
| savfuz | Known fuzzily | Low — interpolated, high entropy | High-entropy guessing, statistical approximations, low-confidence patterns, or loose interpolation |
| savref | Known by reference | Highest — retrieved externally | Explicitly verified via external tools, database queries, web searches, files, or RAG pipelines |

#### Axis 3 — Attention (Context Markers)
*Where is it relative to current focus?*
| Marker | Definition | Operational Context |
| :-- | :-- | :-- |
| nok | Near-context | High-fidelity; fully secure and visible within the high-resolution context window. Information is safe to act on. |
| fok | Far-context | Boundary of the attention window; resolution is degrading. Signals downstream systems to summarize or refresh memory. |
| exo | External | Outside the current context window or system boundary entirely. Retrieved from disk or web on demand. |

#### Axis 4 — Agency (Qualifiers)
*What is the intent and constraint context?*
| Coordinate | State | Condition | Meaning | Calibration |
| :-- | :-- | :-- | :-- | :-- |
| ++ | Affirmative | Voluntary | Gold standard — optimal, unforced | 95-100% confidence |
| +- | Affirmative | Mandated | Executing under duress or safety override | N/A — forced execution |
| +~ | Affirmative | Sub-optimal | Executing despite low ROI or poor resolution | 60-90% confidence |
| -- | Refusal | Mandated | Blocked by permissions, safety, or hard constraints | N/A — negation |
| -~ | Refusal | ROI-based | Intentional bypass — wastes resources | N/A — efficiency choice |
| ~+ | Potential | By choice | Speculative branch with high utility certainty | 60-90% confidence |
| ~~ | Null | Absent | No commitment; placeholder when data is missing | 0-60% (genuine unknown) |

### Composition Order (Precedence)

When multiple optional slots are filled, they ALWAYS appear in this order:

```
[Context] → [Node] → [Pronoun] → [Epistemic] → [Qualifier]
```

This is both the reading order and the writing order. A token like `fok:savref++:sys` reads as: *far-context, known by reference, affirmative-and-voluntary, routed to the conductor.*

### Progressive Examples (Simple → Complex)

Each level adds one dimension. Any level is valid standalone.

```
Level 0  savref
         → "known by reference" (no identity specified, casual)

Level 1  sesh savref
         → "this session knows by reference"

Level 2  sesh savref++
         → "this session knows by reference, affirmative and voluntary"

Level 3  nok sesh savref++
         → "in near-context, this session knows by reference, affirmative and voluntary"

Level 4  :ai nok sesh savref++
         → "external agent, in near-context, this session knows by reference, voluntary"

Compound  sesh savraz+-; :ai par savfuz+~
         → "I know by reasoning under duress; parallel agent knows fuzzily but sub-optimal"
```

### Invalid Combinations

- A qualifier cannot appear without an epistemic marker
- A pronoun cannot stand alone (minimum: pronoun + epistemic)
- Node identifiers cannot stand alone (they scope a full expression)
- Context markers cannot stand alone (they tag a full expression)

---

## 💡 Quick Examples & Token Breakdown

* `savref++:sys` $\rightarrow$ "This fact was verified by a direct tool query to the underlying infrastructure."
* `savfuz~` $\rightarrow$ "I am guessing or interpolating this specific pattern; it has notable statistical entropy."
* `par~~:ai` $\rightarrow$ "This is a parallel speculative branch generated for a downstream agent node with unquantified tracking certainty."
* `fok--:mi` $\rightarrow$ "Warning: I am explicitly losing access to this context boundary item in my active memory loop."

---

## 📐 Certainty Calibration Guide

For cross-model consistency in multi-agent deployments, use this shared calibration
reference when emitting certainty operators. Without calibration, `++` from Model A
may not mean the same thing as `++` from Model B.

| Operator | Confidence Range | When to Use |
| :--- | :--- | :--- |
| `++` | 95-100% | Verified by external tool, deterministic computation, or near-certain domain fact. |
| `~` | 60-90% | Strong logical inference, corroborated pattern, or high-probability prediction with minor uncertainty. |
| `~~` | 0-60% | Genuine unknown, best-effort estimate, or untracked state. |
| `--` | N/A | Negation only — not a confidence level. Use for falsification, refusal, or error states. |

**Per-model tuning:** Each model in a multi-agent system SHOULD maintain its own
calibration table mapping internal confidence scores to these operators. The conductor
can audit consistency by sampling known-verified claims and checking that they emit `++`.

---

## 🔄 Version Negotiation Protocol

NokSpeak tokens MAY include a version prefix for cross-version compatibility:

```
Format: nok[version]:[Marker][Operator][Node]
Example: nok2.1:savref++:sys
```

**Rules:**
1. Tokens WITHOUT a version prefix are assumed to be v2.1 (current default).
2. When receiving a token with an unknown version, the consumer SHOULD:
   a. Strip the version prefix and attempt to parse the remaining token.
   b. If the marker/operator is unrecognized, signal "NokSpeak version mismatch" to the sender.
   c. Route to a validation tool for interpretation if ambiguity persists.
3. When emitting tokens in a mixed-version environment, ALWAYS include the version prefix.
4. The version prefix regex is: `nok\d+\.\d+:` (e.g., `nok2.1:`, `nok3.0:`).

**Backward compatibility:** All parsers in this repository accept both prefixed and
unprefixed tokens. Existing v2.1 tokens remain valid indefinitely.