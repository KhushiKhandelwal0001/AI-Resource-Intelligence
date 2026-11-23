
import os
import re
import textwrap

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE


# ============================================================
# AI RESOURCE INTELLIGENCE
# EVIDENCE-GROUNDED 20-SLIDE PRESENTATION GENERATOR
# ============================================================

NAVY = RGBColor(22, 39, 69)
BLUE = RGBColor(40, 92, 160)
TEAL = RGBColor(0, 135, 139)
GOLD = RGBColor(220, 165, 60)
WHITE = RGBColor(255, 255, 255)
DARK = RGBColor(42, 52, 65)
MUTED = RGBColor(102, 115, 130)
LIGHT = RGBColor(240, 244, 249)
PALE_BLUE = RGBColor(228, 238, 250)
PALE_TEAL = RGBColor(224, 243, 241)


def clean_text(value, default="Not identified in extracted text"):
    """Convert an arbitrary value into safe, readable presentation text."""
    if value is None:
        return default

    if isinstance(value, (dict, list, tuple)):
        value = str(value)

    text = re.sub(r"\s+", " ", str(value)).strip()
    return text if text else default


def truncate_text(value, limit=1100):
    """Keep slide text readable without silently inventing a summary."""
    text = clean_text(value)
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "…"


def add_text(
    slide,
    text,
    x,
    y,
    w,
    h,
    font_size=18,
    color=DARK,
    bold=False,
    font_name="Aptos",
    align=PP_ALIGN.LEFT,
):
    """Add an editable PowerPoint text box."""
    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )

    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(0.08)
    frame.margin_right = Inches(0.08)
    frame.margin_top = Inches(0.04)
    frame.margin_bottom = Inches(0.04)
    frame.vertical_anchor = MSO_ANCHOR.TOP

    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    paragraph.space_after = Pt(5)

    run = paragraph.add_run()
    run.text = str(text)
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color

    return box


def add_background(slide, color=WHITE):
    """Apply a solid background to a slide."""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_footer(slide, slide_number, filename):
    """Add a consistent footer and slide number."""
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.55), Inches(7.12),
        Inches(12.2), Inches(0.018),
    )
    line.fill.solid()
    line.fill.fore_color.rgb = PALE_BLUE
    line.line.fill.background()

    add_text(
        slide,
        truncate_text(filename, 55),
        0.65, 7.17, 9.7, 0.2,
        font_size=8,
        color=MUTED,
    )

    add_text(
        slide,
        f"{slide_number:02d} / 20",
        11.45, 7.15, 1.15, 0.25,
        font_size=9,
        color=BLUE,
        bold=True,
        align=PP_ALIGN.RIGHT,
    )


def add_header(slide, title, section="DOCUMENT INTELLIGENCE"):
    """Add a title and section label."""
    add_text(
        slide, section.upper(),
        0.7, 0.35, 11.8, 0.25,
        font_size=9, color=TEAL, bold=True,
    )

    add_text(
        slide, truncate_text(title, 120),
        0.7, 0.72, 11.8, 0.65,
        font_size=27, color=NAVY, bold=True,
    )

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.72), Inches(1.48),
        Inches(0.85), Inches(0.055),
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = GOLD
    bar.line.fill.background()


def add_bullet_list(slide, items, x=0.9, y=1.85, w=11.5, h=4.95):
    """Add readable, editable bullet paragraphs."""
    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )

    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(0.08)
    frame.margin_right = Inches(0.1)
    frame.margin_top = Inches(0.05)

    usable = list(items) if items else [
        "Not identified in extracted text."
    ]

    for index, item in enumerate(usable):
        if isinstance(item, dict):
            item = item.get(
                "text",
                item.get(
                    "finding",
                    item.get(
                        "recommendation",
                        item.get("action", str(item)),
                    ),
                ),
            )

        paragraph = (
            frame.paragraphs[0]
            if index == 0
            else frame.add_paragraph()
        )

        paragraph.text = truncate_text(item, 520)
        paragraph.level = 0
        paragraph.space_after = Pt(12)
        paragraph.font.name = "Aptos"
        paragraph.font.size = Pt(16 if len(usable) <= 4 else 13)
        paragraph.font.color.rgb = DARK
        paragraph.bullet = True

    return box


