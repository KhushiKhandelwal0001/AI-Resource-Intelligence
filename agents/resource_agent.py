

# ============================================================
# RESOURCE INTELLIGENCE AGENT
# SPECIFIC SEARCH + SEMANTIC RAG
# ============================================================

import re

from rag.retriever import search_document


def resource_agent(question, resource_id, document_data):

    question = (question or "").strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": []
        }

    document_text = (
        document_data.get("text", "")
        if isinstance(document_data, dict)
        else ""
    )

    # --------------------------------------------------------
    # FIRST: EXACT / KEYWORD SEARCH
    # --------------------------------------------------------

    exact_results = exact_keyword_search(
        question,
        document_text
    )

    if exact_results:
        answer = build_exact_search_answer(
            question,
            exact_results
        )

        return {
            "answer": answer,
            "sources": [
                "Uploaded Document",
                "Exact Keyword Search",
                "Resource Intelligence Agent"
            ]
        }

    # --------------------------------------------------------
    # SECOND: SEMANTIC RAG SEARCH
    # Used when an exact keyword match is not available.
    # --------------------------------------------------------

    retrieved = search_document(
        question,
        resource_id,
        top_k=5
    )

    if not retrieved:
        return {
            "answer": (
                "I could not find information matching "
                "your search in the uploaded document."
            ),
            "sources": []
        }

    context_parts = []

    for item in retrieved:

        text = item.get("text", "").strip()

        if text:
            context_parts.append(text)

    context = "\n\n".join(context_parts)

    answer = generate_semantic_answer(
        question,
        context
    )

    return {
        "answer": answer,
        "sources": [
            "Uploaded Document",
            "RAG Semantic Search",
            "Resource Intelligence Agent"
        ]
    }


# ============================================================
# EXACT KEYWORD SEARCH
# ============================================================

def exact_keyword_search(question, document_text):

    if not document_text:
        return []

    query = question.strip()

    # Remove common conversational words.
    cleaned_query = re.sub(
        r"\b(find|show|give|tell|me|about|search|information|details|what|is|are|the|for)\b",
        " ",
        query,
        flags=re.IGNORECASE
    )

    cleaned_query = re.sub(
        r"\s+",
        " ",
        cleaned_query
    ).strip()

    if not cleaned_query:
        return []

    # --------------------------------------------------------
    # Try the complete phrase first.
    # --------------------------------------------------------

    phrase_pattern = re.compile(
        re.escape(cleaned_query),
        flags=re.IGNORECASE
    )

    lines = [
        line.strip()
        for line in document_text.splitlines()
        if line.strip()
    ]

    phrase_matches = []

    for line in lines:

        if phrase_pattern.search(line):

            phrase_matches.append(line)

    if phrase_matches:
        return limit_results(
            phrase_matches,
            8
        )

    # --------------------------------------------------------
    # Single-word / keyword search.
    # --------------------------------------------------------

    words = [
        word.lower()
        for word in re.findall(
            r"[A-Za-z0-9][A-Za-z0-9&./+-]*",
            cleaned_query
        )
        if len(word) >= 2
    ]

    if not words:
        return []

    # For a one-word search, that word MUST occur.
    if len(words) == 1:

        keyword = words[0]

        pattern = re.compile(
            r"\b" + re.escape(keyword) + r"\b",
            flags=re.IGNORECASE
        )

        matches = []

        for line in lines:

            if pattern.search(line):
                matches.append(line)

        return limit_results(
            matches,
            10
        )

    # --------------------------------------------------------
    # Multi-word keyword search.
    # Return lines containing at least one meaningful term.
    # Score lines by number of matching terms.
    # --------------------------------------------------------

    scored = []

    for line in lines:

        score = 0

        lower_line = line.lower()

        for word in words:

            if re.search(
                r"\b" + re.escape(word) + r"\b",
                lower_line
            ):
                score += 1

        if score > 0:

            scored.append(
                (
                    score,
                    line
                )
            )

    scored.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        line
        for score, line in scored[:10]
    ]


# ============================================================
# LIMIT RESULTS
# ============================================================

def limit_results(results, maximum):

    unique_results = []

    seen = set()

    for result in results:

        normalized = result.strip().lower()

        if normalized in seen:
            continue

        seen.add(normalized)

        unique_results.append(result.strip())

        if len(unique_results) >= maximum:
            break

    return unique_results


# ============================================================
# EXACT SEARCH RESPONSE
# ============================================================

def build_exact_search_answer(
    question,
    results
):

    if not results:

        return (
            "No exact information matching "
            f"'{question}' was found in the document."
        )

    formatted_results = []

    for index, result in enumerate(
        results,
        start=1
    ):

        formatted_results.append(
            f"{index}. {result}"
        )

    return (
        f"### Search results for: {question}\n\n"
        + "\n\n".join(formatted_results)
        + "\n\n"
        "These results were selected using exact "
        "keyword matching from the uploaded document."
    )


# ============================================================
# SEMANTIC ANSWER
# ============================================================

def generate_semantic_answer(
    question,
    context
):

    return (
        f"### Relevant information for: {question}\n\n"
        f"{context}\n\n"
        "The information above was retrieved using "
        "semantic search from the uploaded document."
    )
