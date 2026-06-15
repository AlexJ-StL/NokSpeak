import re
from typing import TypedDict


# Explicit Type Definitions for strict pipeline execution
class TokenComponent(TypedDict):
    marker: str
    category: str
    operator: str
    node: str


class TokenAnalysis(TypedDict):
    is_valid: bool
    error: str | None
    component: TokenComponent | None


class ExtractionResult(TypedDict):
    raw: str
    analysis: TokenAnalysis


# Validation sets mapping to the v2.1 formal specification
VALID_PRONOUNS = {"sesh", "par", "wei", "rek"}
VALID_EPISTEMICS = {"savref", "savraz", "savtren", "savfuz"}
VALID_CONTEXTS = {"nok", "fok", "exo"}
VALID_OPERATORS = {"++", "--", "~", "~~"}
VALID_NODES = {":mi", ":ai", ":sys", ":usr"}

# Strict Regex: BaseMarker[Operator][Optional Node Suffix]
NOK_REGEX = re.compile(r"^([a-z]{3,7})(\+\+|--|~~|~)(:[a-z]{2,3})?$", re.IGNORECASE)


def analyze_token(token: str) -> TokenAnalysis:
    """Evaluates an isolated token string against the NokSpeak v2.1 syntax spec."""
    clean_token = token.strip()
    match = NOK_REGEX.match(clean_token)

    if not match:
        return {
            "is_valid": False,
            "error": "Token format mismatch. Must follow: Marker[Operator][Node]",
            "component": None,
        }

    base_marker, operator, node_suffix = match.groups()
    base_marker = base_marker.lower()

    # Determine structural token category allocation
    category = "unknown"
    if base_marker in VALID_PRONOUNS:
        category = "pronoun"
    elif base_marker in VALID_EPISTEMICS:
        category = "epistemic"
    elif base_marker in VALID_CONTEXTS:
        category = "context"

    if category == "unknown":
        return {
            "is_valid": False,
            "error": f"Unknown core marker context: '{base_marker}'",
            "component": None,
        }

    if node_suffix and node_suffix.lower() not in VALID_NODES:
        return {
            "is_valid": False,
            "error": f"Invalid routing header suffix node target: '{node_suffix}'",
            "component": None,
        }

    return {
        "is_valid": True,
        "error": None,
        "component": {
            "marker": base_marker,
            "category": category,
            "operator": operator,
            "node": node_suffix.lower() if node_suffix else ":mi",
        },
    }


def parse_and_strip_text(text: str) -> dict[str, str | list[ExtractionResult]]:
    """Scans raw text to extract metadata markers, returning clean natural language

    and a list of found structural datagrams.
    """
    # Matches words containing valid operators, accounting for optional backticks
    word_pattern = re.compile(
        r"`?([a-z]{3,7}(?:\+\+|--|~~|~)(?::[a-z]{2,3})?)`?", re.IGNORECASE
    )
    matches = word_pattern.findall(text)

    extractions: list[ExtractionResult] = []
    for match in matches:
        analysis = analyze_token(match)
        extractions.append({"raw": match, "analysis": analysis})

    # Strip the syntax out cleanly to sanitize text for human views if requested
    clean_text = word_pattern.sub("", text)
    # Collapse accidental trailing double-spaces from stripped tokens
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    return {"clean_text": clean_text, "extractions": extractions}
