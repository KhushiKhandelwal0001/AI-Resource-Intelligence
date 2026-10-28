
# ============================================================
# AI RESOURCE INTELLIGENCE PLATFORM
# MAIN FLASK APPLICATION
# ============================================================

import os
import uuid
import traceback

from agents.document_analysis import analyze_document
from agents.ppt_generator import create_document_presentation

from flask import ( Flask, render_template, request, jsonify,send_from_directory
)
from flask_cors import CORS
from werkzeug.utils import secure_filename

from document_processing.document_processor import process_document
from agents.agent_controller import analyse_resource
from agents.resource_agent import resource_agent
from rag.retriever import build_embeddings

from agents.technology_analyzer import analyze_technologies

# ============================================================
# APPLICATION SETUP
# ============================================================

app = Flask(__name__)

CORS(app)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# FOLDERS
# ============================================================

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "uploads"
)

PROCESSED_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

EMBEDDING_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "embeddings"
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER
app.config["EMBEDDING_FOLDER"] = EMBEDDING_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

# Maximum upload size: 25 MB

app.config["MAX_CONTENT_LENGTH"] = (
    25 * 1024 * 1024
)


# ============================================================
# ALLOWED FILE TYPES
# ============================================================

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt",
    "pptx"
}


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    PROCESSED_FOLDER,
    exist_ok=True
)

os.makedirs(
    EMBEDDING_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def allowed_file(filename):
    """
    Check whether the uploaded file
    has a supported extension.
    """

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# RESOURCE INTELLIGENCE PAGE
# ============================================================

@app.route("/resource-intelligence")
def resource_intelligence():

    return render_template(
        "index.html"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({

        "status": "online",

        "application":
            "AI Resource Intelligence Platform",

        "version":
            "1.0.0",

        "modules": [

            "Document Processing",

            "Document Information",

            "Document Summary",

            "Key Information Extraction",

            "Skill Extraction",

            "Analytics",

            "Career Matching",

            "RAG",

            "Semantic Search",

            "Resource Intelligence Agent",

            "Generative AI Ready"
        ]
    })


# ============================================================
# UPLOAD RESOURCE
# ============================================================

@app.route(
    "/api/upload",
    methods=["POST"]
)
def upload_resource():

    filepath = None

    try:

        # ----------------------------------------------------
        # CHECK FILE
        # ----------------------------------------------------

        if "file" not in request.files:

            return jsonify({

                "success": False,

                "message":
                    "No file uploaded."

            }), 400


        file = request.files["file"]


        # ----------------------------------------------------
        # CHECK FILE NAME
        # ----------------------------------------------------

        if file.filename == "":

            return jsonify({

                "success": False,

                "message":
                    "Please select a file."

            }), 400


        # ----------------------------------------------------
        # CHECK FILE TYPE
        # ----------------------------------------------------

        if not allowed_file(
            file.filename
        ):

            return jsonify({

                "success": False,

                "message":
                    "Unsupported file format. "
                    "Please upload PDF, DOCX , TXT or create presentation file."

            }), 400


        # ----------------------------------------------------
        # CREATE RESOURCE ID
        # ----------------------------------------------------

        resource_id = str(
            uuid.uuid4()
        )


        # ----------------------------------------------------
        # SECURE FILE NAME
        # ----------------------------------------------------

        original_filename = secure_filename(
            file.filename
        )


        # ----------------------------------------------------
        # GET EXTENSION
        # ----------------------------------------------------

        extension = (
            original_filename
            .rsplit(
                ".",
                1
            )[1]
            .lower()
        )


        # ----------------------------------------------------
        # CREATE STORED FILE NAME
        # ----------------------------------------------------

        stored_filename = (
            f"{resource_id}.{extension}"
        )


        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            stored_filename
        )


        # ----------------------------------------------------
        # SAVE FILE
        # ----------------------------------------------------

        file.save(filepath)


        # ----------------------------------------------------
        # PROCESS DOCUMENT
        # ----------------------------------------------------

        document_data = process_document(
            filepath,
            original_filename
        )


        document_data[
            "resource_id"
        ] = resource_id


        # ----------------------------------------------------
        # AI ANALYSIS
        # ----------------------------------------------------

        analysis = analyse_resource(
            document_data
        )

        analysis["technology_intelligence"] = (
    analyze_technologies(document_data)
)


        # ----------------------------------------------------
        # BUILD RAG EMBEDDINGS
        # ----------------------------------------------------

        

        rag_data = build_embeddings(
            document_data,
            resource_id
        )


        # ----------------------------------------------------
        # RAG STATUS
        # ----------------------------------------------------

        analysis["rag"] = {

            "enabled": True,

            "status":
                "Ready"
                if rag_data
                else "No readable content",

            "model":
                "all-MiniLM-L6-v2",

            "search_type":
                "Semantic Search"
        }


        # ----------------------------------------------------
        # SUCCESS RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "resource_id":
                resource_id,

            "filename":
                original_filename,

            "document":
                document_data,

            "analysis":
                analysis

        })


    except Exception as error:

        # ----------------------------------------------------
        # PRINT ERROR IN TERMINAL
        # ----------------------------------------------------

        print()
        print("=" * 70)
        print("RESOURCE ANALYSIS ERROR")
        print("=" * 70)

        print(
            traceback.format_exc()
        )

        print("=" * 70)
        print()


        # ----------------------------------------------------
        # DELETE FAILED UPLOAD
        # ----------------------------------------------------

        try:

            if filepath:

                if os.path.exists(filepath):

                    os.remove(filepath)

        except Exception:

            pass


        # ----------------------------------------------------
        # RETURN JSON ERROR
        # ----------------------------------------------------

        return jsonify({

            "success": False,

            "message":
                "Resource analysis failed.",

            "error":
                str(error),

            "type":
                type(error).__name__

        }), 500



