
# ============================================================
# AI RESOURCE INTELLIGENCE
# ADVANCED HYBRID RAG RETRIEVER
# ============================================================

import os
import re
import pickle

import numpy as np
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

EMBEDDING_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "embeddings"
)

MODEL_NAME = "all-MiniLM-L6-v2"

DEFAULT_TOP_K = 6
MAX_CONTEXT_CHARS = 7000
MIN_RELEVANCE_SCORE = 0.20

# Load the model only once per running process.
_model = None


# ============================================================
# MODEL
# ============================================================

def get_model():
    """Load and cache the sentence embedding model."""

    global _model

    if _model is None:
        print()
        print("=" * 60)
        print("Loading RAG embedding model...")
        print(f"Model: {MODEL_NAME}")
        print("=" * 60)

        _model = SentenceTransformer(MODEL_NAME)

        print("RAG embedding model loaded successfully.")
        print("=" * 60)
        print()

    return _model


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """Normalize whitespace and convert input to a string."""

    if text is None:
        return ""

    text = str(text)
    text = text.replace("\r", " ")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text):
    """Tokenize text for lexical retrieval."""

    text = normalize_text(text).lower()

    tokens = re.findall(
        r"[a-zA-Z0-9+#.-]+",
        text
    )

    return {
        token
        for token in tokens
        if len(token) > 1
    }


def meaningful_tokens(text):
    """Remove common question words for relevance scoring."""

    stop_words = {
        "a", "an", "and", "or", "the", "to", "of",
        "in", "on", "at", "by", "from", "with",
        "for", "about", "what", "which", "who",
        "when", "where", "why", "how", "is", "are",
        "was", "were", "be", "been", "being", "do",
        "does", "did", "can", "could", "would",
        "should", "will", "it", "this", "that",
        "these", "those", "my", "your", "their",
        "me", "please", "tell", "show", "give",
        "find", "explain", "describe", "information",
        "details", "document", "uploaded"
    }

    return {
        token
        for token in tokenize(text)
        if token not in stop_words
    }


# ============================================================
# SENTENCE SPLITTING
# ============================================================

def split_sentences(text):
    """Split normalized text into sentences."""

    text = normalize_text(text)

    if not text:
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


# ============================================================
# SMART CHUNKING
# ============================================================

def create_chunks(
    text,
    chunk_size=850,
    overlap=150,
    page_number=None
):
    """
    Create overlapping text chunks while preserving
    sentence boundaries where possible.

    Each chunk stores its original page number.
    """

    text = normalize_text(text)

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0:
        overlap = 0

    # Overlap should not exceed the chunk size.
    overlap = min(overlap, chunk_size - 1)

    sentences = split_sentences(text)

    if not sentences:
        return []

    chunks = []
    current = []
    current_length = 0

    for sentence in sentences:

        sentence_length = len(sentence)

        # Handle exceptionally long sentences separately.
        if sentence_length > chunk_size:

            if current:
                chunk_text = " ".join(current).strip()

                if chunk_text:
                    chunks.append({
                        "text": chunk_text,
                        "page": page_number
                    })

                current = []
                current_length = 0

            start = 0
            step = max(1, chunk_size - overlap)

            while start < len(sentence):
                piece = sentence[start:start + chunk_size].strip()

                if piece:
                    chunks.append({
                        "text": piece,
                        "page": page_number
                    })

                start += step

            continue

        added_length = sentence_length

        if current:
            added_length += 1  # Space between sentences.

        if (
            current
            and current_length + added_length > chunk_size
        ):
            chunk_text = " ".join(current).strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page_number
                })

            # Preserve recent sentences for overlap.
            overlap_sentences = []
            overlap_length = 0

            for previous in reversed(current):

                required_length = len(previous)

                if overlap_sentences:
                    required_length += 1

                if overlap_length + required_length > overlap:
                    break

                overlap_sentences.insert(0, previous)
                overlap_length += required_length

            # Avoid carrying overlap into a chunk that
            # would already exceed the configured size.
            while (
                overlap_sentences
                and sum(map(len, overlap_sentences))
                + len(overlap_sentences) - 1
                + len(sentence)
                + 1
                > chunk_size
            ):
                overlap_sentences.pop(0)

            current = overlap_sentences + [sentence]

            current_length = (
                sum(len(item) for item in current)
                + max(0, len(current) - 1)
            )

        else:
            current.append(sentence)
            current_length += added_length

    if current:
        chunk_text = " ".join(current).strip()

        if chunk_text:
            chunks.append({
                "text": chunk_text,
                "page": page_number
            })

    return chunks


