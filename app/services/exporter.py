import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def export_csv(data, filename):

    df = pd.DataFrame(data)

    df.to_csv(filename, index=False)


def export_pdf(data, filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    for item in data:

        story.append(
            Paragraph(
                f"<b>{item['filename']}</b><br/>{item['summary']}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 12))

    doc.build(story)