
import os
import uuid
from pptx import Presentation

from agents.document_analysis import analyze_document
from agents.ppt_generator import create_document_presentation

text = (
    "The company reported revenue growth of 15% during the year. "
    "The report recommends improving operational efficiency. "
    "Investment in technology increased by 20%. "
    "The organisation identified data quality as a major challenge. "
    "Further analysis should examine costs, productivity and outcomes."
)

document = {
    "filename": "test_report.txt",
    "text": text,
    "word_count": len(text.split()),
    "page_count": 1,
    "pages": [{"page": 1, "text": text}],
}

analysis = analyze_document(document)

os.makedirs("reports", exist_ok=True)
path = os.path.join("reports", f"test_{uuid.uuid4().hex}.pptx")

result = create_document_presentation(document, analysis, path)
presentation = Presentation(path)

print("PowerPoint:", result["filename"])
print("Slides:", len(presentation.slides))
print("File size:", result["size_bytes"], "bytes")
print("Topics:", len(analysis["main_topics"]))
print("Findings:", len(analysis["key_findings"]))

assert len(presentation.slides) == 20, "Slide count is not 20!"
assert os.path.getsize(path) > 0, "PowerPoint file is empty!"

print("PASS: PowerPoint generated with exactly 20 slides.")