# ============================================================
# DOCUMENT CHUNK CREATION
# ============================================================

def create_document_chunks(document_data):
    """
    Convert document content into page-aware chunks.

    Supported input formats:

    1. {"text": "..."}
    2. {"pages": [{"page": 1, "text": "..."}]}
    3. {"pages": [{"page_number": 1, "text": "..."}]}

    Page references are preserved for citations.
    """

    if isinstance(document_data, str):
        document_data = {
            "text": document_data
        }

    if not isinstance(document_data, dict):
        return []

    pages = document_data.get("pages", [])
    chunks = []

    if isinstance(pages, list) and pages:

        for page in pages:

            if not isinstance(page, dict):
                continue

            page_number = page.get("page_number")

            if page_number is None:
                page_number = page.get("page")

            page_text = page.get("text", "")

            page_chunks = create_chunks(
                page_text,
                page_number=page_number
            )

            chunks.extend(page_chunks)

    else:
        # Fallback for documents without page-level content.
        text = document_data.get("text", "")

        chunks = create_chunks(text)

    return chunks


# ============================================================
# DUPLICATE REMOVAL
# ============================================================

def deduplicate_chunks(chunks):
    """
    Remove duplicate text chunks.

    Keep page number in the signature so identical text
    appearing on different pages retains its page provenance.
    """

    seen = set()
    unique_chunks = []

    for chunk in chunks:

        if not isinstance(chunk, dict):
            continue

        text = normalize_text(
            chunk.get("text", "")
        )

        if not text:
            continue

        signature_text = re.sub(
            r"[^a-z0-9]+",
            " ",
            text.lower()
        ).strip()

        page = chunk.get("page")

        signature = (signature_text, page)

        if signature in seen:
            continue

        seen.add(signature)

        unique_chunks.append({
            "text": text,
            "page": page
        })

    return unique_chunks


# ============================================================
# BUILD EMBEDDINGS
# ============================================================

def build_embeddings(document_data, resource_id):
    """
    Build and save normalized semantic embeddings
    for one uploaded resource.
    """

    if not resource_id:
        raise ValueError("resource_id is required.")

    if isinstance(document_data, str):
        document_data = {
            "text": document_data,
            "pages": [{
                "page": 1,
                "text": document_data
            }]
        }

    if not isinstance(document_data, dict):
        return None

    chunks = create_document_chunks(document_data)
    chunks = deduplicate_chunks(chunks)

    if not chunks:
        print(
            f"No readable text found for resource: {resource_id}"
        )
        return None

    os.makedirs(
        EMBEDDING_FOLDER,
        exist_ok=True
    )

    model = get_model()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    if (
        embeddings.ndim != 2
        or embeddings.shape[0] != len(chunks)
    ):
        raise ValueError(
            "Embedding count does not match the document chunks."
        )

    rag_data = {
        "resource_id": str(resource_id),
        "model": MODEL_NAME,
        "chunks": chunks,
        "embeddings": embeddings
    }

    file_path = os.path.join(
        EMBEDDING_FOLDER,
        f"{resource_id}.pkl"
    )

    with open(file_path, "wb") as file:
        pickle.dump(
            rag_data,
            file,
            protocol=pickle.HIGHEST_PROTOCOL
        )

    print(
        f"RAG embeddings saved for {resource_id}: "
        f"{len(chunks)} chunks"
    )

    return rag_data


# ============================================================
# LOAD EMBEDDINGS
# ============================================================

def load_embeddings(resource_id):
    """Load and validate a resource's saved embeddings."""

    if not resource_id:
        return None

    file_path = os.path.join(
        EMBEDDING_FOLDER,
        f"{resource_id}.pkl"
    )

    if not os.path.isfile(file_path):
        return None

    try:
        with open(file_path, "rb") as file:
            rag_data = pickle.load(file)

    except (OSError, EOFError, pickle.UnpicklingError) as error:
        print(
            f"Unable to load embeddings for {resource_id}: {error}"
        )
        return None

    if not isinstance(rag_data, dict):
        return None

    chunks = rag_data.get("chunks")
    embeddings = rag_data.get("embeddings")

    if not isinstance(chunks, list) or embeddings is None:
        return None

    embeddings = np.asarray(embeddings)

    if embeddings.ndim != 2:
        return None

    if len(chunks) != embeddings.shape[0]:
        return None

    rag_data["embeddings"] = embeddings

    return rag_data