# ============================================================
# DETAILED DOCUMENT ANALYSIS API
# ============================================================

@app.route("/api/analyze-document", methods=["POST"])
def analyze_document_api():
    try:
        payload = request.get_json(silent=True) or {}
        document_data = payload.get("document")

        if not isinstance(document_data, dict):
            return jsonify({
                "success": False,
                "message": "A valid document object is required."
            }), 400

        if not str(document_data.get("text", "")).strip():
            return jsonify({
                "success": False,
                "message": "The document contains no readable text."
            }), 400

        result = analyze_document(document_data)

        return jsonify({
            "success": True,
            "analysis": result
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400

    except Exception:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": "Detailed document analysis failed."
        }), 500


# ============================================================
# CREATE EDITABLE 20-SLIDE POWERPOINT
# ============================================================

@app.route("/api/create-ppt", methods=["POST"])
def create_ppt_api():
    try:
        payload = request.get_json(silent=True) or {}
        document_data = payload.get("document")

        if not isinstance(document_data, dict):
            return jsonify({
                "success": False,
                "message": "A valid document object is required."
            }), 400

        if not str(document_data.get("text", "")).strip():
            return jsonify({
                "success": False,
                "message": "Upload a readable document first."
            }), 400

        # Always build the evidence-grounded analysis on the server.
        # Preserve other existing analysis fields if supplied.
        detailed_analysis = analyze_document(document_data)
        combined_analysis = dict(payload.get("analysis") or {})
        combined_analysis.update(detailed_analysis)

        filename = f"{uuid.uuid4().hex}.pptx"
        output_path = os.path.join(
            app.config["REPORT_FOLDER"],
            filename
        )

        result = create_document_presentation(
            document_data=document_data,
            analysis=combined_analysis,
            output_path=output_path,
        )

        return jsonify({
            "success": True,
            "message": "20-slide PowerPoint created successfully.",
            "filename": result["filename"],
            "slide_count": result["slide_count"],
            "size_bytes": result["size_bytes"],
            "download_url": f"/download/{result['filename']}",
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400

    except Exception:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": "PowerPoint generation failed. Check the server terminal."
        }), 500


# ============================================================
# SECURE GENERATED-REPORT DOWNLOAD
# ============================================================