def add_paragraph_slide(slide, title, paragraphs, section="ANALYSIS"):
    """Add a narrative slide with multiple readable paragraphs."""
    add_background(slide)
    add_header(slide, title, section)

    y = 1.8
    paragraphs = paragraphs or [
        "Not identified in extracted text."
    ]

    for paragraph in paragraphs[:4]:
        paragraph = truncate_text(paragraph, 1350)
        estimated_lines = max(2, len(paragraph) // 105 + 1)
        height = min(1.48, max(0.72, estimated_lines * 0.24))

        add_text(
            slide, paragraph,
            0.85, y, 11.6, height,
            font_size=15, color=DARK,
        )
        y += height + 0.17

        if y > 6.65:
            break


def add_list_slide(slide, title, items, section="EVIDENCE"):
    """Add a slide with a structured evidence list."""
    add_background(slide)
    add_header(slide, title, section)
    add_bullet_list(slide, items)


def add_reference(item):
    """Format an evidence item with its available page reference."""
    if isinstance(item, dict):
        content = item.get(
            "text",
            item.get(
                "finding",
                item.get(
                    "recommendation",
                    item.get("action", ""),
                ),
            ),
        )
        page = item.get("page")
        reference = f" [Page {page}]" if page else ""
        return truncate_text(clean_text(content) + reference, 520)

    return truncate_text(item, 520)


def create_document_presentation(
    document_data,
    analysis,
    output_path,
):
    """
    Create a professional, editable PowerPoint with exactly 20 slides.

    All substantive content is taken from the extracted document or
    its analysis. Missing evidence is explicitly labelled rather than
    replaced with fabricated claims.
    """
    if not isinstance(document_data, dict):
        raise ValueError("document_data must be a dictionary.")

    if not isinstance(analysis, dict):
        analysis = {}

    source_text = clean_text(
        document_data.get("text", ""),
        default="",
    )

    if not source_text:
        raise ValueError(
            "The document contains no extracted text. "
            "Upload a readable document first."
        )

    filename = clean_text(
        document_data.get("filename"),
        "Uploaded document",
    )

    page_count = document_data.get("page_count", 0)
    word_count = document_data.get(
        "word_count",
        len(source_text.split()),
    )

    topics = analysis.get("main_topics") or []
    findings = analysis.get("key_findings") or []
    recommendations = analysis.get("source_recommendations") or []
    proposed_actions = analysis.get("suggested_actions") or []

    summary = analysis.get("summary") or (
        "A detailed summary was not supplied by the analysis module. "
        "Refer to the extracted document and evidence slides."
    )

    topic_names = [
        clean_text(
            topic.get("topic", "Unnamed topic")
            if isinstance(topic, dict)
            else topic
        )
        for topic in topics
    ]

    evidence = []
    for topic in topics:
        if isinstance(topic, dict):
            for item in topic.get("evidence", []):
                evidence.append(add_reference(item))

    evidence = list(dict.fromkeys(evidence))

    finding_text = [
        add_reference(item) for item in findings
    ]

    recommendation_text = [
        add_reference(item) for item in recommendations
    ]

    action_text = []
    for action in proposed_actions:
        if isinstance(action, dict):
            action_text.append(
                clean_text(action.get("action"))
                + " (Analyst-proposed; not a source quotation.)"
            )
        else:
            action_text.append(
                clean_text(action)
                + " (Analyst-proposed.)"
            )

    if not action_text:
        action_text = [
            "Review the source evidence with relevant stakeholders "
            "before defining actions. This is a proposed workflow, "
            "not a recommendation attributed to the source."
        ]

    # Split source-grounded text into presentation-friendly passages.
    source_sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", source_text)
        if len(sentence.strip()) > 45
    ]

    if not source_sentences:
        source_sentences = [source_text[:1500]]

    representative = list(dict.fromkeys(source_sentences))[:4]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    def new_slide(title, items=None, section="ANALYSIS"):
        slide = prs.slides.add_slide(blank_layout)
        add_list_slide(slide, title, items or [], section)
        return slide

    # --------------------------------------------------------
    # SLIDE 1: TITLE
    # --------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_background(slide, NAVY)

    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0), Inches(0.2), Inches(7.5),
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = GOLD
    accent.line.fill.background()

    add_text(
        slide, "AI RESOURCE INTELLIGENCE",
        0.95, 1.05, 11.3, 0.4,
        font_size=13, color=RGBColor(105, 220, 207), bold=True,
    )

    add_text(
        slide, "Document Intelligence\n& Evidence Review",
        0.95, 1.8, 11.3, 1.65,
        font_size=34, color=WHITE, bold=True,
    )

    add_text(
        slide, truncate_text(filename, 150),
        1.0, 4.0, 10.9, 0.85,
        font_size=20, color=RGBColor(224, 233, 245),
    )

    add_text(
        slide,
        f"{word_count:,} extracted words  |  "
        f"{page_count} extracted pages",
        1.0, 5.35, 10.9, 0.4,
        font_size=13, color=WHITE,
    )

    add_text(
        slide,
        "Evidence-grounded analysis • Editable presentation",
        1.0, 6.15, 10.9, 0.35,
        font_size=11, color=RGBColor(195, 208, 226),
    )

    # --------------------------------------------------------
    # SLIDE 2: EXECUTIVE OVERVIEW
    # --------------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    add_paragraph_slide(
        slide,
        "Executive Overview",
        [
            truncate_text(summary, 1400),
            (
                "This presentation organises extracted content, recurring "
                "topics, findings, and recommendations. Interpretation "
                "should be checked against the source document."
            ),
        ],
        "EXECUTIVE BRIEF",
    )

    # --------------------------------------------------------
    # SLIDE 3: DOCUMENT PROFILE
    # --------------------------------------------------------
    new_slide(
        "Document Profile & Scope",
        [
            f"Source file: {filename}",
            f"Extracted word count: {word_count:,}",
            f"Extracted page count: {page_count}",
            f"Evidence sentences identified: "
            f"{analysis.get('evidence_sentence_count', 'Not recorded')}",
            f"Analysis method: {analysis.get('analysis_method', 'Not specified')}",
            "Scope: text successfully extracted from the uploaded file.",
        ],
        "DOCUMENT PROFILE",
    )

    # --------------------------------------------------------
    # SLIDE 4: METHOD AND LIMITATIONS
    # --------------------------------------------------------
    limitations = analysis.get("limitations") or [
        "Interpretations depend on the text extracted from the file.",
        "Scanned pages may require OCR before their content is available.",
        "Topic frequency alone does not establish importance.",
    ]

    new_slide(
        "Methodology & Limitations",
        [
            "The presentation uses the supplied document and analysis results.",
            "Supporting page references are shown when available.",
        ] + list(limitations)[:4],
        "METHODOLOGY",
    )

    # --------------------------------------------------------
    # SLIDE 5: DETAILED SUMMARY
    # --------------------------------------------------------
    summary_paragraphs = [
        part.strip()
        for part in str(summary).split("\n\n")
        if part.strip()
    ]

    add_paragraph_slide(
        prs.slides.add_slide(blank_layout),
        "Detailed Document Summary",
        summary_paragraphs or [summary],
        "DOCUMENT SUMMARY",
    )

    # --------------------------------------------------------
    # SLIDE 6: MAIN THEMES
    # --------------------------------------------------------
    new_slide(
        "Main Topics Identified",
        [
            (
                f"{topic.get('topic', 'Topic')} — "
                f"{topic.get('mentions', 'N/A')} mentions"
            )
            if isinstance(topic, dict)
            else str(topic)
            for topic in topics[:12]
        ],
        "THEMATIC ANALYSIS",
    )

    # --------------------------------------------------------
    # SLIDES 7-9: TOPIC DETAIL
    # --------------------------------------------------------
    for index in range(3):
        topic = topics[index] if index < len(topics) else None

        if isinstance(topic, dict):
            topic_name = clean_text(topic.get("topic"))
            topic_explanation = clean_text(topic.get("explanation"))
            topic_evidence = topic.get("evidence") or []

            paragraphs = [
                topic_explanation,
                *[
                    add_reference(item)
                    for item in topic_evidence[:3]
                ],
            ]
        elif topic is not None:
            topic_name = clean_text(topic)
            paragraphs = [
                "The topic name was supplied by the analysis module. "
                "A separate explanation or supporting excerpt was "
                "not supplied for this topic."
            ]
        else:
            topic_name = f"Topic {index + 1}: Evidence unavailable"
            paragraphs = [
                "No additional topic was identified in the supplied "
                "analysis. No topic-specific claim has been invented."
            ]

        add_paragraph_slide(
            prs.slides.add_slide(blank_layout),
            f"Topic Deep Dive: {topic_name}",
            paragraphs,
            "THEMATIC ANALYSIS",
        )

    # --------------------------------------------------------
    # SLIDE 10: QUANTITATIVE EVIDENCE
    # --------------------------------------------------------
    numeric_pattern = re.compile(
        r"(?:\d+(?:,\d{3})*(?:\.\d+)?\s*%|"
        r"[₹$€£]\s*\d[\d,.]*|"
        r"\b\d+(?:\.\d+)?\s*"
        r"(?:million|billion|crore|lakh|thousand)\b)",
        re.IGNORECASE,
    )

    metrics = [
        sentence for sentence in source_sentences
        if numeric_pattern.search(sentence)
    ]

    new_slide(
        "Quantitative Facts & Metrics",
        [
            truncate_text(sentence, 400)
            for sentence in list(dict.fromkeys(metrics))[:10]
        ] or [
            "No matching numeric statements were identified in the "
            "extracted text. This does not prove that the source "
            "contains no quantitative information."
        ],
        "QUANTITATIVE EVIDENCE",
    )

    # --------------------------------------------------------
    # SLIDES 11-12: FINDINGS AND IMPLICATIONS
    # --------------------------------------------------------
    new_slide(
        "Evidence-Based Key Findings",
        finding_text[:8] or [
            "No qualifying findings were identified by the extraction "
            "rules. Review the original document for additional evidence."
        ],
        "KEY FINDINGS",
    )

    add_paragraph_slide(
        prs.slides.add_slide(blank_layout),
        "Findings: Interpretation & Context",
        [
            (
                "The findings listed in this presentation are extracted "
                "statements selected by evidence-oriented text patterns. "
                "They have not automatically been verified as causal "
                "relationships or independently validated facts."
            ),
            *[
                truncate_text(item, 450)
                for item in finding_text[8:12]
            ],
        ],
        "FINDINGS REVIEW",
    )

    # --------------------------------------------------------
    # SLIDE 13: SOURCE RECOMMENDATIONS
    # --------------------------------------------------------
    new_slide(
        "Recommendations Stated in the Source",
        recommendation_text[:10] or [
            "No explicit recommendation statements were identified "
            "by the extraction rules. This does not establish that "
            "the source contains no recommendations."
        ],
        "SOURCE RECOMMENDATIONS",
    )

    # --------------------------------------------------------
    # SLIDE 14: PROPOSED ACTIONS
    # --------------------------------------------------------
    new_slide(
        "Proposed Action Plan — Analyst Suggestions",
        action_text[:8],
        "PROPOSED ACTIONS",
    )

    # --------------------------------------------------------
    # SLIDE 15: OPPORTUNITIES
    # --------------------------------------------------------
    opportunity_items = [
        f"Review the source evidence relating to {name}."
        for name in topic_names[:6]
    ]

    new_slide(
        "Potential Opportunities for Further Review",
        opportunity_items or [
            "Review the source document with relevant subject-matter "
            "experts to identify opportunities."
        ],
        "OPPORTUNITY REVIEW",
    )

    # --------------------------------------------------------
    # SLIDE 16: RISKS AND DATA GAPS
    # --------------------------------------------------------
    new_slide(
        "Risks, Caveats & Data Gaps",
        [
            "Text extraction may omit information contained only in images.",
            "Numeric statements should be checked against their original context.",
            "The analysis may not capture relationships across distant sections.",
            "No external fact-checking is implied by this presentation.",
        ] + list(limitations)[:3],
        "RISK & QUALITY REVIEW",
    )

    # --------------------------------------------------------
    # SLIDE 17: STAKEHOLDERS
    # --------------------------------------------------------
    add_paragraph_slide(
        prs.slides.add_slide(blank_layout),
        "Stakeholder Considerations",
        [
            "The extracted analysis does not establish a definitive "
            "stakeholder list.",
            "Relevant stakeholders should be identified based on the "
            "document's subject, intended use, and organisational context.",
            (
                "Before acting on a finding, confirm its source, date, "
                "scope, and applicability with the responsible subject "
                "matter owner."
            ),
        ],
        "STAKEHOLDER REVIEW",
    )

    # --------------------------------------------------------
    # SLIDE 18: IMPLEMENTATION ROADMAP
    # --------------------------------------------------------
    new_slide(
        "Suggested Review & Implementation Roadmap",
        [
            "Stage 1 — Validate important statements against the source.",
            "Stage 2 — Confirm key figures, dates, and page references.",
            "Stage 3 — Discuss source recommendations with stakeholders.",
            "Stage 4 — Approve any proposed actions with accountable owners.",
            "Stage 5 — Define measurable outcomes and review progress.",
            "This roadmap is a proposed workflow, not a source quotation.",
        ],
        "IMPLEMENTATION",
    )

    # --------------------------------------------------------
    # SLIDE 19: CONCLUSION
    # --------------------------------------------------------
    add_paragraph_slide(
        prs.slides.add_slide(blank_layout),
        "Conclusion & Next Steps",
        [
            truncate_text(summary, 1000),
            (
                "The next step is to validate important evidence, review "
                "the cited source passages, and distinguish the source's "
                "own conclusions from analyst interpretation."
            ),
        ],
        "CONCLUSION",
    )

    # --------------------------------------------------------
    # SLIDE 20: REFERENCES AND EXTRACTION NOTES
    # --------------------------------------------------------
    reference_items = [
        f"Primary source: {filename}",
        f"Extracted pages: {page_count}",
        f"Extracted words: {word_count:,}",
    ]

    reference_items.extend(
        f"Supporting excerpt: {item}"
        for item in evidence[:5]
    )

    if not evidence:
        reference_items.append(
            "Topic-specific excerpts were not supplied by the analysis."
        )

    reference_items.append(
        "Page numbers are included only when supplied by the extractor."
    )

    new_slide(
        "References & Extraction Notes",
        reference_items[:10],
        "REFERENCES",
    )

    # Apply footer to all slides.
    for index, slide in enumerate(prs.slides, start=1):
        if index != 1:
            add_footer(slide, index, filename)

    # Guarantee the required slide count before saving.
    if len(prs.slides) != 20:
        raise RuntimeError(
            f"Expected exactly 20 slides; generated {len(prs.slides)}."
        )

    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)

    if not os.path.isfile(output_path):
        raise RuntimeError("The PowerPoint file was not created.")

    return {
        "path": output_path,
        "slide_count": len(prs.slides),
        "filename": os.path.basename(output_path),
        "size_bytes": os.path.getsize(output_path),
    }
