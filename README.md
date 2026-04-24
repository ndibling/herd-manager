# Herd Manager

A lightweight, friendly **livestock management** app for tracking animals, health (shots/medicine), pedigree (4 generations), documents (e.g., Mini Zebu of America), and photos (used as the icon).

## Features
- Species: cow, goat, sheep, horse, swine, chicken, rabbit
- Units: **lbs**, **inches**
- Photo upload (used as icon)
- Treatments (shots & medicines)
- 4-generation pedigree
- Registration orgs + document upload

---

## Run it now (local)

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
