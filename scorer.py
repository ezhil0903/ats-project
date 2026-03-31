def smart_match(text, skill):
    skill_words = skill.lower().split()
    return any(word in text for word in skill_words)


def calculate_score(text, job_skills):
    total_weight = sum(job_skills.values())
    score = 0

    matched = []
    missing = []

    for skill, weight in job_skills.items():
        if smart_match(text, skill):
            score += weight * 10
            matched.append(skill)
        else:
            missing.append(skill)

    ats_score = (score / (total_weight * 10)) * 100 if total_weight else 0

    return {
        "score": round(ats_score, 2),
        "matched": matched,
        "missing": missing
    }