import os
import re

import markdown


def clean_markdown_to_txt(md_content: str) -> str:
    """Strips markdown formatting to create a highly readable plain text file."""
    text = md_content

    # Convert main headers into underlined plaintext section breaks
    text = re.sub(
        r"^# (.*?)$",
        lambda m: f"\n{m.group(1).upper()}\n" + "=" * len(m.group(1)),
        text,
        flags=re.M,
    )
    text = re.sub(
        r"^## (.*?)$",
        lambda m: f"\n{m.group(1)}\n" + "-" * len(m.group(1)),
        text,
        flags=re.M,
    )
    text = re.sub(
        r"^### (.*?)$",
        lambda m: f"\n{m.group(1)}\n" + "~" * len(m.group(1)),
        text,
        flags=re.M,
    )

    # Remove bold/italic markup markers
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # Strip backticks from code text snippets
    text = re.sub(r"`(.*?)`", r"\1", text)

    # Clean up standard blockquote signs
    text = re.sub(r"^>\s?", "", text, flags=re.M)
    return text


def compile_html_page(title: str, body_html: str) -> str:
    """Wraps HTML content in a clean, professional CSS template."""
    font_stack = (
        '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, '
        "Helvetica, Arial, sans-serif"
    )

    css_styles = f"""
        body {{
            font-family: {font_stack};
            line-height: 1.6;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            color: #333;
            background-color: #fdfdfd;
        }}
        h1 {{ border-bottom: 2px solid #333; padding-bottom: 10px; margin-top: 40px; }}
        h2 {{ border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 30px; }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9em;
        }}
        pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
        }}
        pre code {{ background: none; padding: 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #f8f8f8; }}
        blockquote {{
            border-left: 4px solid #0066cc;
            margin: 20px 0;
            padding-left: 15px;
            color: #555;
            font-style: italic;
        }}
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>{css_styles}</style>
</head>
<body>
    {body_html}
</body>
</html>
"""


def main():
    docs_dir = "docs"
    paper_path = os.path.join(docs_dir, "academic-paper.md")
    lexicon_path = os.path.join(docs_dir, "reference-lexicon.md")

    if not os.path.exists(docs_dir):
        print(f"Error: Path '{docs_dir}' directory missing locally.")
        return

    if not os.path.exists(paper_path) or not os.path.exists(lexicon_path):
        print("Error: Target markdown documents missing in docs/ folder structure.")
        return

    print("[BUILD] Compiling dual-vector human documentation...")

    with open(paper_path, encoding="utf-8") as f:
        paper_md = f.read()
    with open(lexicon_path, encoding="utf-8") as f:
        lexicon_md = f.read()

    # Vector 1: Plain Text (.txt)
    with open(os.path.join(docs_dir, "academic-paper.txt"), "w", encoding="utf-8") as f:
        f.write(clean_markdown_to_txt(paper_md))
    with open(
        os.path.join(docs_dir, "reference-lexicon.txt"), "w", encoding="utf-8"
    ) as f:
        f.write(clean_markdown_to_txt(lexicon_md))

    # Vector 2: Beautiful rendered standalone HTML
    extensions = ["extra", "codehilite"]
    paper_html_body = markdown.markdown(paper_md, extensions=extensions)
    lexicon_html_body = markdown.markdown(lexicon_md, extensions=extensions)

    with open(
        os.path.join(docs_dir, "academic-paper.html"), "w", encoding="utf-8"
    ) as f:
        f.write(compile_html_page("NokSpeak v2.1 Academic Paper", paper_html_body))
    with open(
        os.path.join(docs_dir, "reference-lexicon.html"), "w", encoding="utf-8"
    ) as f:
        f.write(compile_html_page("NokSpeak v2.1 Reference Lexicon", lexicon_html_body))

    print("[OK] Build complete! Artifacts generated inside docs/ folder.")


if __name__ == "__main__":
    main()
