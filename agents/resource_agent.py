


# ============================================================
# AI RESOURCE INTELLIGENCE
# RESOURCE INTELLIGENCE AGENT
# EXACT SEARCH + HYBRID RAG + PAGE-AWARE EVIDENCE
# ============================================================

import re

from rag.retriever import search_document


# ============================================================
# CONFIGURATION
# ============================================================

MAX_EXACT_RESULTS = 8
MAX_RAG_RESULTS = 5

# Words that usually do not help identify the requested evidence.
STOP_WORDS = {
    "a", "an", "and", "or", "the", "to", "of",
    "in", "on", "at", "by", "from", "with",
    "for", "about", "what", "which", "who",
    "when", "where", "why", "how", "is", "are",
    "was", "were", "be", "been", "being",
    "do", "does", "did", "can", "could",
    "would", "should", "will", "it", "this",
    "that", "these", "those", "my", "your",
    "their", "me", "please", "tell", "show",
    "give", "find", "search", "explain",
    "describe", "information", "details",
    "document", "uploaded", "page", "mention",
    "mentions", "mentioned"
}


# ============================================================
# TEXT HELPERS
# ============================================================

def normalize_text(text):
    """Normalize whitespace without changing the original meaning."""

    if text is None:
        return ""

    text = str(text)
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def tokenize(text):
    """Extract lowercase searchable terms."""

    return set(
        token.lower()
        for token in re.findall(
            r"[A-Za-z0-9][A-Za-z0-9+#./-]*",
            normalize_text(text)
        )
        if len(token) > 1
    )


def get_meaningful_words(question):
    """Remove conversational stop words from a question."""

    return {
        word
        for word in tokenize(question)
        if word not in STOP_WORDS
    }


def split_into_searchable_units(text):
    """
    Split document content into reasonably small units.

    Sentence-level matching reduces the chance that an unrelated
    sentence elsewhere in a long document is returned as evidence.
    """

    text = normalize_text(text)

    if not text:
        return []

    units = re.split(
        r"\n+|(?<=[.!?])\s+",
        text
    )

    return [
        unit.strip()
        for unit in units
        if unit.strip()
    ]


# ============================================================
# DOCUMENT TEXT EXTRACTION
# ============================================================

def extract_document_units(document_data):
    """
    Return searchable document units with page metadata.

    Supports:
        {"text": "..."}
        {"pages": [{"page": 1, "text": "..."}]}
        {"pages": [{"page_number": 1, "text": "..."}]}
    """

    if isinstance(document_data, str):
        document_data = {"text": document_data}

    if not isinstance(document_data, dict):
        return []

    units = []
    pages = document_data.get("pages", [])

    if isinstance(pages, list) and pages:

        for page in pages:

            if not isinstance(page, dict):
                continue

            page_number = page.get("page_number")

            if page_number is None:
                page_number = page.get("page")

            page_text = normalize_text(
                page.get("text", "")
            )

            for sentence in split_into_searchable_units(
                page_text
            ):
                units.append({
                    "text": sentence,
                    "page": page_number
                })

    else:

        text = normalize_text(
            document_data.get("text", "")
        )

        for sentence in split_into_searchable_units(text):
            units.append({
                "text": sentence,
                "page": None
            })

    return units


# ============================================================
# EXACT / KEYWORD SEARCH
# ============================================================

def exact_keyword_search(question, document_text):
    """
    Search for strong keyword evidence.

    Requires all meaningful terms for questions containing
    one or two meaningful terms. For longer queries, requires
    at least 60% of meaningful terms, rounded up.

    Returns records containing text and page metadata.
    """

    question = normalize_text(question)

    if not question:
        return []

    query_words = get_meaningful_words(question)

    if not query_words:
        return []

    document_units = extract_document_units(document_text)

    if not document_units:
        return []

    scored = []

    for unit in document_units:

        text = unit["text"]
        text_tokens = tokenize(text)

        matched_words = query_words.intersection(
            text_tokens
        )

        if not matched_words:
            continue

        coverage = len(matched_words) / len(query_words)

        # Short queries need stronger evidence.
        if len(query_words) <= 2:
            minimum_matches = len(query_words)
        else:
            minimum_matches = max(
                2,
                (len(query_words) * 3 + 4) // 5
            )

        if len(matched_words) < minimum_matches:
            continue

        # Prefer complete meaningful-term matches.
        exact_coverage_bonus = (
            0.15
            if len(matched_words) == len(query_words)
            else 0.0
        )

        score = coverage + exact_coverage_bonus

        scored.append({
            "text": text,
            "page": unit.get("page"),
            "keyword_score": float(score),
            "matched_terms": sorted(matched_words)
        })

    scored.sort(
        key=lambda item: item["keyword_score"],
        reverse=True
    )

    return limit_results(
        scored,
        MAX_EXACT_RESULTS
    )


