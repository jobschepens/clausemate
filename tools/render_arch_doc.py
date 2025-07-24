import re

import markdown
import requests


def render_architecture_doc():
    """Renders the ARCHITECTURE.md file to HTML.

    Converts the DOT graph to SVG using an online service, and adds the Mermaid.js
    script to the HTML.
    """
    with open("docs/ARCHITECTURE.md", encoding="utf-8") as f:
        md_content = f.read()

    # Extract the dot graph
    dot_match = re.search(r"```dot\n(.*?)```", md_content, re.DOTALL)
    if dot_match:
        dot_code = dot_match.group(1)

        # Render the dot code to SVG using quickchart.io
        response = requests.post(
            "https://quickchart.io/graphviz", json={"graph": dot_code}
        )

        if response.status_code == 200:
            with open("docs/project_flow.svg", "w", encoding="utf-8") as f:
                f.write(response.text)

            # Replace the dot code block with an img tag
            md_content = md_content.replace(
                dot_match.group(0), '![Project Flow](project_flow.svg "Project Flow")'
            )
        else:
            print("Failed to render DOT graph. Status code:", response.status_code)

    # Convert markdown to HTML with mermaid support
    html_body = markdown.markdown(md_content, extensions=["markdown_mermaid"])

    # Add mermaid.js script
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Architecture</title>
    </head>
    <body>
        {html_body}
        <script src="https://unpkg.com/mermaid@8.14.0/dist/mermaid.min.js"></script>
        <script>mermaid.initialize({{startOnLoad:true}});</script>
    </body>
    </html>
    """

    with open("docs/ARCHITECTURE.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    render_architecture_doc()
