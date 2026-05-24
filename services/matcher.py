import re

def clean_skills(text):

    text = text.lower()

    text = text.replace("\n", " ")

    skills = re.split(r"[,\s]+", text)

    cleaned = []

    for skill in skills:

        skill = skill.strip()

        if skill != "":

            cleaned.append(skill)

    return list(set(cleaned))


def calculate_match(candidate_skills, job_description):

    candidate_skill_list = clean_skills(candidate_skills)

    jd_skill_list = clean_skills(job_description)

    matched_skills = []

    missing_skills = []

    for skill in jd_skill_list:

        if skill in candidate_skill_list:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    if len(jd_skill_list) == 0:

        match_score = 0

    else:

        match_score = int(
            (len(matched_skills) / len(jd_skill_list)) * 100
        )

    return (
        match_score,
        ", ".join(missing_skills)
    )