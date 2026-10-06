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
# SKILL AGENT
# ============================================================

def skill_agent(text):

    detected = {}

    text_lower = text.lower()

    for category, skills in TECHNICAL_SKILLS.items():

        found = []

        for skill in skills:

            if skill.lower() in text_lower:

                if skill not in found:
                    found.append(skill)

        if found:
            detected[category] = found

    return detected


# ============================================================
# ANALYTICS AGENT
# ============================================================

def analytics_agent(text, skills):

    words = text.split()

    sentences = [
        sentence.strip()
        for sentence in text.split(".")
        if sentence.strip()
    ]

    total_skills = sum(
        len(values)
        for values in skills.values()
    )

    return {

        "character_count": len(text),

        "word_count": len(words),

        "sentence_count": len(sentences),

        "skill_categories": len(skills),

        "total_detected_skills": total_skills

    }


# ============================================================
# INSIGHT AGENT
# ============================================================

def insight_agent(skills):

    insights = []

    if "Programming" in skills:

        insights.append(
            "The resource demonstrates programming capabilities."
        )

    if "Data Analytics" in skills:

        insights.append(
            "The profile demonstrates data analytics and data-processing capabilities."
        )

    if "Data Visualization" in skills:

        insights.append(
            "The profile includes data visualization and dashboard-oriented capabilities."
        )

    if "Statistics" in skills:

        insights.append(
            "The profile demonstrates exposure to statistical analysis."
        )

    if "Machine Learning" in skills:

        insights.append(
            "The resource demonstrates exposure to machine learning techniques."
        )

    if "Artificial Intelligence" in skills:

        insights.append(
            "The resource contains AI, NLP, GenAI or RAG-related capabilities."
        )

    if "Document AI" in skills:

        insights.append(
            "The profile contains document intelligence, semantic search or retrieval-oriented capabilities."
        )

    if "Agentic AI" in skills:

        insights.append(
            "The profile demonstrates exposure to AI agent architecture and workflow orchestration."
        )

    if "Development" in skills:

        insights.append(
            "The profile contains software development and API development exposure."
        )

    return insights


# ============================================================
# CAREER INTELLIGENCE AGENT
# ============================================================

def career_agent(skills):

    roles = {}

    role_rules = {

        "Data Analyst": [
            "Programming",
            "Data Analytics",
            "Data Visualization",
            "Statistics"
        ],

        "Business Analyst": [
            "Data Analytics",
            "Data Visualization",
            "Statistics",
            "Programming"
        ],

        "Data Scientist": [
            "Programming",
            "Data Analytics",
            "Statistics",
            "Machine Learning"
        ],

        "AI / ML Engineer": [
            "Programming",
            "Machine Learning",
            "Artificial Intelligence",
            "Development"
        ],

        "Generative AI Engineer": [
            "Programming",
            "Artificial Intelligence",
            "Document AI",
            "Development"
        ],

        "AI / RAG Engineer": [
            "Artificial Intelligence",
            "Document AI",
            "Development",
            "Generative AI"
        ]
    }

    for role, categories in role_rules.items():

        matched_categories = [

            category

            for category in categories

            if category in skills

        ]

        score = round(

            (
                len(matched_categories)
                /
                len(categories)
            )
            * 100

        )

        roles[role] = {

            "score": score,

            "matched_categories":
                matched_categories,

            "required_categories":
                categories

        }

    return dict(

        sorted(

            roles.items(),

            key=lambda item:
                item[1]["score"],

            reverse=True

        )

    )


# ============================================================
# SUMMARY AGENT
# ============================================================

def summary_agent(text, skills, careers):

    summary_parts = []

    summary_parts.append(

        "The uploaded resource was analysed using "
        "document processing, skill extraction, "
        "analytics and career intelligence."

    )

    if skills:

        categories = ", ".join(
            skills.keys()
        )

        summary_parts.append(

            f"The resource demonstrates capabilities "
            f"across {categories}."

        )

    if careers:

        top_roles = list(
            careers.keys()
        )[:3]

        summary_parts.append(

            "The strongest potential career areas are "
            + ", ".join(top_roles)
            + "."

        )

    return " ".join(summary_parts)


# ============================================================
# MAIN AGENT CONTROLLER
# ============================================================

def analyse_resource(document_data):

    text = document_data.get(
        "text",
        ""
    )

    # Step 1: Skill Agent
    skills = skill_agent(text)

    # Step 2: Analytics Agent
    analytics = analytics_agent(
        text,
        skills
    )

    # Step 3: Insight Agent
    insights = insight_agent(
        skills
    )

    # Step 4: Career Agent
    careers = career_agent(
        skills
    )

    # Step 5: Summary Agent
    summary = summary_agent(
        text,
        skills,
        careers
    )

    return {

        "skills": skills,

        "analytics": analytics,

        "insights": insights,

        "career_matches": careers,

        "summary": summary

    }