# ============================================================
# LIMIT AND DEDUPLICATE RESULTS
# ============================================================

def limit_results(results, maximum):
    """Remove duplicate evidence while preserving its page."""

    unique_results = []
    seen = set()

    for result in results:

        if isinstance(result, dict):
            text = normalize_text(
                result.get("text", "")
            )
            page = result.get("page")
        else:
            text = normalize_text(result)
            page = None

        if not text:
            continue

        signature = (
            text.lower(),
            page
        )

        if signature in seen:
            continue

        seen.add(signature)

        if isinstance(result, dict):
            unique_results.append(result)
        else:
            unique_results.append({
                "text": text,
                "page": page
            })

        if len(unique_results) >= maximum:
            break

    return unique_results


# ============================================================
# PAGE REFERENCES
# ============================================================

def get_referenced_pages(results):
    """Return unique page numbers in ascending order."""

    pages = set()

    for item in results:

        if not isinstance(item, dict):
            continue

        page = item.get("page")

        if page is None:
            continue

        pages.add(page)

    return sorted(
        pages,
        key=lambda value: (
            0,
            float(value)
        ) if str(value).replace(".", "", 1).isdigit()
        else (1, str(value))
    )


def format_page_sources(results):
    """Create readable page-reference source labels."""

    pages = get_referenced_pages(results)

    if not pages:
        return []

    return [
        "Referenced pages: "
        + ", ".join(str(page) for page in pages)
    ]


# ============================================================
# EXACT SEARCH RESPONSE
# ============================================================

def build_exact_search_answer(question, results):
    """
    Format keyword evidence without inventing conclusions.

    Exact search returns document excerpts, not generated facts.
    """

    if not results:
        return (
            "No sufficiently strong keyword evidence was found "
            "for this question."
        )

    formatted_results = []

    for index, item in enumerate(results, start=1):

        if isinstance(item, dict):
            text = normalize_text(
                item.get("text", "")
            )
            page = item.get("page")
        else:
            text = normalize_text(item)
            page = None

        if not text:
            continue

        if page is not None:
            formatted_results.append(
                f"{index}. [Page {page}] {text}"
            )
        else:
            formatted_results.append(
                f"{index}. {text}"
            )

    if not formatted_results:
        return (
            "No readable evidence was found in the document."
        )

    return (
        f"### Relevant document evidence\n\n"
        f"**Question:** {question}\n\n"
        + "\n\n".join(formatted_results)
        + "\n\n"
        "These excerpts were selected using keyword matching. "
        "Review the cited document pages for their full context."
    )


# ============================================================
# RETRIEVAL RESULT NORMALIZATION
# ============================================================

def normalize_retrieval_results(retrieved):
    """
    Support the current dictionary-based retriever and
    older list-based results.
    """

    if isinstance(retrieved, dict):

        results = retrieved.get("results", [])
        context = retrieved.get("context", "")

        retrieval_method = retrieved.get(
            "retrieval_method",
            "Hybrid Semantic + Lexical RAG"
        )

    elif isinstance(retrieved, list):

        results = retrieved
        context = ""
        retrieval_method = "RAG Search"

    else:

        results = []
        context = ""
        retrieval_method = "RAG Search"

    valid_results = []

    for item in results:

        if not isinstance(item, dict):
            continue

        text = normalize_text(
            item.get("text", "")
        )

        if not text:
            continue

        valid_results.append({
            **item,
            "text": text
        })

    context = normalize_text(context)

    return (
        valid_results,
        context,
        retrieval_method
    )


