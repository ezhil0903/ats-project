import pdfplumber

# 🔥 MASTER SKILL DICTIONARY (WITH VARIATIONS)
SKILL_MAP = {
    "python": ["python"],
    "sql": ["sql", "mysql", "postgres", "postgresql"],
    "django": ["django"],
    "react": ["react", "reactjs"],
    "machine learning": ["machine learning", "ml"],
    "javascript": ["javascript", "js"],
    "html": ["html"],
    "css": ["css"],
    "docker": ["docker"],
    "api": ["api", "rest api", "restful"],
    "testing": ["testing", "test cases", "qa"],
    "selenium": ["selenium"],
    "excel": ["excel"],
    "communication": ["communication", "verbal", "spoken"]
}


# ✅ EXTRACT TEXT FROM PDF
def extract_text(file_path):
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + " "
    except Exception as e:
        print("PDF ERROR:", e)

    return text.lower()


# ✅ SMART SKILL EXTRACTION
def extract_skills(text):
    found_skills = []

    for skill, variations in SKILL_MAP.items():
        for variant in variations:
            if variant in text:
                found_skills.append(skill)
                break  # avoid duplicates

    return found_skills