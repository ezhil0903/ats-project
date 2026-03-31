import uuid

@app.route("/upload", methods=["POST"])
def upload_resume():
    try:
        # 🔥 ROLE INPUT
        role = request.form.get("role", "").lower()

        if role not in JOB_ROLES:
            return jsonify({"error": "Invalid role selected"}), 400

        # 🔥 COPY ROLE SKILLS (important)
        job_skills = JOB_ROLES[role].copy()

        # 🔥 NEW: JOB DESCRIPTION INPUT
        job_description = request.form.get("job_description", "").lower()

        # 🔥 ADD JD KEYWORDS TO SKILLS
        if job_description:
            jd_words = job_description.split()

            for word in jd_words:
                if len(word) > 3:  # ignore small words
                    job_skills[word] = job_skills.get(word, 5)

        # 🔥 FILE VALIDATION
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["resume"]

        if file.filename == "":
            return jsonify({"error": "Empty file"}), 400

        # 🔥 SAFE FILE NAME (NO OVERWRITE)
        filename = str(uuid.uuid4()) + "_" + file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        print("✅ File saved:", filename)

        # 🔥 EXTRACT TEXT
        text = extract_text(file_path)

        if not text:
            return jsonify({"error": "Could not extract text"}), 400

        # 🔥 SKILLS EXTRACTION
        skills = extract_skills(text)

        # 🔥 SCORING (HYBRID AI)
        result = calculate_score(text, job_skills)

        # 🔥 SUGGESTIONS SAFE ACCESS
        suggestions = generate_suggestions(result.get("missing", []))

        # 🔥 DELETE FILE AFTER USE
        os.remove(file_path)

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