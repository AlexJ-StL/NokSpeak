import pytest

from templates.integrations.nok_skill import (
    VALID_CONTEXTS,
    VALID_EPISTEMICS,
    VALID_NODES,
    VALID_OPERATORS,
    VALID_PRONOUNS,
    analyze_token,
    parse_and_strip_text,
)


class TestAnalyzeToken:
    """Test core token validation logic."""

    # Valid tokens from each category
    @pytest.mark.parametrize(
        "token,expected_category",
        [
            ("sesh++:mi", "pronoun"),
            ("par--:ai", "pronoun"),
            ("wei~:sys", "pronoun"),
            ("rek~~:usr", "pronoun"),
            ("savref++:mi", "epistemic"),
            ("savraz--:ai", "epistemic"),
            ("savtren~:sys", "epistemic"),
            ("savfuz~~:usr", "epistemic"),
            ("nok++:mi", "context"),
            ("fok--:ai", "context"),
            ("exo~:sys", "context"),
        ],
    )
    def test_valid_tokens_return_correct_category(self, token, expected_category):
        result = analyze_token(token)
        assert result["is_valid"] is True
        assert result["component"]["category"] == expected_category
        assert result["error"] is None

    # Invalid tokens
    @pytest.mark.parametrize(
        "token",
        [
            "invalid++:mi",  # Unknown marker
            "seshXX:mi",  # Invalid operator
            "savref++:xx",  # Invalid node
            "notatoken",  # No operator
            "",  # Empty string
            "sesh+++:mi",  # Triple operator
        ],
    )
    def test_invalid_tokens_rejected(self, token):
        result = analyze_token(token)
        assert result["is_valid"] is False
        assert result["error"] is not None

    def test_default_node_assignment(self):
        """Tokens without node suffix should default to :mi"""
        result = analyze_token("savref++")
        assert result["is_valid"] is True
        assert result["component"]["node"] == ":mi"

    def test_case_insensitive_markers(self):
        """Markers should be case-insensitive per regex"""
        result = analyze_token("SAVREF++:MI")
        assert result["is_valid"] is True
        assert result["component"]["marker"] == "savref"

    def test_node_suffix_case_insensitive(self):
        """Node suffixes should be case-insensitive"""
        result = analyze_token("savref++:AI")
        assert result["is_valid"] is True
        assert result["component"]["node"] == ":ai"

    def test_operator_validation(self):
        """All valid operators should work"""
        for op in VALID_OPERATORS:
            result = analyze_token(f"sesh{op}:mi")
            assert result["is_valid"] is True, f"Operator {op} should be valid"

    def test_invalid_operator_rejected(self):
        """Invalid operators should be rejected"""
        result = analyze_token("sesh**:mi")
        assert result["is_valid"] is False


class TestParseAndStripText:
    """Test text parsing and extraction."""

    def test_extracts_multiple_tokens(self):
        text = "Task done. savref++:sys Next step. savraz~:ai"
        result = parse_and_strip_text(text)

        assert len(result["extractions"]) == 2
        assert result["extractions"][0]["raw"] == "savref++:sys"
        assert result["extractions"][1]["raw"] == "savraz~:ai"
        assert "Task done." in result["clean_text"]
        assert "Next step." in result["clean_text"]

    def test_removes_backticks(self):
        text = "Check `savref++:sys` and `savfuz~:ai`"
        result = parse_and_strip_text(text)

        assert len(result["extractions"]) == 2
        assert result["extractions"][0]["raw"] == "savref++:sys"
        assert "`" not in result["clean_text"]

    def test_handles_no_tokens(self):
        text = "Plain text with no markers."
        result = parse_and_strip_text(text)

        assert result["extractions"] == []
        assert result["clean_text"] == text

    def test_collapses_whitespace(self):
        text = "Before  savref++:sys   after"
        result = parse_and_strip_text(text)
        assert "  " not in result["clean_text"]

    def test_preserves_newlines(self):
        text = "Line 1\nsavref++:sys\nLine 2"
        result = parse_and_strip_text(text)
        assert "Line 1" in result["clean_text"]
        assert "Line 2" in result["clean_text"]

    def test_extraction_includes_full_analysis(self):
        text = "Check savref++:sys"
        result = parse_and_strip_text(text)

        assert len(result["extractions"]) == 1
        extraction = result["extractions"][0]
        assert "raw" in extraction
        assert "analysis" in extraction
        assert extraction["analysis"]["is_valid"] is True
        assert extraction["analysis"]["component"]["marker"] == "savref"


class TestConstants:
    """Verify constant sets match specification."""

    def test_pronouns_complete(self):
        assert VALID_PRONOUNS == {"sesh", "par", "wei", "rek"}

    def test_epistemics_complete(self):
        assert VALID_EPISTEMICS == {"savref", "savraz", "savtren", "savfuz"}

    def test_contexts_complete(self):
        assert VALID_CONTEXTS == {"nok", "fok", "exo"}

    def test_operators_complete(self):
        assert VALID_OPERATORS == {"++", "--", "~", "~~"}

    def test_nodes_complete(self):
        assert VALID_NODES == {":mi", ":ai", ":sys", ":usr"}
