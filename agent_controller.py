
# ============================================================
# AI RESOURCE INTELLIGENCE
# AGENT CONTROLLER
# ============================================================

import re


# ============================================================
# TECHNICAL SKILLS
# ============================================================

TECHNICAL_SKILLS = {

    "Programming": [
        "Python",
        "SQL",
        "Java",
        "JavaScript",
        "C++"
    ],

    "Data Analytics": [
        "Pandas",
        "NumPy",
        "EDA",
        "Exploratory Data Analysis",
        "Data Analytics"
    ],

    "Data Visualization": [
        "Power BI",
        "Tableau",
        "Matplotlib",
        "Seaborn",
        "Plotly",
        "Data Visualization"
    ],

    "Statistics": [
        "Statistics",
        "Statistical Analysis",
        "Hypothesis Testing",
        "Regression"
    ],

    "Machine Learning": [
        "Machine Learning",
        "Random Forest",
        "Logistic Regression",
        "Decision Tree",
        "XGBoost",
        "Classification",
        "Clustering"
    ],

    "Artificial Intelligence": [
        "Artificial Intelligence",
        "AI",
        "NLP",
        "Natural Language Processing",
        "Generative AI",
        "GenAI",
        "RAG",
        "Retrieval Augmented Generation",
        "LLM",
        "Large Language Model"
    ],

    "Development": [
        "Flask",
        "REST API",
        "API",
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "GitHub"
    ],

    "Databases": [
        "SQL",
        "SQLite",
        "MySQL",
        "PostgreSQL"
    ],

    "Document AI": [
        "PyMuPDF",
        "OCR",
        "Tesseract",
        "Document Processing",
        "Document Intelligence",
        "Embeddings",
        "Vector Search",
        "Semantic Search"
    ],

    "Agentic AI": [
        "Agentic AI",
        "AI Agents",
        "Multi-Agent",
        "Multi Agent",
        "Agent Architecture",
        "Agent Controller",
        "Workflow Orchestration"
    ],

    "Generative AI": [
        "Generative AI",
        "GenAI",
        "Prompt Engineering",
        "Large Language Model",
        "LLM",
        "Text Generation"
    ],

    "Engineering": [
        "Data Pipeline",
        "Data Pipelines",
        "ETL",
        "Web Scraping",
        "BeautifulSoup",
        "JSON",
        "Automation"
    ]
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    if not text:

        return ""

    text = str(text)

    text = text.replace(
        "\n",
        " "
    )

    text = text.replace(
        "\r",
        " "
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.lower().strip()


# ============================================================
# SKILL MATCHING
# ============================================================

def skill_exists(
    text,
    skill
):

    normalized_text = normalize_text(
        text
    )

    normalized_skill = normalize_text(
        skill
    )


    if not normalized_skill:

        return False


    if " " in normalized_skill:

        return (
            normalized_skill
            in normalized_text
        )


    if len(normalized_skill) <= 4:

        pattern = (
            rf"\b"
            rf"{re.escape(normalized_skill)}"
            rf"\b"
        )

        return bool(
            re.search(
                pattern,
                normalized_text
            )
        )


    return (
        normalized_skill
        in normalized_text
    )


# ============================================================
# SKILL AGENT
# ============================================================

def skill_agent(text):

    detected_skills = {}

    if not text:

        return detected_skills


    for category, skills in (
        TECHNICAL_SKILLS.items()
    ):

        found_skills = []


        for skill in skills:

            if skill_exists(
                text,
                skill
            ):

                if skill not in found_skills:

                    found_skills.append(
                        skill
                    )


        if found_skills:

            detected_skills[
                category
            ] = found_skills


    return detected_skills


# ============================================================
# ANALYTICS AGENT
# ============================================================

def analytics_agent(
    text,
    skills
):

    normalized_text = normalize_text(
        text
    )

    word_count = len(
        normalized_text.split()
    )


    skill_count = sum(

        len(skill_list)

        for skill_list
        in skills.values()

        if isinstance(
            skill_list,
            list
        )

    )


    return {

        "word_count":
            word_count,

        "skill_categories":
            len(skills),

        "detected_skills":
            skill_count,

        "technical_coverage":

            "High"

            if skill_count >= 10

            else "Moderate"

            if skill_count >= 5

            else "Developing"

    }


# ============================================================
# INSIGHT AGENT
# ============================================================

def insight_agent(
    skills,
    document_type
):

    insights = []


    if document_type != "CV / Resume":

        return [

            {
                "title":
                    "Document Intelligence",

                "description":
                    f"The document was identified as a "
                    f"{document_type}. CV-specific skill "
                    f"analysis is not applied."
            }

        ]


    categories = set(
        skills.keys()
    )


    if (
        "Data Analytics"
        in categories
        or
        "Data Visualization"
        in categories
        or
        "Statistics"
        in categories
    ):

        insights.append({

            "title":
                "📊 Analytics Capability",

            "description":
                "The profile demonstrates data "
                "analytics and analytical "
                "problem-solving capabilities."

        })


    if "Machine Learning" in categories:

        insights.append({

            "title":
                "🤖 Machine Learning Capability",

            "description":
                "The profile demonstrates exposure "
                "to machine learning techniques "
                "and predictive modelling."

        })


    if (
        "Artificial Intelligence"
        in categories
        or
        "Generative AI"
        in categories
        or
        "Agentic AI"
        in categories
    ):

        insights.append({

            "title":
                "🧠 AI Capability",

            "description":
                "The profile contains Artificial "
                "Intelligence, Generative AI or "
                "intelligent-agent capabilities."

        })


    if (
        "Programming"
        in categories
        or
        "Development"
        in categories
    ):

        insights.append({

            "title":
                "💻 Development Capability",

            "description":
                "The profile contains programming "
                "and software development capabilities."

        })


    if not insights:

        insights.append({

            "title":
                "🔎 Skill Analysis",

            "description":
                "No significant technical skills "
                "were detected in the CV / Resume."

        })


    return insights


# ============================================================
# CAREER AGENT
# ============================================================

def career_agent(
    skills,
    document_type
):

    if document_type != "CV / Resume":

        return []


    career_scores = {}

    categories = set(
        skills.keys()
    )


    # --------------------------------------------------------
    # AI / ML ENGINEER
    # --------------------------------------------------------

    score = 0

    if "Artificial Intelligence" in categories:
        score += 30

    if "Machine Learning" in categories:
        score += 30

    if "Programming" in categories:
        score += 20

    if "Development" in categories:
        score += 20

    if score:

        career_scores[
            "AI / ML Engineer"
        ] = min(
            score,
            100
        )


    # --------------------------------------------------------
    # AI / RAG ENGINEER
    # --------------------------------------------------------

    score = 0

    if "Artificial Intelligence" in categories:
        score += 25

    if "Generative AI" in categories:
        score += 25

    if "Document AI" in categories:
        score += 20

    if "Agentic AI" in categories:
        score += 20

    if "Development" in categories:
        score += 10

    if score:

        career_scores[
            "AI / RAG Engineer"
        ] = min(
            score,
            100
        )


    # --------------------------------------------------------
    # DATA ANALYST
    # --------------------------------------------------------

    score = 0

    if "Data Analytics" in categories:
        score += 35

    if "Data Visualization" in categories:
        score += 25

    if "Statistics" in categories:
        score += 20

    if "Databases" in categories:
        score += 20

    if score:

        career_scores[
            "Data Analyst"
        ] = min(
            score,
            100
        )


    # --------------------------------------------------------
    # DATA SCIENTIST
    # --------------------------------------------------------

    score = 0

    if "Data Analytics" in categories:
        score += 20

    if "Statistics" in categories:
        score += 20

    if "Machine Learning" in categories:
        score += 30

    if "Programming" in categories:
        score += 20

    if "Data Visualization" in categories:
        score += 10

    if score:

        career_scores[
            "Data Scientist"
        ] = min(
            score,
            100
        )


    # --------------------------------------------------------
    # GENERATIVE AI ENGINEER
    # --------------------------------------------------------

    score = 0

    if "Generative AI" in categories:
        score += 35

    if "Artificial Intelligence" in categories:
        score += 25

    if "Agentic AI" in categories:
        score += 20

    if "Development" in categories:
        score += 20

    if score:

        career_scores[
            "Generative AI Engineer"
        ] = min(
            score,
            100
        )


    # --------------------------------------------------------
    # BUSINESS ANALYST
    # --------------------------------------------------------

    score = 0

    if "Data Analytics" in categories:
        score += 35

    if "Statistics" in categories:
        score += 20

    if "Data Visualization" in categories:
        score += 25

    if "Databases" in categories:
        score += 20

    if score:

        career_scores[
            "Business Analyst"
        ] = min(
            score,
            100
        )


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    sorted_careers = sorted(

        career_scores.items(),

        key=lambda item:
            item[1],

        reverse=True

    )


    return [

        {

            "role":
                role,

            "match_percentage":
                percentage

        }

        for role, percentage
        in sorted_careers

    ]


# ============================================================
# SUMMARY AGENT
# ============================================================

def summary_agent(
    text,
    skills,
    careers,
    document_type
):

    if document_type == "Annual Report":

        return (
            "This resource has been identified "
            "as an Annual Report. The system "
            "has processed the document for "
            "document intelligence and semantic "
            "search. CV-specific career and "
            "technical skill extraction is not "
            "applied to this document."
        )


    if document_type != "CV / Resume":

        return (
            f"This resource has been identified "
            f"as a {document_type}. The document "
            f"has been processed using AI-powered "
            f"document intelligence."
        )


    if not text:

        return (
            "No readable text was detected "
            "in the uploaded CV / Resume."
        )


    categories = list(
        skills.keys()
    )


    summary_parts = []


    if categories:

        category_text = ", ".join(
            categories
        )

        summary_parts.append(

            "The CV / Resume demonstrates "
            f"capabilities across "
            f"{category_text}."

        )

    else:

        summary_parts.append(

            "No significant technical skills "
            "were detected in the CV / Resume."

        )


    if careers:

        top_careers = [

            career["role"]

            for career
            in careers[:3]

        ]

        career_text = ", ".join(
            top_careers
        )

        summary_parts.append(

            "Potential career areas include "
            f"{career_text}."

        )


    return " ".join(
        summary_parts
    )


# ============================================================
# MAIN ANALYSIS CONTROLLER
# ============================================================

def analyse_resource(
    document_data
):

    if not document_data:

        return {

            "skills": {},

            "analytics": {},

            "insights": [],

            "career_matches": [],

            "summary":
                "No document data available."

        }


    text = document_data.get(
        "text",
        ""
    )


    document_type = document_data.get(
        "document_type",
        "General Document"
    )


    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    if document_type == "CV / Resume":

        skills = skill_agent(
            text
        )

    else:

        skills = {}


    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    analytics = analytics_agent(

        text,

        skills

    )


    # --------------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------------

    insights = insight_agent(

        skills,

        document_type

    )


    # --------------------------------------------------------
    # CAREER
    # --------------------------------------------------------

    careers = career_agent(

        skills,

        document_type

    )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    summary = summary_agent(

        text,

        skills,

        careers,

        document_type

    )


    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return {

        "document_type":
            document_type,

        "skills":
            skills,

        "analytics":
            analytics,

        "insights":
            insights,

        "career_matches":
            careers,

        "summary":
            summary,

        "key_information":
            document_data.get(
                "key_information",
                {}
            ),

        "agent_status": {

            "skill_agent":
                "Completed",

            "analytics_agent":
                "Completed",

            "insight_agent":
                "Completed",

            "career_agent":
                "Completed",

            "summary_agent":
                "Completed"

        }

    }