# ============================================================
# SEMANTIC SEARCH
# ============================================================

def semantic_search(
    question,
    rag_data,
    top_k=10
):
    """Retrieve chunks ranked by semantic similarity."""

    question = normalize_text(question)

    if not question or not isinstance(rag_data, dict):
        return []

    chunks = rag_data.get("chunks", [])
    embeddings = rag_data.get("embeddings")

    if not chunks or embeddings is None:
        return []

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    if (
        embeddings.ndim != 2
        or embeddings.shape[0] != len(chunks)
    ):
        return []

    model = get_model()

    question_embedding = model.encode(
        [question],
        normalize_embeddings=True,
        show_progress_bar=False
    )[0]

    scores = np.dot(
        embeddings,
        question_embedding
    )

    top_k = max(1, int(top_k))

    indexes = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in indexes:

        chunk = chunks[int(index)]

        if not isinstance(chunk, dict):
            continue

        results.append({
            "text": chunk.get("text", ""),
            "page": chunk.get("page"),
            "semantic_score": float(scores[index])
        })

    return results


# ============================================================
# LEXICAL SEARCH
# ============================================================

def lexical_search(
    question,
    rag_data,
    top_k=10
):
    """Retrieve chunks using meaningful keyword overlap."""

    question_tokens = meaningful_tokens(question)

    if not question_tokens or not isinstance(rag_data, dict):
        return []

    scored = []

    for chunk in rag_data.get("chunks", []):

        if not isinstance(chunk, dict):
            continue

        text = chunk.get("text", "")
        chunk_tokens = tokenize(text)

        if not chunk_tokens:
            continue

        overlap = question_tokens.intersection(chunk_tokens)

        if not overlap:
            continue

        # Score the proportion of meaningful question terms
        # found in this chunk.
        score = len(overlap) / len(question_tokens)

        scored.append({
            "text": text,
            "page": chunk.get("page"),
            "lexical_score": float(score),
            "matched_terms": sorted(overlap)
        })

    scored.sort(
        key=lambda item: item["lexical_score"],
        reverse=True
    )

    return scored[:max(1, int(top_k))]


# ============================================================
# HYBRID RETRIEVAL
# ============================================================

