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

_model = None


# ============================================================
# MODEL
# ============================================================

def get_model():
    """
    Load the embedding model only once.
    """

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
    if not text:
        return ""

    text = str(text)

    text = text.replace("\r", " ")
    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text):
    """
    Lightweight tokenizer used for lexical retrieval.
    """

    text = normalize_text(text).lower()

    return set(
        token
        for token in re.findall(
            r"[a-zA-Z0-9+#.-]+",
            text
        )
        if len(token) > 1
    )


# ============================================================
# SENTENCE SPLITTING
# ============================================================

def split_sentences(text):
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
    Creates overlapping chunks while trying to preserve
    sentence boundaries.
    """

    text = normalize_text(text)

    if not text:
        return []

    sentences = split_sentences(text)

    if not sentences:
        return []

    chunks = []

    current = []
    current_length = 0

    for sentence in sentences:

        sentence_length = len(sentence)

        if (
            current
            and
            current_length + sentence_length > chunk_size
        ):

            chunk_text = " ".join(current).strip()

            if chunk_text:

                chunks.append({
                    "text": chunk_text,
                    "page": page_number
                })


            # ------------------------------------------------
            # Preserve overlap
            # ------------------------------------------------

            overlap_text = []
            overlap_length = 0

            for previous in reversed(current):

                if overlap_length + len(previous) > overlap:
                    break

                overlap_text.insert(
                    0,
                    previous
                )

                overlap_length += len(previous)


            current = overlap_text + [sentence]

            current_length = sum(
                len(item)
                for item in current
            )

        else:

            current.append(sentence)

            current_length += sentence_length


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
    Converts document pages into page-aware RAG chunks.
    """

    pages = document_data.get(
        "pages",
        []
    )

    chunks = []


    if pages:

        for page in pages:

            page_number = page.get(
                "page",
                None
            )

            page_text = page.get(
                "text",
                ""
            )

            page_chunks = create_chunks(
                page_text,
                page_number=page_number
            )

            chunks.extend(page_chunks)

    else:

        text = document_data.get(
            "text",
            ""
        )

        chunks = create_chunks(
            text
        )


    return chunks


# ============================================================
# DUPLICATE REMOVAL
# ============================================================

def deduplicate_chunks(chunks):

    seen = set()
    unique_chunks = []

    for chunk in chunks:

        text = normalize_text(
            chunk.get("text", "")
        )

        if not text:
            continue

        signature = re.sub(
            r"[^a-z0-9]+",
            " ",
            text.lower()
        ).strip()


        if signature in seen:
            continue


        seen.add(signature)

        unique_chunks.append(chunk)


    return unique_chunks


# ============================================================
# BUILD EMBEDDINGS
# ============================================================

def build_embeddings(
    document_data,
    resource_id
):
    """
    Builds and stores page-aware semantic embeddings.
    """

    if isinstance(document_data, str):

        document_data = {
            "text": document_data,
            "pages": [
                {
                    "page": 1,
                    "text": document_data
                }
            ]
        }


    chunks = create_document_chunks(
        document_data
    )

    chunks = deduplicate_chunks(
        chunks
    )


    if not chunks:

        return None


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


    file_path = os.path.join(
        EMBEDDING_FOLDER,
        f"{resource_id}.pkl"
    )


    rag_data = {

        "resource_id":
            resource_id,

        "model":
            MODEL_NAME,

        "chunks":
            chunks,

        "embeddings":
            embeddings

    }


    with open(
        file_path,
        "wb"
    ) as file:

        pickle.dump(
            rag_data,
            file
        )


    return rag_data


# ============================================================
# LOAD EMBEDDINGS
# ============================================================

def load_embeddings(resource_id):

    file_path = os.path.join(
        EMBEDDING_FOLDER,
        f"{resource_id}.pkl"
    )


    if not os.path.exists(file_path):
        return None


    with open(
        file_path,
        "rb"
    ) as file:

        return pickle.load(file)


# ============================================================
# SEMANTIC SEARCH
# ============================================================

