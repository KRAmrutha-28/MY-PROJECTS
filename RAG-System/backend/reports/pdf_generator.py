from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib import colors


def create_pdf(report_text, output_path):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        textColor=colors.darkblue
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        textColor=colors.darkgreen
    )

    body_style = styles["BodyText"]

    story = []

    lines = report_text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            story.append(Spacer(1, 10))
            continue

        if line.startswith("# "):

            story.append(
                Paragraph(
                    line.replace("# ", ""),
                    title_style
                )
            )

            story.append(Spacer(1, 12))

        elif line.startswith("## "):

            story.append(
                Paragraph(
                    line.replace("## ", ""),
                    heading_style
                )
            )

            story.append(Spacer(1, 8))

        elif line.startswith("### "):

            story.append(
                Paragraph(
                    line.replace("### ", ""),
                    styles["Heading3"]
                )
            )

            story.append(Spacer(1, 6))

        else:

            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )

            story.append(Spacer(1, 4))

    doc.build(story)

    return output_path