
# ============================================================
# AI RESOURCE INTELLIGENCE
# TECHNOLOGY & BACKEND INTELLIGENCE ANALYZER
# ============================================================

import re


TECHNOLOGY_RULES = [
    {
        "name": "Python",
        "category": "Programming Language",
        "patterns": [
            r"\bimport\s+(?:pandas|numpy|flask|django|"
            r"sklearn|torch|tensorflow|requests)\b",
            r"\bdef\s+\w+\s*\(",
            r"\bif\s+__name__\s*==\s*['\"]__main__['\"]",
            r"\bprint\s*\("
        ],
        "mentions": [r"\bpython\b"],
    },
    {
        "name": "SQL",
        "category": "Database Query Language",
        "patterns": [
            r"\bSELECT\b[\s\S]{0,500}?\bFROM\b",
            r"\bINSERT\s+INTO\b",
            r"\bUPDATE\s+\w+\s+SET\b",
            r"\bCREATE\s+TABLE\b",
            r"\bDELETE\s+FROM\b",
        ],
        "mentions": [r"\bSQL\b"],
    },
    {
        "name": "JavaScript",
        "category": "Programming Language",
        "patterns": [
            r"\bfunction\s+\w+\s*\(",
            r"\bconst\s+\w+\s*=",
            r"\blet\s+\w+\s*=",
            r"\bdocument\.querySelector\b",
            r"\baddEventListener\s*\(",
        ],
        "mentions": [r"\bJavaScript\b"],
    },
    {
        "name": "HTML",
        "category": "Frontend",
        "patterns": [
            r"<!DOCTYPE\s+html",
            r"<html[\s>]",
            r"<body[\s>]",
        ],
        "mentions": [r"\bHTML\b"],
    },
    {
        "name": "CSS",
        "category": "Frontend",
        "patterns": [
            r"\{[^{}]{0,300}(?:color|margin|padding|display)\s*:",
            r"<style[\s>]",
        ],
        "mentions": [r"\bCSS\b"],
    },
    {
        "name": "Flask",
        "category": "Backend Framework",
        "patterns": [
            r"\bfrom\s+flask\s+import\b",
            r"\bFlask\s*\(",
            r"@\w+\.route\s*\(",
        ],
        "mentions": [r"\bFlask\b"],
    },
    {
        "name": "Django",
        "category": "Backend Framework",
        "patterns": [
            r"\bfrom\s+django\b",
            r"\bmodels\.Model\b",
            r"\burlpatterns\s*=",
        ],
        "mentions": [r"\bDjango\b"],
    },
    {
        "name": "Pandas",
        "category": "Data Analysis",
        "patterns": [
            r"\bimport\s+pandas\b",
            r"\bpd\.read_(?:csv|excel|json|sql)\s*\(",
            r"\bpd\.DataFrame\s*\(",
        ],
        "mentions": [r"\bpandas\b"],
    },
    {
        "name": "NumPy",
        "category": "Scientific Computing",
        "patterns": [
            r"\bimport\s+numpy\b",
            r"\bnp\.(?:array|mean|median|std|reshape)\s*\(",
        ],
        "mentions": [r"\bNumPy\b", r"\bnumpy\b"],
    },
    {
        "name": "Scikit-learn",
        "category": "Machine Learning",
        "patterns": [
            r"\bfrom\s+sklearn\.",
            r"\bsklearn\.",
        ],
        "mentions": [
            r"\bscikit-learn\b",
            r"\bsklearn\b",
        ],
    },
    {
        "name": "TensorFlow",
        "category": "Deep Learning",
        "patterns": [
            r"\bimport\s+tensorflow\b",
            r"\btf\.keras\b",
        ],
        "mentions": [r"\bTensorFlow\b", r"\btensorflow\b"],
    },
    {
        "name": "PyTorch",
        "category": "Deep Learning",
        "patterns": [
            r"\bimport\s+torch\b",
            r"\btorch\.nn\b",
        ],
        "mentions": [r"\bPyTorch\b", r"\btorch\b"],
    },
    {
        "name": "SQLite",
        "category": "Database",
        "patterns": [
            r"\bsqlite3\.connect\s*\(",
            r"\bimport\s+sqlite3\b",
        ],
        "mentions": [r"\bSQLite\b", r"\bSQLite3\b"],
    },
    {
        "name": "MySQL",
        "category": "Database",
        "patterns": [
            r"\bmysql\.connector\b",
            r"\bimport\s+pymysql\b",
        ],
        "mentions": [r"\bMySQL\b"],
    },
    {
        "name": "PostgreSQL",
        "category": "Database",
        "patterns": [
            r"\bimport\s+psycopg2\b",
            r"\bpsycopg\.connect\s*\(",
        ],
        "mentions": [r"\bPostgreSQL\b", r"\bPostgres\b"],
    },
    {
        "name": "MongoDB",
        "category": "Database",
        "patterns": [
            r"\bMongoClient\s*\(",
            r"\bfrom\s+pymongo\b",
        ],
        "mentions": [r"\bMongoDB\b"],
    },
    {
        "name": "REST API",
        "category": "Backend Integration",
        "patterns": [
            r"\brequests\.(?:get|post|put|delete|patch)\s*\(",
            r"\bfetch\s*\(",
            r"@\w+\.route\s*\(",
            r"\bapp\.add_url_rule\s*\(",
        ],
        "mentions": [
            r"\bREST\s+API\b",
            r"\bRESTful\s+API\b",
        ],
    },
    {
        "name": "RAG",
        "category": "Generative AI",
        "patterns": [
            r"\bretriev(?:er|al)\b.{0,100}\bgenerat(?:ion|ive)\b",
            r"\b(?:vector|semantic)\s+search\b",
            r"\bSentenceTransformer\s*\(",
        ],
        "mentions": [
            r"\bRAG\b",
            r"\bretrieval[- ]augmented generation\b",
        ],
    },
    {
        "name": "Sentence Transformers",
        "category": "Embeddings",
        "patterns": [
            r"\bfrom\s+sentence_transformers\s+import\b",
            r"\bSentenceTransformer\s*\(",
        ],
        "mentions": [r"\bSentence Transformers\b"],
    },
    {
        "name": "Power BI",
        "category": "Business Intelligence",
        "patterns": [],
        "mentions": [r"\bPower\s*BI\b"],
    },
    {
        "name": "Tableau",
        "category": "Business Intelligence",
        "patterns": [],
        "mentions": [r"\bTableau\b"],
    },
]


