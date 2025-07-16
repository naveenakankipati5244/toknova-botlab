import tempfile, os
from pyresparser import ResumeParser

def parse_resume(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    try:
        data = ResumeParser(tmp_path).get_extracted_data()
    except Exception as e:
        os.remove(tmp_path)
        return {
            "error": f"Resume parsing failed: {str(e)}",
            "full_text": "",
            "name": "",
            "skills": [],
            "experience": ""
        }

    os.remove(tmp_path)

    if not data:
        return {
            "error": "Resume parsing returned no data.",
            "full_text": "",
            "name": "",
            "skills": [],
            "experience": ""
        }

    # Fallbacks and safety checks
    name = data.get("name", "")
    skills = data.get("skills", [])
    experience = data.get("experience", "") or data.get("total_experience", "")

    if not isinstance(name, str):
        name = ""
    if not isinstance(skills, list):
        skills = []
    if not isinstance(experience, str):
        experience = ""

    # Debug print (optional)
    print("DEBUG - Parsed Fields:")
    print("Name:", name)
    print("Skills:", skills)
    print("Experience:", experience)

    # Safe full_text
    full_text = " ".join([
        name,
        " ".join(skills),
        experience
    ])

    data["full_text"] = full_text
    data["error"] = ""

    return data
