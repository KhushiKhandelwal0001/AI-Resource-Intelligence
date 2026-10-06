
# ============================================================
# AI RESOURCE INTELLIGENCE
# DOCUMENT PROCESSOR
# ============================================================

import os
import re

import pymupdf
from docx import Document


# ============================================================
# PDF EXTRACTION
# ============================================================

def extract_pdf(filepath):

    pages = []

    pdf = pymupdf.open(filepath)

    for page_number, page in enumerate(
        pdf,
        start=1
    ):

        text = page.get_text("text")

        if text and text.strip():

            pages.append({

                "page": page_number,

                "text": text.strip()

            })

    pdf.close()

    return pages


# ============================================================
# DOCX EXTRACTION
# ============================================================

def extract_docx(filepath):

    document = Document(filepath)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:

            paragraphs.append(text)

    full_text = "\n".join(
        paragraphs
    )

    if not full_text.strip():

        return []

    return [{

        "page": 1,

        "text": full_text

    }]


# ============================================================
# TXT EXTRACTION
# ============================================================

def extract_txt(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        text = file.read()

    if not text.strip():

        return []

    return [{

        "page": 1,

        "text": text.strip()

    }]


# ============================================================
# CONTACT INFORMATION
# ============================================================

def extract_contact_information(text):

    email_matches = re.findall(

        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

        text
    )


    phone_matches = re.findall(

        r"(?:\+91[\s-]?)?"
        r"[6-9]\d{9}",

        text
    )


    linkedin_matches = re.findall(

        r"(?:https?://)?"
        r"(?:www\.)?"
        r"linkedin\.com/[^\s]+",

        text,

        flags=re.IGNORECASE
    )


    return {

        "email":
            email_matches[0]
            if email_matches
            else "",

        "phone":
            phone_matches[0]
            if phone_matches
            else "",

        "linkedin":
            linkedin_matches[0]
            if linkedin_matches
            else ""

    }


# ============================================================
# DOCUMENT TYPE DETECTION
# ============================================================


def detect_document_type(text, filename=""):
    """
    Detect the type of uploaded document using both:
    1. Filename
    2. Extracted document text

    Filename detection is given priority because some PDFs,
    especially scanned or poorly extracted PDFs, may not expose
    useful text for document classification.
    """

    filename_text = str(filename).lower().strip()
    document_text = str(text).lower().strip()

    combined_text = f"{filename_text} {document_text}"

    # ============================================================
    # 1. ANNUAL REPORT
    # ============================================================

    annual_report_filename_keywords = [
        "annual-report",
        "annual_report",
        "annual report",
        "annualreport"
    ]

    if any(
        keyword in filename_text
        for keyword in annual_report_filename_keywords
    ):
        return "Annual Report"

    annual_report_keywords = [
        "annual report",
        "annual-report",
        "annual report 2021",
        "annual report 2022",
        "annual report 2023",
        "annual report 2024",
        "annual report 2025",
        "annual report 2026",
        "directors report",
        "director's report",
        "financial statements",
        "board of directors",
        "corporate governance",
        "auditors report",
        "auditor's report",
        "management discussion and analysis",
        "md&a",
        "balance sheet",
        "profit and loss account",
        "cash flow statement"
    ]

    annual_report_score = sum(
        1
        for keyword in annual_report_keywords
        if keyword in combined_text
    )

    if annual_report_score >= 2:
        return "Annual Report"

    # ============================================================
    # 2. CV / RESUME
    # ============================================================

    resume_filename_keywords = [
        "resume",
        "cv",
        "curriculum-vitae",
        "curriculum_vitae"
    ]

    if any(
        keyword in filename_text
        for keyword in resume_filename_keywords
    ):
        return "CV / Resume"

    resume_keywords = [
        "resume",
        "curriculum vitae",
        "professional summary",
        "career objective",
        "work experience",
        "employment history",
        "technical skills",
        "education",
        "certifications",
        "projects",
        "professional experience"
    ]

    resume_score = sum(
        1
        for keyword in resume_keywords
        if keyword in combined_text
    )

    if resume_score >= 3:
        return "CV / Resume"

    # ============================================================
    # 3. JOB DESCRIPTION
    # ============================================================

    job_keywords = [
        "job description",
        "job requirements",
        "responsibilities",
        "required skills",
        "qualifications",
        "job role",
        "candidate should",
        "experience required",
        "roles and responsibilities",
        "key responsibilities"
    ]

    job_score = sum(
        1
        for keyword in job_keywords
        if keyword in combined_text
    )

    if job_score >= 3:
        return "Job Description"

    # ============================================================
    # 4. RESEARCH PAPER
    # ============================================================

    research_keywords = [
        "abstract",
        "methodology",
        "literature review",
        "research methodology",
        "references",
        "research findings",
        "conclusion",
        "research paper",
        "experimental results"
    ]

    research_score = sum(
        1
        for keyword in research_keywords
        if keyword in combined_text
    )

    if research_score >= 4:
        return "Research Paper"

    # ============================================================
    # 5. POLICY DOCUMENT
    # ============================================================

    policy_keywords = [
        "policy framework",
        "policy document",
        "guidelines",
        "regulatory framework",
        "compliance framework",
        "policy objectives",
        "implementation framework",
        "policy recommendations"
    ]

    policy_score = sum(
        1
        for keyword in policy_keywords
        if keyword in combined_text
    )

    if policy_score >= 2:
        return "Policy Document"

    # ============================================================
    # 6. GENERAL DOCUMENT
    # ============================================================

    return "General Document"


    # --------------------------------------------------------
    # ANNUAL REPORT
    # --------------------------------------------------------

    annual_report_keywords = [

        "annual report",

        "annual-report",

        "directors report",

        "director's report",

        "financial statements",

        "board of directors",

        "corporate governance",

        "auditors report",

        "auditor's report"

    ]


    annual_report_score = sum(

        1

        for keyword
        in annual_report_keywords

        if keyword in combined_text

    )


    if annual_report_score >= 2:

        return "Annual Report"


    # --------------------------------------------------------
    # CV / RESUME
    # --------------------------------------------------------

    resume_keywords = [

        "resume",

        "curriculum vitae",

        "professional summary",

        "career objective",

        "work experience",

        "employment history",

        "technical skills",

        "education",

        "certifications"

    ]


    resume_score = sum(

        1

        for keyword
        in resume_keywords

        if keyword in combined_text

    )


    if resume_score >= 3:

        return "CV / Resume"


    # --------------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------------

    job_keywords = [

        "job description",

        "job requirements",

        "responsibilities",

        "required skills",

        "qualifications",

        "job role",

        "candidate should",

        "experience required"

    ]


    job_score = sum(

        1

        for keyword
        in job_keywords

        if keyword in combined_text

    )


    if job_score >= 3:

        return "Job Description"


    # --------------------------------------------------------
    # RESEARCH PAPER
    # --------------------------------------------------------

    research_keywords = [

        "abstract",

        "methodology",

        "literature review",

        "research methodology",

        "references",

        "research findings",

        "conclusion"

    ]


    research_score = sum(

        1

        for keyword
        in research_keywords

        if keyword in combined_text

    )


    if research_score >= 4:

        return "Research Paper"


    # --------------------------------------------------------
    # POLICY DOCUMENT
    # --------------------------------------------------------

    policy_keywords = [

        "policy framework",

        "policy document",

        "guidelines",

        "regulatory framework",

        "compliance framework",

        "policy objectives"

    ]


    policy_score = sum(

        1

        for keyword
        in policy_keywords

        if keyword in combined_text

    )


    if policy_score >= 2:

        return "Policy Document"


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    return "General Document"


# ============================================================
# SECTION DEFINITIONS
# ============================================================

SECTION_NAMES = {

    "education": [

        "education",

        "academic background",

        "academic qualification",

        "qualifications",

        "educational qualification"

    ],

    "experience": [

        "experience",

        "work experience",

        "professional experience",

        "employment",

        "work history"

    ],

    "projects": [

        "projects",

        "academic projects",

        "personal projects",

        "key projects"

    ],

    "certifications": [

        "certifications",

        "certificates",

        "courses",

        "training"

    ],

    "skills": [

        "skills",

        "technical skills",

        "technical expertise",

        "technologies",

        "core skills"

    ]

}


# ============================================================
# HEADING NORMALIZATION
# ============================================================

def normalize_heading(text):

    text = text.lower().strip()

    text = re.sub(
        r"[^a-z\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_sections(text):

    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()

    ]


    sections = {}

    current_section = None

    current_content = []


    for line in lines:

        normalized = normalize_heading(
            line
        )

        detected_section = None


        for (
            section_name,
            aliases
        ) in SECTION_NAMES.items():

            if normalized in aliases:

                detected_section = (
                    section_name
                )

                break


        if detected_section:

            if current_section:

                sections[
                    current_section
                ] = "\n".join(
                    current_content
                ).strip()


            current_section = (
                detected_section
            )

            current_content = []


        elif current_section:

            current_content.append(
                line
            )


    if current_section:

        sections[
            current_section
        ] = "\n".join(
            current_content
        ).strip()


    return sections


# ============================================================
# CLEAN EXTRACTED SKILL SECTION
# ============================================================

def clean_skill_section(
    sections,
    document_type
):

    # --------------------------------------------------------
    # IMPORTANT:
    # Annual reports, research papers and general documents
    # should NOT have arbitrary text displayed as skills.
    # --------------------------------------------------------

    if document_type != "CV / Resume":

        return ""


    skill_text = sections.get(
        "skills",
        ""
    )


    if not skill_text:

        return ""


    return skill_text.strip()


# ============================================================
# KEY INFORMATION
# ============================================================

def extract_key_information(
    sections,
    document_type
):

    key_information = {}


    # --------------------------------------------------------
    # CV / RESUME
    # --------------------------------------------------------

    if document_type == "CV / Resume":

        if sections.get("education"):

            key_information[
                "Education"
            ] = sections[
                "education"
            ]


        if sections.get("experience"):

            key_information[
                "Experience"
            ] = sections[
                "experience"
            ]


        if sections.get("projects"):

            key_information[
                "Projects"
            ] = sections[
                "projects"
            ]


        if sections.get("certifications"):

            key_information[
                "Certifications"
            ] = sections[
                "certifications"
            ]


        return key_information


    # --------------------------------------------------------
    # OTHER DOCUMENT TYPES
    # --------------------------------------------------------

    if document_type == "Annual Report":

        key_information[
            "Document Type"
        ] = "Annual Report"


        key_information[
            "Analysis"
        ] = (
            "This document has been identified "
            "as an Annual Report. Career or "
            "CV-specific skill extraction is "
            "not applicable."
        )


        return key_information


    if document_type == "Research Paper":

        key_information[
            "Document Type"
        ] = "Research Paper"


        key_information[
            "Analysis"
        ] = (
            "This document has been identified "
            "as a Research Paper. Technical "
            "skills are not inferred from "
            "research content."
        )


        return key_information


    if document_type == "Job Description":

        key_information[
            "Document Type"
        ] = "Job Description"


        key_information[
            "Analysis"
        ] = (
            "This document contains job-related "
            "requirements. Skills will be treated "
            "as job requirements rather than "
            "candidate skills."
        )


        return key_information


    # --------------------------------------------------------
    # GENERAL DOCUMENT
    # --------------------------------------------------------

    key_information[
        "Document Type"
    ] = "General Document"


    key_information[
        "Analysis"
    ] = (
        "No CV-specific skill information "
        "was identified in this document."
    )


    return key_information


# ============================================================
# MAIN DOCUMENT PROCESSOR
# ============================================================

def process_document(
    filepath,
    filename
):

    extension = (
        os.path.splitext(
            filename
        )[1]
        .lower()
    )


    # --------------------------------------------------------
    # EXTRACT TEXT
    # --------------------------------------------------------

    if extension == ".pdf":

        pages = extract_pdf(
            filepath
        )

    elif extension == ".docx":

        pages = extract_docx(
            filepath
        )

    elif extension == ".txt":

        pages = extract_txt(
            filepath
        )

    else:

        raise ValueError(
            "Unsupported document format."
        )


    # --------------------------------------------------------
    # FULL TEXT
    # --------------------------------------------------------

    full_text = "\n\n".join(

        page["text"]

        for page in pages

    )


    # --------------------------------------------------------
    # CONTACT INFORMATION
    # --------------------------------------------------------

    contact_information = (
        extract_contact_information(
            full_text
        )
    )


    # --------------------------------------------------------
    # DOCUMENT TYPE
    # --------------------------------------------------------

    document_type = (
        detect_document_type(
            full_text,
            filename
        )
    )


    # --------------------------------------------------------
    # SECTIONS
    # --------------------------------------------------------

    sections = extract_sections(
        full_text
    )


    # --------------------------------------------------------
    # CV SKILL SECTION
    # --------------------------------------------------------

    skill_section = (
        clean_skill_section(
            sections,
            document_type
        )
    )


    # --------------------------------------------------------
    # KEY INFORMATION
    # --------------------------------------------------------

    key_information = (
        extract_key_information(
            sections,
            document_type
        )
    )


    # --------------------------------------------------------
    # FINAL DOCUMENT OBJECT
    # --------------------------------------------------------

    return {

        "filename":
            filename,

        "file_type":
            extension
            .replace(
                ".",
                ""
            )
            .upper(),

        "document_type":
            document_type,

        "page_count":
            len(pages),

        "character_count":
            len(full_text),

        "word_count":
            len(
                full_text.split()
            ),

        "text":
            full_text,

        "pages":
            pages,

        "contact_information":
            contact_information,

        "sections":
            sections,

        "skill_section":
            skill_section,

        "key_information":
            key_information

    }
