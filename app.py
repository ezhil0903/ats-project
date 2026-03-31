from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import re

from resume_parser import extract_text, extract_skills
from scorer import calculate_score

# =========================
# 🔥 CREATE FLASK APP
# =========================
app = Flask(__name__)
CORS(app)

# =========================
# 🔥 UPLOAD FOLDER
# =========================
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# 🔥 JOB ROLES (EXAMPLE)
# =========================
JOB_ROLES = {
    "python developer": {
        "python": 10,
        "django": 8,
        "sql": 7,
        "api": 6,
        "docker": 5
    },
    "frontend developer": {
        "html": 10,
        "css": 9,
        "javascript": 9,
        "react": 8
    },
    "data analyst": {
        "python": 9,
        "sql": 10,
        "excel": 8,
        "power bi": 7
    }
}

# =========================
# 🔥 HEALTH CHECK ROUTE
# =========================
@app.route("/")
def home():
    return jsonify({"message": "ATS Backend Running ✅"})

# =========================
# 🔥 UPLOAD ROUTE
# =========================
@app.route("/upload", methods=["POST"])
def upload_resume():
    try:
        # =========================
        # 🔥 ROLE INPUT
        # =========================
        role = request.form.get("role", "").lower().strip()

        if role not in JOB_ROLES:
            return jsonify({"error": "Invalid role selected"}), 400

        job_skills = JOB_ROLES[role].copy()

        # =========================
        # 🔥 JOB DESCRIPTION INPUT
        # =========================
        job_description = request.form.get("job_description", "").lower().strip()

        if job_description:
            jd_words = re.findall(r'\b[a-zA-Z]{4,}\b', job_description)

            for word in jd_words:
                job_skills[word] = job_skills.get(word, 5)

        # =========================
        # 🔥 FILE VALIDATION
        # =========================
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["resume"]

        if file.filename.strip() == "":
            return jsonify({"error": "Empty file"}), 400

        # =========================
        # 🔥 SAVE FILE
        # =========================
        filename = str(uuid.uuid4()) + "_" + file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        print("✅ File saved:", filename)

        # =========================
        # 🔥 EXTRACT TEXT
        # =========================
        text = extract_text(file_path)

        if not text or len(text.strip()) < 20:
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({"error": "Could not extract text"}), 400

        # =========================
        # 🔥 SKILLS EXTRACTION
        # =========================
        skills = extract_skills(text)

        # =========================
        # 🔥 SCORING
        # =========================
        result = calculate_score(text, job_skills)

        # =========================
        # 🔥 SUGGESTIONS
        # =========================
        suggestions = generate_suggestions(result.get("missing", []))

        # =========================
        # 🔥 CLEANUP
        # =========================
        if os.path.exists(file_path):
            os.remove(file_path)

        # =========================
        # 🔥 RESPONSE
        # =========================
        return jsonify({
            "role": role,
            "skills_found": skills,
            "ats_score": result.get("score", 0),
            "rule_score": result.get("rule_score", 0),
            "ai_score": result.get("ai_score", 0),
            "matched_skills": result.get("matched", []),
            "missing_skills": result.get("missing", []),
            "suggestions": suggestions
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": "Internal server error"}), 500


# =========================
# 🔥 SUGGESTIONS FUNCTION
# =========================
def generate_suggestions(missing_skills):
    return [
        f"Add projects or experience related to '{skill}'"
        for skill in missing_skills
    ]


# =========================
# 🔥 RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)