# ============================================================
# AI RESEARCH / KNOWLEDGE SEARCH AGENT
# ============================================================

def search_resource(question, document_data=None):

    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": []
        }

    document_data = document_data or {}

    text = document_data.get("text", "")

    skills = skill_agent(text)

    question_lower = question.lower()

    # --------------------------------------------------------
    # CV / PROFILE QUESTIONS
    # --------------------------------------------------------

    if any(
        keyword in question_lower
        for keyword in [
            "my skills",
            "my skill",
            "what skills",
            "skills do i have",
            "skills i have"
        ]
    ):

        if skills:

            skill_text = []

            for category, values in skills.items():

                skill_text.append(
                    f"{category}: "
                    + ", ".join(values)
                )

            answer = (
                "Based on the uploaded document, "
                "the detected skills are:\n\n"
                + "\n".join(skill_text)
            )

        else:

            answer = (
                "I could not detect technical skills "
                "from the uploaded document."
            )

        return {
            "answer": answer,
            "sources": [
                "Uploaded document"
            ]
        }

    # --------------------------------------------------------
    # CAREER QUESTIONS
    # --------------------------------------------------------

    if any(
        keyword in question_lower
        for keyword in [
            "career",
            "job role",
            "job roles",
            "which role",
            "which job"
        ]
    ):

        careers = career_agent(skills)

        top_roles = list(careers.items())[:5]

        if top_roles:

            career_lines = []

            for role, information in top_roles:

                career_lines.append(
                    f"{role} — "
                    f"{information['score']}% match"
                )

            answer = (
                "Based on the skills detected in your "
                "document, these are the strongest "
                "potential career directions:\n\n"
                + "\n".join(career_lines)
            )

        else:

            answer = (
                "I need more skill information from "
                "your document before recommending "
                "career directions."
            )

        return {
            "answer": answer,
            "sources": [
                "Career Intelligence Agent",
                "Uploaded document"
            ]
        }

    # --------------------------------------------------------
    # RAG / AI QUESTIONS
    # --------------------------------------------------------

    if any(
        keyword in question_lower
        for keyword in [
            "rag",
            "retrieval augmented generation",
            "vector database",
            "embeddings",
            "semantic search",
            "llm",
            "large language model",
            "generative ai",
            "genai",
            "agentic ai",
            "ai agent"
        ]
    ):

        answer = (
            "This platform is being designed with a "
            "Retrieval-Augmented Generation (RAG) architecture. "
            "RAG combines document retrieval with AI-generated "
            "answers. In this system, documents can be converted "
            "into chunks, transformed into embeddings and searched "
            "semantically to retrieve relevant information before "
            "generating an answer."
        )

        return {
            "answer": answer,
            "sources": [
                "AI Knowledge Base"
            ]
        }

    # --------------------------------------------------------
    # DATA ANALYTICS QUESTIONS
    # --------------------------------------------------------

    if any(
        keyword in question_lower
        for keyword in [
            "data analyst",
            "data analytics",
            "data analysis",
            "power bi",
            "tableau",
            "sql"
        ]
    ):

        answer = (
            "A strong Data Analyst skill set generally includes "
            "SQL, Python or another analytical programming language, "
            "Excel, statistics, data cleaning, exploratory data "
            "analysis and visualization tools such as Power BI "
            "or Tableau. Practical projects and business problem "
            "solving are also important."
        )

        return {
            "answer": answer,
            "sources": [
                "AI Knowledge Base"
            ]
        }

    # --------------------------------------------------------
    # MACHINE LEARNING QUESTIONS
    # --------------------------------------------------------

    if any(
        keyword in question_lower
        for keyword in [
            "machine learning",
            "random forest",
            "logistic regression",
            "xgboost",
            "classification",
            "clustering"
        ]
    ):

        answer = (
            "Machine Learning is a branch of AI where models "
            "learn patterns from data. Common areas include "
            "supervised learning, unsupervised learning, "
            "classification, regression and clustering. "
            "Python libraries such as scikit-learn and XGBoost "
            "are widely used for practical machine-learning "
            "projects."
        )

        return {
            "answer": answer,
            "sources": [
                "AI Knowledge Base"
            ]
        }

    # --------------------------------------------------------
    # GENERAL QUESTION
    # --------------------------------------------------------

    answer = (
        "I received your question:\n\n"
        f"\"{question}\"\n\n"
        "The AI Research Assistant is currently using the "
        "uploaded resource and the platform's knowledge "
        "modules. The next RAG upgrade will allow this "
        "assistant to retrieve relevant document chunks "
        "and provide more detailed, source-aware answers."
    )

    return {
        "answer": answer,
        "sources": [
            "AI Resource Intelligence Platform"
        ]
    }