def _get_document_pages(document_data):
    """Return document text as page-aware records."""

    pages = document_data.get("pages", [])

    if isinstance(pages, list) and pages:
        return [
            {
                "page": item.get("page", index + 1),
                "text": str(item.get("text", "")),
            }
            for index, item in enumerate(pages)
            if isinstance(item, dict) and item.get("text")
        ]

    text = str(document_data.get("text", ""))

    return [{"page": None, "text": text}] if text else []



def _find_evidence(patterns, text, limit=3):
    """Return concise, relevant evidence snippets."""

    evidence = []

    # Analyze individual lines to avoid returning the entire
    # document as evidence for every technology.
    lines = text.splitlines()

    for pattern in patterns:
        try:
            compiled_pattern = re.compile(
                pattern,
                flags=re.IGNORECASE,
            )

            for line_number, line in enumerate(lines, start=1):
                if not compiled_pattern.search(line):
                    continue

                excerpt = line.strip()

                # Avoid overly long evidence snippets.
                if len(excerpt) > 220:
                    excerpt = excerpt[:217] + "..."

                if excerpt and excerpt not in evidence:
                    evidence.append(excerpt)

                if len(evidence) >= limit:
                    return evidence

        except re.error:
            continue

    return evidence



def analyze_technologies(document_data):
    """
    Analyze technologies mentioned or evidenced in a document.

    This performs static text-pattern analysis. It does not execute
    code or prove that a program ran successfully.
    """

    if not isinstance(document_data, dict):
        document_data = {"text": str(document_data or "")}

    pages = _get_document_pages(document_data)

    findings = []

    for technology in TECHNOLOGY_RULES:
        code_evidence = []
        mention_evidence = []
        evidence_pages = set()

        for page_data in pages:
            page_text = page_data["text"]
            page_number = page_data["page"]

            # Patterns indicate code/query-like evidence.
            matches = _find_evidence(
                technology["patterns"],
                page_text,
            )

            for excerpt in matches:
                code_evidence.append(excerpt)

                if page_number is not None:
                    evidence_pages.add(page_number)

            # Mentions are reported separately from code evidence.
            mentions = _find_evidence(
                technology["mentions"],
                page_text,
            )

            for excerpt in mentions:
                mention_evidence.append(excerpt)

                if page_number is not None:
                    evidence_pages.add(page_number)

        if code_evidence:
            status = "Code-pattern evidence detected"
            confidence = "Higher"
        elif mention_evidence:
            status = "Mentioned; usage not verified"
            confidence = "Limited"
        else:
            continue

        findings.append({
            "technology": technology["name"],
            "category": technology["category"],
            "status": status,
            "confidence": confidence,
            "code_evidence": code_evidence[:3],
            "mention_evidence": mention_evidence[:3],
            "pages": sorted(evidence_pages),
        })

    code_detected = sum(
        item["status"] == "Code-pattern evidence detected"
        for item in findings
    )

    mentioned_only = sum(
        item["status"] == "Mentioned; usage not verified"
        for item in findings
    )

    return {
        "status": "Completed",
        "method": "Evidence-based static technology analysis",
        "document_pages_analyzed": len(pages),
        "summary": {
            "technologies_found": len(findings),
            "code_pattern_evidence": code_detected,
            "mentioned_not_verified": mentioned_only,
        },
        "findings": findings,
        "limitations": [
            "Pattern matches are evidence, not proof that code executed.",
            "A mention does not confirm that a technology was used.",
            "Absence of a finding does not prove a technology was not used.",
            "Source-code files provide stronger evidence than CV descriptions.",
        ],
    }