# ============================================================
# SEMANTIC ANSWER FORMATTER
# ============================================================

def generate_semantic_answer(question, context):
    """
    Format retrieved evidence into a grounded response.

    Note: this function does not call an LLM. It formats
    the evidence returned by the retrieval pipeline.
    """

    context = normalize_text(context)

    if not context:
        return (
            "I could not find sufficiently relevant evidence "
            "in the uploaded document."
        )

    return (
        f"### Relevant information\n\n"
        f"**Question:** {question}\n\n"
        f"{context}\n\n"
        "The information above was retrieved from the uploaded "
        "document. Check the referenced pages to verify the "
        "full context."
    )


# ============================================================
# RESOURCE INTELLIGENCE AGENT
# ============================================================

def resource_agent(question, resource_id, document_data):
    """
    Main agent entry point.

    Processing order:
        1. Validate the question.
        2. Search for strong keyword evidence.
        3. Use hybrid RAG when keyword evidence is insufficient.
        4. Return page-aware evidence and source metadata.
        5. Abstain when relevant evidence cannot be found.
    """

    question = normalize_text(question)

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": []
        }

    if not isinstance(document_data, dict):
        document_data = {
            "text": str(document_data or "")
        }

    # --------------------------------------------------------
    # STEP 1: STRONG KEYWORD SEARCH
    # --------------------------------------------------------

    try:
        exact_results = exact_keyword_search(
            question,
            document_data
        )

    except Exception as error:
        print(f"Keyword search error: {error}")
        exact_results = []

    if exact_results:

        answer = build_exact_search_answer(
            question,
            exact_results
        )

        sources = [
            "Uploaded Document",
            "Exact Keyword Search",
            "Resource Intelligence Agent"
        ]

        sources.extend(
            format_page_sources(exact_results)
        )

        return {
            "answer": answer,
            "sources": sources
        }

    # --------------------------------------------------------
    # STEP 2: HYBRID RAG SEARCH
    # --------------------------------------------------------

    try:
        retrieved = search_document(
            question,
            resource_id,
            top_k=MAX_RAG_RESULTS
        )

    except Exception as error:

        print(
            f"RAG retrieval error for resource "
            f"{resource_id}: {error}"
        )

        return {
            "answer": (
                "I could not complete the document search because "
                "the retrieval system encountered an error. "
                "Please check the application logs and confirm "
                "that the document has been indexed."
            ),
            "sources": []
        }

    (
        valid_results,
        context,
        retrieval_method
    ) = normalize_retrieval_results(retrieved)

    # --------------------------------------------------------
    # STEP 3: ABSTAIN IF THERE IS NO SUPPORTING EVIDENCE
    # --------------------------------------------------------

    if not valid_results and not context:

        return {
            "answer": (
                "I could not find sufficiently relevant evidence "
                "for this question in the uploaded document. "
                "Try different keywords or ask a more specific "
                "question. I will not guess an answer when the "
                "document does not provide supporting evidence."
            ),
            "sources": []
        }

    # --------------------------------------------------------
    # STEP 4: BUILD PAGE-AWARE CONTEXT IF NEEDED
    # --------------------------------------------------------

    if not context:

        context_parts = []

        for item in valid_results:

            text = item["text"]
            page = item.get("page")

            if page is not None:
                context_parts.append(
                    f"[Page {page}] {text}"
                )
            else:
                context_parts.append(text)

        context = "\n\n".join(context_parts)

    if not context.strip():

        return {
            "answer": (
                "I could not prepare readable evidence from "
                "the retrieved document passages."
            ),
            "sources": []
        }

    # --------------------------------------------------------
    # STEP 5: FORMAT THE GROUNDED RESPONSE
    # --------------------------------------------------------

    answer = generate_semantic_answer(
        question,
        context
    )

    # --------------------------------------------------------
    # STEP 6: RETURN SOURCE METADATA
    # --------------------------------------------------------

    sources = [
        "Uploaded Document",
        retrieval_method,
        "Resource Intelligence Agent"
    ]

    sources.extend(
        format_page_sources(valid_results)
    )

    return {
        "answer": answer,
        "sources": sources
    }
