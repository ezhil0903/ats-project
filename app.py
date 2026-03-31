from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from resume_parser import extract_text, extract_skills
from scorer import calculate_score

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🔥 ROLE-BASED JOB SKILLS (LOWERCASE ONLY)
JOB_ROLES = {

    "python developer": {
        "python":10, "django":9, "flask":8, "fastapi":8,
        "sql":9, "rest api":9, "pandas":7, "numpy":7,
        "git":7, "docker":6
    },

    "java developer": {
        "java":10, "spring":9, "spring boot":9, "hibernate":8,
        "sql":9, "microservices":8, "rest api":8,
        "maven":7, "git":7, "docker":6
    },

    "software tester": {
        "manual testing":10, "automation testing":9, "selenium":9,
        "test cases":9, "bug tracking":9, "jira":8,
        "api testing":8, "postman":8, "regression testing":8,
        "test automation":9
    },

    "data analyst": {
        "excel":10, "sql":9, "python":8, "power bi":9,
        "tableau":9, "data visualization":9, "statistics":8,
        "data cleaning":8, "reporting":8, "dashboard":9
    },

    "data science": {
        "python":10, "machine learning":10, "deep learning":9,
        "pandas":9, "numpy":9, "scikit learn":9,
        "data modeling":8, "statistics":9, "nlp":8,
        "tensorflow":8
    },

    "mern stack developer": {
        "mongodb":10, "express":9, "react":10, "node":10,
        "javascript":10, "rest api":9, "redux":8,
        "html":8, "css":8, "git":7
    },

    "cloud engineer": {
        "aws":10, "azure":9, "gcp":9, "docker":9,
        "kubernetes":9, "linux":9, "networking":8,
        "ci cd":8, "terraform":8, "cloud security":8
    },

    "cyber security engineer": {
        "network security":10, "penetration testing":9,
        "ethical hacking":9, "firewalls":9,
        "vulnerability assessment":9, "security tools":8,
        "siem":8, "incident response":8,
        "risk management":8, "encryption":8
    },

    "frontend developer": {
        "html":10, "css":10, "javascript":10,
        "react":9, "tailwind":9, "responsive design":9,
        "bootstrap":8, "redux":8, "ui ux":8, "git":7
    },

    "backend developer": {
        "api":10, "database":9, "sql":9,
        "node":8, "python":8, "java":8,
        "microservices":8, "authentication":8,
        "rest api":9, "docker":7
    },

    "product engineer": {
        "problem solving":10, "data structures":10,
        "algorithms":10, "system design":9,
        "coding":9, "optimization":8,
        "debugging":8, "scalability":8,
        "performance tuning":8, "design patterns":8
    },

    "senior full stack developer": {
        "system design":10, "microservices":9,
        "api":9, "database":9, "cloud":9,
        "scalability":9, "docker":8,
        "kubernetes":8, "ci cd":8, "architecture":10
    },

    "hr": {
        "recruitment":10, "communication":10,
        "interviewing":9, "onboarding":9,
        "employee engagement":8, "hr policies":8,
        "talent acquisition":9, "training":8,
        "performance management":8, "conflict resolution":8
    },

    "bpo": {
        "communication":10, "customer service":10,
        "problem solving":9, "voice support":9,
        "client handling":9, "time management":8,
        "call handling":9, "crm":8,
        "teamwork":8, "adaptability":8
    },

    "voice process": {
        "communication":10, "voice support":10,
        "customer handling":9, "call center":9,
        "problem solving":8, "crm":8,
        "listening skills":9, "fluency":9,
        "teamwork":8, "time management":8
    },

    "non voice": {
        "typing":10, "email support":10,
        "chat support":10, "documentation":9,
        "data entry":9, "crm":8,
        "attention to detail":9,
        "problem solving":8,
        "time management":8, "accuracy":9
    }
}


# ✅ HOME ROUTE
@app.route("/")
def home():
    return "ATS Backend Running ✅"


# ✅ UPLOAD ROUTE
@app.route("/upload", methods=["POST"])
def upload_resume():
    try:
        # 🔥 ROLE INPUT
        role = request.form.get("role", "").lower()

        if role not in JOB_ROLES:
            return jsonify({"error": "Invalid role selected"}), 400

        job_skills = JOB_ROLES[role]

        # 🔥 FILE VALIDATION
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["resume"]

        if file.filename == "":
            return jsonify({"error": "Empty file"}), 400

        # 🔥 SAVE FILE
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        print("File saved:", file.filename)

        # 🔥 EXTRACT TEXT
        text = extract_text(file_path)

        # 🔥 OPTIONAL (for display only)
        skills = extract_skills(text)

        # 🔥 CORRECT SCORING (PASS TEXT)
        result = calculate_score(text, job_skills)

        # 🔥 SUGGESTIONS
        suggestions = generate_suggestions(result["missing"])

        return jsonify({
            "role": role,
            "skills_found": skills,
            "ats_score": result["score"],
            "matched_skills": result["matched"],
            "missing_skills": result["missing"],
            "suggestions": suggestions
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# 🔥 Suggestions
def generate_suggestions(missing_skills):
    return [
        f"Add experience or projects related to '{skill}'"
        for skill in missing_skills
    ]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)