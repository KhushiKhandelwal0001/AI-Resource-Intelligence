import re
from collections import Counter


STOP_WORDS = set("""
a an and are as at be been being by can could did do does for from
had has have he her hers him his how i if in into is it its may might
more most must no not of on or our out over she should so than that
the their them then there these they this those through to under up
us was we were what when where which while who why will with would
you your about after again also among any because before between both
but each further here however just other same some such very according
based document report section page information analysis result results
include includes including provide provides using used within across
following overview key main total
""".split())

SIGNAL_WORDS = {
    "increased", "decreased", "grew", "declined", "improved",
    "reduced", "achieved", "reported", "found", "concluded",
    "estimated", "projected", "target", "targets", "compared",
    "higher", "lower", "significant", "challenge", "risk",
    "opportunity", "impact", "result", "outcome", "growth",
    "revenue", "cost", "costs", "investment", "recommendation"
}

RECOMMENDATION_PATTERN = re.compile(
    r"\b(recommend(?:s|ed|ation|ations)?|should|must|need to|"
    r"propose(?:s|d)?|suggest(?:s|ed)?|call for|advise|advises|advised)\b",
    re.IGNORECASE
)

NUMBER_PATTERN = re.compile(
    r"(?:\b\d+(?:,\d{3})*(?:\.\d+)?\s*%|"
    r"\b\d+(?:\.\d+)?\s*(?:million|billion|crore|lakh|thousand)\b|"
    r"(?:INR|USD|EUR|GBP|Rs\.?)\s*\d[\d,.]*)",
    re.IGNORECASE
)


def split_sentences(text):
    """Split extracted text into readable sentence-like units."""
    text = str(text or "").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)

    parts = re.split(r"(?<=[.!?])\s+|\n+", text)

    return [
        part.strip()
        for part in parts
        if len(part.strip()) > 25
    ]


def get_page_evidence(document_data):
    """Extract unique text passages and preserve page references."""
    evidence = []
    pages = document_data.get("pages") or []

    if isinstance(pages, list):
        for page_data in pages:
            if not isinstance(page_data, dict):
                continue

            page_number = page_data.get("page")
            if page_number is None:
                page_number = page_data.get("page_number")

            for sentence in split_sentences(page_data.get("text", "")):
                evidence.append({
                    "text": sentence,
                    "page": page_number
                })

    if not evidence:
        for sentence in split_sentences(document_data.get("text", "")):
            evidence.append({"text": sentence, "page": None})

    unique = []
    seen = set()

    for item in evidence:
        signature = item["text"].casefold()
        if signature in seen:
            continue
        seen.add(signature)
        unique.append(item)

    return unique


def tokenize(text):
    """Return useful lowercase words."""
    words = re.findall(r"\b[a-zA-Z][a-zA-Z-]{2,}\b", str(text).lower())
    return [
        word for word in words
        if word not in STOP_WORDS and len(word) > 2
    ]


def rank_sentence(item):
    """Rank evidence passages using transparent text signals."""
    text = item["text"]
    words = tokenize(text)
    score = 0.0

    if len(words) >= 8:
        score += 1.0

    if NUMBER_PATTERN.search(text):
        score += 2.0

    if re.search(r"\b" + "|".join(SIGNAL_WORDS) + r"\b", text, re.I):
        score += 1.5

    if RECOMMENDATION_PATTERN.search(text):
        score += 1.0

    if len(text) > 220:
        score -= 0.5

    return score


def extract_topics(evidence, limit=10):
    """Rank recurring terms and attach representative evidence."""
    frequencies = Counter()
    sentence_terms = []

    for item in evidence:
        terms = set(tokenize(item["text"]))
        frequencies.update(terms)
        sentence_terms.append((item, terms))

    topics = []

    for term, count in frequencies.most_common(limit * 3):
        if len(topics) >= limit:
            break

        supporting = [
            item for item, terms in sentence_terms
            if term in terms
        ]

        if not supporting:
            continue

        topics.append({
            "topic": term.replace("-", " ").title(),
            "mentions": count,
            "explanation": (
                f"The term '{term}' appears in {count} distinct "
                "extracted passages. Frequency indicates recurrence, "
                "not necessarily importance."
            ),
            "evidence": [
                {"text": item["text"], "page": item["page"]}
                for item in supporting[:3]
            ]
        })

    return topics


