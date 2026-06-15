import os

from build_docs import clean_markdown_to_txt, compile_html_page, main


class TestCleanMarkdownToTxt:
    """Test markdown to text conversion."""

    def test_headers_converted(self):
        md = "# Title\n## Subtitle\n### Sub-sub"
        txt = clean_markdown_to_txt(md)

        assert "TITLE" in txt
        assert "=" * 5 in txt  # underline for H1
        assert "Subtitle" in txt
        assert "-" * 8 in txt  # underline for H2
        assert "Sub-sub" in txt
        assert "~" * 7 in txt  # underline for H3

    def test_bold_italic_removed(self):
        md = "**bold** and *italic*"
        txt = clean_markdown_to_txt(md)
        assert txt == "bold and italic"

    def test_code_backticks_removed(self):
        md = "Use `code` here"
        txt = clean_markdown_to_txt(md)
        assert txt == "Use code here"

    def test_blockquotes_cleaned(self):
        md = "> quoted text"
        txt = clean_markdown_to_txt(md)
        assert txt == "quoted text"

    def test_multiple_headers(self):
        md = "# H1\n## H2\n### H3\n#### H4"
        txt = clean_markdown_to_txt(md)
        # H4 not handled, should remain as plain text
        assert "H1" in txt
        assert "H2" in txt
        assert "H3" in txt


class TestCompileHtmlPage:
    """Test HTML template generation."""

    def test_generates_valid_html(self):
        html = compile_html_page("Test", "<p>Content</p>")

        assert "<!DOCTYPE html>" in html
        assert "<title>Test</title>" in html
        assert "<p>Content</p>" in html
        assert "font-family" in html
        assert "max-width: 800px" in html

    def test_includes_css(self):
        html = compile_html_page("Test", "<p>Content</p>")
        assert "<style>" in html
        assert "body {" in html

    def test_special_chars_escaped(self):
        html = compile_html_page("Test & Title", "<p>Content</p>")
        assert "Test & Title" in html


class TestMainFunction:
    """Test main build process (integration)."""

    def test_creates_output_files(self, tmp_path):
        # Create test markdown files
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        (docs_dir / "academic-paper.md").write_text("# Test Paper\n\nContent")
        (docs_dir / "reference-lexicon.md").write_text("# Test Lexicon\n\nContent")

        # Change to temp dir and run
        old_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            main()

            # Check outputs exist
            assert (docs_dir / "academic-paper.txt").exists()
            assert (docs_dir / "academic-paper.html").exists()
            assert (docs_dir / "reference-lexicon.txt").exists()
            assert (docs_dir / "reference-lexicon.html").exists()
        finally:
            os.chdir(old_cwd)

    def test_output_content_correct(self, tmp_path):
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        paper_content = "# Test Paper\n\n**Bold** and `code`"
        lexicon_content = "# Test Lexicon\n\n> Quote"

        (docs_dir / "academic-paper.md").write_text(paper_content)
        (docs_dir / "reference-lexicon.md").write_text(lexicon_content)

        old_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            main()

            # Check TXT output
            txt_content = (docs_dir / "academic-paper.txt").read_text()
            assert "TEST PAPER" in txt_content
            assert "Bold" in txt_content  # markdown removed
            assert "code" in txt_content  # backticks removed

            # Check HTML output
            html_content = (docs_dir / "academic-paper.html").read_text()
            assert "<h1>Test Paper</h1>" in html_content
            assert "<strong>Bold</strong>" in html_content
            assert "<code>code</code>" in html_content
        finally:
            os.chdir(old_cwd)
