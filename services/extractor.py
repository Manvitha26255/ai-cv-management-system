import re

def extract_candidate_details(text):

    lines = text.split("\n")

    name = lines[0].strip()

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    phone_pattern = r"(\+91[-\s]?)?[6-9]\d{9}"

    email_match = re.search(email_pattern, text)

    phone_match = re.search(phone_pattern, text)

    email = email_match.group() if email_match else "Not Found"

    phone = phone_match.group() if phone_match else "Not Found"

    skill_keywords = [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "React",
        "Flask",
        "Django",
        "HTML",
        "CSS",
        "SQL",
        "MySQL",
        "MongoDB",
        "Git",
        "GitHub",
        "AWS",
        "Docker",
        "Machine Learning",
        "AI"
    ]

    found_skills = []

    for skill in skill_keywords:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    skills = ", ".join(found_skills)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills
    }