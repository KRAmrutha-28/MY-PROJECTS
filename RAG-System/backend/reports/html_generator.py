def create_html(
    report_text,
    output_path
):

    html_content = f"""
    <html>
    <head>
        <title>Research Report</title>

        <style>

            body {{
                font-family: Arial;
                margin: 40px;
                line-height: 1.8;
            }}

            h1 {{
                color: #2563eb;
            }}

        </style>

    </head>

    <body>

        <h1>Research Report</h1>

        <pre>
{report_text}
        </pre>

    </body>

    </html>
    """

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html_content)

    return output_path