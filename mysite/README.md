# Resume Builder

## What changed in this update
- **Ready for GitHub**: the secret key and other config now live in a local
  `.env` file (never committed) instead of being hardcoded in `settings.py`.
  A `.gitignore` keeps `.env`, `db.sqlite3`, virtual envs, and cache files out
  of version control. See **Setup** below.
- **Example placeholders are now generic and ATS-friendly** — the builder no
  longer shows anyone's real personal history as example text. Every example
  uses the XYZ format ("Accomplished [X], as measured by [Y], by doing [Z]")
  with strong action verbs and measurable results, so it's genuinely useful
  guidance for someone who's never written a resume bullet before.
- **Fully responsive** — the nav bar, forms, and dashboard now adapt cleanly
  from small phones up through desktop (wrapping nav items, full-width
  buttons on mobile, single-column forms below the `sm` breakpoint, etc).

## What the app does (recap)
- The PDF output follows a clean, standard resume layout: bold section
  headers (EDUCATION, WORK EXPERIENCE, PERSONAL PROJECTS, EXTRACURRICULAR
  ACTIVITIES, SKILLS), a horizontal rule under each header, name centered at
  the top, contact line with clickable **LinkedIn**, **Gmail**, **GitHub**
  links, and title-on-the-left/date-on-the-right rows.
- Work Experience, Personal Projects, and Extracurricular Activities each
  have a **+ Add** button — no fixed limit on entries.
- **Guest mode**: anyone can fill in the builder and download the PDF
  immediately — nothing is saved, no account required.
- **Accounts**: sign up to have resumes saved to a **My Resumes** dashboard,
  where you can edit, re-download, or delete them. Each account only ever
  sees its own resumes, enforced at the database query level
  (`Resume.objects.filter(owner=request.user)`), not just hidden in the UI.

## Setup
```bash
python3 -m venv env
source env/bin/activate          # env\Scripts\Activate.ps1 on Windows (PowerShell)
pip install -r requirements.txt

cp .env.example .env             # then open .env and set a real SECRET_KEY
python manage.py migrate
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

### Generating a SECRET_KEY for your `.env`
```bash
python -c "import secrets,string; c=string.ascii_letters+string.digits+'!@#$%^&*(-_=+)'; print(''.join(secrets.choice(c) for _ in range(50)))"
```
Paste the output as `SECRET_KEY=...` in `.env`.

## Pushing this to GitHub
`.env` and `db.sqlite3` are already in `.gitignore`, so a normal `git init`,
`git add .`, `git commit`, `git push` will not leak your secret key or local
database. Double-check with `git status` before your first commit that
`.env` isn't showing up as a tracked file.

## Key files if you want to keep customizing
- `mysite/settings.py` — reads `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` from `.env`
- `myapp/models.py` — Resume, Education, WorkExperience, Project, Extracurricular
- `myapp/views.py` — `submit_resume` handles both the guest (no-save) and
  logged-in (save) paths; `_render_pdf` + `myapp/templates/myapp/resume_pdf.html`
  is where the PDF layout lives
- `myapp/templates/myapp/builder.html` — the form, with the `<template>` tags
  and small JS at the bottom powering the "+ Add" buttons
- `myapp/templates/myapp/resume_pdf.html` — edit this to tweak the exact
  resume layout/format

