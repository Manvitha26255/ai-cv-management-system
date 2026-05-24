def generate_summary(skills, match_score):

    skill_list = skills.split(",")

    top_skills = ", ".join(skill_list[:3])

    if match_score >= 80:

        level = "Excellent"

    elif match_score >= 60:

        level = "Strong"

    elif match_score >= 40:

        level = "Average"

    else:

        level = "Beginner"

    summary = f"""

    {level} candidate with skills in
    {top_skills}.

    Suitable for software development
    and technical roles.

    """

    return summary