def hybrid_search(
    question,
    resource_id,
    top_k=DEFAULT_TOP_K
):
    """
    Combine semantic similarity, lexical relevance,
    and phrase/term coverage into a hybrid ranking.

    Scores are ranking signals, not calibrated probabilities.
    """

    question = normalize_text(question)

    if not question:
        return []

    rag_data = load_embeddings(resource_id)

    if not rag_data:
        return []

    semantic_results = semantic_search(
        question,
        rag_data,
        top_k=10
    )

    lexical_results = lexical_search(
        question,
        rag_data,
        top_k=10
    )

    merged = {}

    # --------------------------------------------------------
    # Merge semantic candidates
    # --------------------------------------------------------

    for result in semantic_results:

        text = normalize_text(result.get("text", ""))

        if not text:
            continue

        key = text.lower()

        merged[key] = {
            "text": text,
            "page": result.get("page"),
            "semantic_score": result.get(
                "semantic_score", 0.0
            ),
            "lexical_score": 0.0,
            "matched_terms": []
        }

    # --------------------------------------------------------
    # Merge lexical candidates
    # --------------------------------------------------------

    for result in lexical_results:

        text = normalize_text(result.get("text", ""))

        if not text:
            continue

        key = text.lower()

        if key not in merged:
            merged[key] = {
                "text": text,
                "page": result.get("page"),
                "semantic_score": 0.0,
                "lexical_score": result.get(
                    "lexical_score", 0.0
                ),
                "matched_terms": result.get(
                    "matched_terms", []
                )
            }

        else:
            merged[key]["lexical_score"] = result.get(
                "lexical_score", 0.0
            )

            merged[key]["matched_terms"] = result.get(
                "matched_terms", []
            )

    # --------------------------------------------------------
    # Calculate query coverage and hybrid scores
    # --------------------------------------------------------

    query_tokens = meaningful_tokens(question)
    question_normalized = normalize_text(question).lower()

    results = []

    for item in merged.values():

        text = normalize_text(item["text"])
        text_normalized = text.lower()

        semantic_score = float(
            item.get("semantic_score", 0.0)
        )

        lexical_score = float(
            item.get("lexical_score", 0.0)
        )

        chunk_tokens = tokenize(text)

        matched_query_tokens = query_tokens.intersection(
            chunk_tokens
        )

        query_coverage = (
            len(matched_query_tokens) / len(query_tokens)
            if query_tokens
            else 0.0
        )

        # Exact full-question match is uncommon, but useful
        # when the document contains the same wording.
        exact_phrase_score = (
            1.0
            if len(question_normalized) > 5
            and question_normalized in text_normalized
            else 0.0
        )

        # Full meaningful-term coverage is also a strong signal.
        if query_tokens and query_coverage == 1.0:
            exact_phrase_score = max(
                exact_phrase_score,
                1.0
            )

        final_score = (
            semantic_score * 0.55
            + lexical_score * 0.30
            + exact_phrase_score * 0.15
        )

        results.append({
            "text": text,
            "page": item.get("page"),
            "semantic_score": semantic_score,
            "lexical_score": lexical_score,
            "query_coverage": float(query_coverage),
            "matched_terms": sorted(matched_query_tokens),
            "score": float(final_score)
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # --------------------------------------------------------
    # Relevance filtering
    # --------------------------------------------------------

    filtered = [
        item
        for item in results
        if item["score"] >= MIN_RELEVANCE_SCORE
    ]

    return filtered[:max(1, int(top_k))]


# ============================================================
# CONTEXT COMPRESSION
# ============================================================

def compress_context(
    question,
    results,
    max_chars=MAX_CONTEXT_CHARS
):
    """
    Extract relevant sentences from retrieved chunks.

    Adds page labels so the answer layer can identify
    supporting document locations.
    """

    if not results or max_chars <= 0:
        return ""

    question_tokens = meaningful_tokens(question)

    selected_sentences = []
    seen_sentences = set()
    current_length = 0

    for result in results:

        if not isinstance(result, dict):
            continue

        text = result.get("text", "")

        sentences = split_sentences(text)

        ranked_sentences = []

        for sentence in sentences:

            sentence_tokens = tokenize(sentence)

            overlap = question_tokens.intersection(
                sentence_tokens
            )

            # Rank sentences with more query-term matches first.
            score = len(overlap)

            ranked_sentences.append(
                (score, sentence)
            )

        ranked_sentences.sort(
            key=lambda item: item[0],
            reverse=True
        )

        for score, sentence in ranked_sentences:

            normalized = normalize_text(sentence).lower()

            if not normalized:
                continue

            if normalized in seen_sentences:
                continue

            # If query tokens exist, avoid adding unrelated
            # sentences from a retrieved chunk.
            if question_tokens and score == 0:
                continue

            page = result.get("page")

            if page is not None:
                formatted_sentence = (
                    f"[Page {page}] {sentence}"
                )
            else:
                formatted_sentence = sentence

            # Do not exceed the context budget.
            remaining = max_chars - current_length

            if len(formatted_sentence) > remaining:
                if remaining <= 0:
                    return "\n".join(selected_sentences)

                # Avoid emitting a misleading partial sentence.
                break

            selected_sentences.append(formatted_sentence)
            seen_sentences.add(normalized)

            current_length += len(formatted_sentence) + 1

            if current_length >= max_chars:
                return "\n".join(selected_sentences)

    return "\n".join(selected_sentences)


# ============================================================
# PUBLIC SEARCH API
# ============================================================

def search_document(
    question,
    resource_id,
    top_k=DEFAULT_TOP_K
):
    """
    Public entry point used by the Resource Intelligence Agent.

    Returns ranked evidence, page-aware context, and
    retrieval metadata.
    """

    question = normalize_text(question)

    if not question:
        return {
            "results": [],
            "context": "",
            "retrieval_method": "Hybrid Semantic + Lexical RAG",
            "model": MODEL_NAME
        }

    results = hybrid_search(
        question,
        resource_id,
        top_k=top_k
    )

    compressed_context = compress_context(
        question,
        results
    )

    return {
        "results": results,
        "context": compressed_context,
        "retrieval_method": "Hybrid Semantic + Lexical RAG",
        "model": MODEL_NAME
    }
