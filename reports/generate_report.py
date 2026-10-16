from pathlib import Path
import markdown

BASE_DIR = Path(__file__).resolve().parent

md_path = BASE_DIR / "Netflix_Content_Portfolio_Report.md"
html_path = BASE_DIR / "Netflix_Content_Portfolio_Report.html"

markdown_text = md_path.read_text(encoding="utf-8")

html_body = markdown.markdown(
    markdown_text,
    extensions=["tables", "fenced_code"]
)

html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Netflix Content Portfolio Intelligence</title>

    <style>
        body {{
            font-family: Arial, Helvetica, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 50px;
            line-height: 1.6;
            color: #222;
            background: #fff;
        }}

        h1 {{
            font-size: 34px;
            margin-bottom: 8px;
            border-bottom: 3px solid #E50914;
            padding-bottom: 12px;
        }}

        h2 {{
            margin-top: 38px;
            font-size: 24px;
            color: #111;
        }}

        h3 {{
            margin-top: 25px;
        }}

        p {{
            font-size: 15px;
        }}

        ul, ol {{
            margin-bottom: 20px;
        }}

        li {{
            margin-bottom: 6px;
        }}

        code {{
            background: #f3f3f3;
            padding: 2px 6px;
            border-radius: 4px;
        }}

        pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
        }}

        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }}

        @media print {{
            body {{
                padding: 25px;
            }}

            h2 {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>

<body>

{html_body}

</body>
</html>
"""

html_path.write_text(
    html_template,
    encoding="utf-8"
)

print("Report generated successfully:")
print(html_path)