def extract_findings(evidence, limit=12):
    """Select potentially important statements; retain source wording."""
    findings = []
    seen = set()

    for item in sorted(evidence, key=rank_sentence, reverse=True):
        text = item["text"]

        has_number = bool(NUMBER_PATTERN.search(text))
        has_signal = bool(
            re.search(
                r"\b(" + "|".join(SIGNAL_WORDS) + r")\b",
                text,
                re.IGNORECASE
            )
        )

        if not (has_number or has_signal):
            continue

        signature = text.casefold()
        if signature in seen:
            continue
        seen.add(signature)

        findings.append({
            "finding": text,
            "page": item["page"],
            "evidence_type": (
                "Quantitative statement" if has_number
                else "Conclusion-oriented statement"
            )
        })

        if len(findings) >= limit:
            break

    return findings


def extract_source_recommendations(evidence, limit=10):
    """Extract statements that may express source recommendations."""
    recommendations = []
    seen = set()

    for item in evidence:
        text = item["text"]

        if not RECOMMENDATION_PATTERN.search(text):
            continue

        signature = text.casefold()
        if signature in seen:
            continue
        seen.add(signature)

        recommendations.append({
            "recommendation": text,
            "page": item["page"],
            "source_status": (
                "Contains recommendation language; verify context"
            )
        })

        if len(recommendations) >= limit:
            break

    return recommendations


def build_detailed_summary(document_data, evidence, topics, findings):
    """Build a structured, extractive overview from source passages."""
    filename = document_data.get("filename") or "Uploaded document"
    text = document_data.get("text", "")
    word_count = document_data.get("word_count", len(text.split()))
    page_count = document_data.get("page_count", 0)

    sections = [
        (
            "DOCUMENT PROFILE\n"
            f"Source: {filename}\n"
            f"Extracted words: {word_count:,}\n"
            f"Extracted pages: {page_count}"
        )
    ]

    if topics:
        sections.append(
            "RECURRING THEMES\n"
            + ", ".join(topic["topic"] for topic in topics[:6])
            + ". These terms recur in the extracted text; their "
              "frequency should not be interpreted as a definitive "
              "measure of business importance."
        )

    representative = sorted(
        evidence, key=rank_sentence, reverse=True
    )[:5]

    if representative:
        sections.append(
            "IMPORTANT SOURCE PASSAGES\n"
            + "\n".join(
                f"- {item['text']}"
                + (f" [Page {item['page']}]" if item["page"] else "")
                for item in representative
            )
        )

    if findings:
        sections.append(
            "POTENTIAL KEY FINDINGS\n"
            + "\n".join(
                f"- {item['finding']}"
                + (f" [Page {item['page']}]" if item["page"] else "")
                for item in findings[:5]
            )
        )

    sections.append(
        "INTERPRETATION NOTE\n"
        "This overview selects and organises passages from extracted "
        "source text. It does not independently verify claims, establish "
        "causation, or replace expert review. Scanned or image-only "
        "content may be missing if OCR was not applied."
    )

    return "\n\n".join(sections)


def analyze_document(document_data):
    """Return a structured analysis compatible with the existing APIs."""
    if not isinstance(document_data, dict):
        raise ValueError("A valid document object is required.")

    text = str(document_data.get("text", "") or "")

    if not text.strip():
        raise ValueError(
            "No readable text was extracted from this document."
        )

    evidence = get_page_evidence(document_data)
    topics = extract_topics(evidence)
    findings = extract_findings(evidence)
    recommendations = extract_source_recommendations(evidence)

    suggested_actions = []

    if not recommendations:
        suggested_actions.append({
            "action": (
                "Review the extracted evidence with a subject-matter "
                "expert and define specific actions appropriate to "
                "the document's purpose."
            ),
            "basis": "General analyst-proposed workflow",
            "source_status": (
                "Proposed action; not identified as a source recommendation"
            )
        })

    summary = build_detailed_summary(
        document_data, evidence, topics, findings
    )

    return {
        "summary": summary,
        "main_topics": topics,
        "key_findings": findings,
        "source_recommendations": recommendations,
        "suggested_actions": suggested_actions,
        "evidence_sentence_count": len(evidence),
        "analysis_method": (
            "Rule-based extractive analysis with evidence ranking"
        ),
        "limitations": [
            "This module does not call a generative language model.",
            "Topic frequency is not equivalent to topic importance.",
            "Selected findings are candidates for review, not independently verified facts.",
            "Page references are available only when supplied by the document extractor.",
            "Scanned or image-only content may be missing if OCR has not been applied."
        ]
    }