def semantic_search(
    question,
    rag_data,
    top_k=10
):

    model = get_model()


    question_embedding = model.encode(
        [question],
        normalize_embeddings=True,
        show_progress_bar=False
    )[0]


    embeddings = rag_data["embeddings"]


    scores = np.dot(
        embeddings,
        question_embedding
    )


    indexes = np.argsort(
        scores
    )[::-1][:top_k]


    results = []


    for index in indexes:

        chunk = rag_data["chunks"][index]


        results.append({

            "text":
                chunk.get("text", ""),

            "page":
                chunk.get("page"),

            "semantic_score":
                float(scores[index])

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

    question_tokens = tokenize(question)


    if not question_tokens:
        return []


    scored = []


    for chunk in rag_data["chunks"]:

        text = chunk.get("text","" )


        chunk_tokens = tokenize(text)


        if not chunk_tokens:
            continue


        overlap = question_tokens.intersection(chunk_tokens)


        score = (
            len(overlap)
            /
            max(
                len(question_tokens),
                1
            )
        )


        if score <= 0:
            continue


        scored.append({

            "text":
                text,

            "page":
                chunk.get("page"),

            "lexical_score":
                float(score),

            "matched_terms":
                sorted(overlap)

        })


    scored.sort(
        key=lambda item:
            item["lexical_score"],
        reverse=True
    )


    return scored[:top_k]


# ============================================================
# HYBRID RETRIEVAL
# ============================================================

def hybrid_search(
    question,
    resource_id,
    top_k=DEFAULT_TOP_K
):
    """
    Combines:

    1. Semantic similarity
    2. Keyword overlap
    3. Exact phrase relevance

    into one ranked retrieval pipeline.
    """

    rag_data = load_embeddings(resource_id)


    if not rag_data:
        return []


    semantic_results = semantic_search(question,rag_data,top_k=10)


    lexical_results = lexical_search(question,rag_data,top_k=10)


    merged = {}


    # --------------------------------------------------------
    # Semantic candidates
    # --------------------------------------------------------

    for result in semantic_results:

        key = normalize_text( result["text"])

        merged[key] = {

            "text":
                result["text"],

            "page":
                result.get("page"),

            "semantic_score":
                result.get(
                    "semantic_score",
                    0
                ),

            "lexical_score":
                0,

            "matched_terms":
                []

        }


    # --------------------------------------------------------
    # Lexical candidates
    # --------------------------------------------------------

    for result in lexical_results:

        key = normalize_text(result["text"])


        if key not in merged:

            merged[key] = {

                "text":
                    result["text"],

                "page":
                    result.get("page"),

                "semantic_score":
                    0,

                "lexical_score":
                    result.get(
                        "lexical_score",
                        0
                    ),

                "matched_terms":
                    result.get(
                        "matched_terms",
                        []
                    )

            }

        else:

            merged[key][
                "lexical_score"
            ] = result.get(
                "lexical_score",
                0
            )

            merged[key][
                "matched_terms"
            ] = result.get(
                "matched_terms",
                []
            )


    question_normalized = normalize_text(question).lower()


    # --------------------------------------------------------
    # Final hybrid ranking
    # --------------------------------------------------------

    results = []


    for item in merged.values():

        text = normalize_text(item["text"]).lower()


        exact_phrase_score = 0


        if len(question_normalized) > 5:

            if question_normalized in text:
                exact_phrase_score = 1


        final_score = (

            item["semantic_score"]
            * 0.60

            +

            item["lexical_score"]
            * 0.25

            +

            exact_phrase_score
            * 0.15

        )


        item["score"] = float(final_score)


        results.append(item)


    results.sort(
        key=lambda item:
            item["score"],
        reverse=True
    )


    # --------------------------------------------------------
    # Relevance filtering
    # --------------------------------------------------------

    filtered = []


    for item in results:

        if item["score"] >= 0.20:

            filtered.append(item)


    return filtered[:top_k]


# ============================================================
# CONTEXT COMPRESSION
# ============================================================

def compress_context(
    question,
    results,
    max_chars=MAX_CONTEXT_CHARS
):
    """
    Extracts only the most relevant sentences
    instead of sending entire chunks to the answer engine.
    """

    question_tokens = tokenize(question)


    selected_sentences = []

    seen_sentences = set()

    for result in results:

        sentences = split_sentences(result.get("text","" ) )


        ranked_sentences = []


        for sentence in sentences:

            sentence_tokens = tokenize(sentence)


            overlap = question_tokens.intersection(sentence_tokens)


            score = len(overlap)


            ranked_sentences.append(
                (
                    score,
                    sentence
                )
            )


        ranked_sentences.sort(
            key=lambda item:
                item[0],
            reverse=True
        )


        for score, sentence in ranked_sentences:

            normalized = normalize_text(sentence).lower()


            if not normalized:
                continue


            if normalized in seen_sentences:
                continue


            if score == 0 and selected_sentences:
                continue


            seen_sentences.add(
                normalized
            )


            page = result.get("page")


            if page:

                source = f"[Page {page}] "

            else:

                source = ""


            selected_sentences.append(
                source + sentence
            )


            current_length = sum(len(item)for item in selected_sentences)


            if current_length >= max_chars:

                break


        if (
            sum(
                len(item)
                for item in selected_sentences
            )
            >= max_chars
        ):

            break


    return "\n".join(
        selected_sentences
    )


# ============================================================
# PUBLIC SEARCH API
# ============================================================

def search_document(
    question,
    resource_id,
    top_k=DEFAULT_TOP_K
):

    results = hybrid_search(question,resource_id,top_k)


    compressed_context = compress_context(question,results)


    return {

        "results":
            results,

        "context":
            compressed_context,

        "retrieval_method":
            "Hybrid Semantic + Lexical RAG",

        "model":
            MODEL_NAME

    }

