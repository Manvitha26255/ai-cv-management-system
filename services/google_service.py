import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open("AI CV Candidates").sheet1

def save_to_google_sheet(candidate):

    existing_data = sheet.get_all_values()

    if len(existing_data) == 0:

        sheet.append_row([
            "Name",
            "Email",
            "Phone",
            "Skills",
            "Match Score",
            "Missing Skills"
        ])

    rows = sheet.get_all_records()

    for index, row in enumerate(rows, start=2):

        if row["Email"] == candidate.email:

            sheet.update(
                f"A{index}:F{index}",
                [[
                    candidate.name,
                    candidate.email,
                    candidate.phone,
                    candidate.skills,
                    f"{candidate.match_score}%",
                    candidate.missing_skills
                ]]
            )

            return

    sheet.append_row([
        candidate.name,
        candidate.email,
        candidate.phone,
        candidate.skills,
        f"{candidate.match_score}%",
        candidate.missing_skills
    ])