@app.route("/download/<filename>", methods=["GET"])
def download_generated_report(filename):
    # Only accept filenames generated as 32 hexadecimal
    # characters followed by .pptx. Never accept a path.
    import re

    if not re.fullmatch(r"[0-9a-f]{32}\.pptx", filename):
        return jsonify({
            "success": False,
            "message": "Invalid report filename."
        }), 400

    report_folder = os.path.abspath(
        app.config["REPORT_FOLDER"]
    )

    report_path = os.path.abspath(
        os.path.join(report_folder, filename)
    )

    if os.path.dirname(report_path) != report_folder:
        return jsonify({
            "success": False,
            "message": "Invalid report path."
        }), 400

    if not os.path.isfile(report_path):
        return jsonify({
            "success": False,
            "message": "The requested report was not found."
        }), 404

    return send_from_directory(
        report_folder,
        filename,
        as_attachment=True,
        download_name="AI_Resource_Intelligence_20_Slide_Report.pptx",
    )


# ============================================================
# AI / RAG SEARCH
# ============================================================

@app.route(
    "/api/search",
    methods=["POST"]
)
def ai_search():

    try:

        # ----------------------------------------------------
        # READ JSON
        # ----------------------------------------------------

        data = request.get_json(
            silent=True
        )


        # ----------------------------------------------------
        # CHECK REQUEST
        # ----------------------------------------------------

        if not data:

            return jsonify({

                "success": False,

                "message":
                    "No search request received."

            }), 400


        # ----------------------------------------------------
        # QUESTION
        # ----------------------------------------------------

        question = (
            data.get(
                "question",
                ""
            )
            .strip()
        )


        # ----------------------------------------------------
        # RESOURCE ID
        # ----------------------------------------------------

        resource_id = (
            data.get(
                "resource_id",
                ""
            )
            .strip()
        )


        # ----------------------------------------------------
        # DOCUMENT
        # ----------------------------------------------------

        document_data = data.get(
            "document",
            {}
        )


        # ----------------------------------------------------
        # VALIDATE QUESTION
        # ----------------------------------------------------

        if not question:

            return jsonify({

                "success": False,

                "message":
                    "Please enter a question."

            }), 400


        # ----------------------------------------------------
        # VALIDATE RESOURCE
        # ----------------------------------------------------

        if not resource_id:

            return jsonify({

                "success": False,

                "message":
                    "Please upload a document first."

            }), 400


        # ----------------------------------------------------
        # RESOURCE INTELLIGENCE AGENT
        # ----------------------------------------------------

        result = resource_agent(

            question,

            resource_id,

            document_data
        )


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "question":
                question,

            "answer":
                result.get(
                    "answer",
                    ""
                ),

            "sources":
                result.get(
                    "sources",
                    []
                ),

            "agent":
                "Resource Intelligence Agent",

            "rag": True

        })


    except Exception as error:

        print()
        print("=" * 70)
        print("RAG SEARCH ERROR")
        print("=" * 70)

        print(
            traceback.format_exc()
        )

        print("=" * 70)
        print()


        return jsonify({

            "success": False,

            "message":
                "AI search failed.",

            "error":
                str(error),

            "type":
                type(error).__name__

        }), 500


# ============================================================
# FILE TOO LARGE
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({

        "success": False,

        "message":
            "The uploaded file is too large. "
            "Maximum allowed size is 25 MB."

    }), 413


# ============================================================
# PAGE / API NOT FOUND
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "success": False,

        "message":
            "Requested endpoint was not found."

    }), 404


# ============================================================
# INTERNAL SERVER ERROR
# ============================================================

@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({

        "success": False,

        "message":
            "Internal server error.",

        "error":
            str(error)

    }), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("AI RESOURCE INTELLIGENCE PLATFORM")
    print("=" * 70)

    print(
        "Dashboard: "
        "http://127.0.0.1:5001"
    )

    print(
        "Health Check: "
        "http://127.0.0.1:5001/api/health"
    )

    print(
        "Upload API: "
        "http://127.0.0.1:5001/api/upload"
    )

    print(
        "RAG / AI Search: "
        "http://127.0.0.1:5001/api/search"
    )

    print("=" * 70)

    print(
        "RAG MODEL: "
        "all-MiniLM-L6-v2"
    )

    print(
        "AGENT: "
        "Resource Intelligence Agent"
    )

    print(
        "GENAI: "
        "Ready for LLM integration"
    )

    print("=" * 70)
    print()

    # IMPORTANT:
    # RAG model loading can take time.
    # Disable Flask's automatic reloader so
    # the model is not repeatedly re-imported.

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True,
        use_reloader=False
    )
