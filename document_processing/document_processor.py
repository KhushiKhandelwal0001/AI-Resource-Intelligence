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

                "page":
                    page_number,

                "text":
                    text.strip()

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

            paragraphs.append(
                text
            )

    full_text = "\n".join(
        paragraphs
    )

    if not full_text.strip():

        return []

    return [{

        "page":
            1,

        "text":
            full_text

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

        "page":
            1,

        "text":
            text.strip()

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
# SECTION EXTRACTION
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


        for section_name, aliases in SECTION_NAMES.items():

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
# DOCUMENT PROCESSING
# ============================================================

def process_document(
    filepath,
    filename
):

    extension = os.path.splitext(
        filename
    )[1].lower()


    # --------------------------------------------------------
    # SELECT EXTRACTION METHOD
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
    # COMBINE TEXT
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
    # DOCUMENT SECTIONS
    # --------------------------------------------------------

    sections = extract_sections(
        full_text
    )


    # --------------------------------------------------------
    # RETURN DOCUMENT DATA
    # --------------------------------------------------------

    return {

        "filename":
            filename,

        "file_type":
            extension
            .replace(".", "")
            .upper(),

        "page_count":
            len(pages),

        "character_count":
            len(full_text),

        "word_count":
            len(full_text.split()),

        "text":
            full_text,

        "pages":
            pages,

        "contact_information":
            contact_information,

        "sections":
            sections

    }