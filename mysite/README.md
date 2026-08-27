# Resume Builder

Build a professional, ATS-friendly resume in your browser and export it straight to PDF — no account required to use it, but sign up if you want your resumes saved.

## Demo

<!-- Add a link to your live demo here, e.g.: -->
<!-- 🔗 Live demo: https://your-app-name.onrender.com -->

<!-- Add a screenshot or short screen recording here, e.g.: -->
<!-- ![Resume Builder screenshot](./screenshots/builder.png) -->
<!-- ![Sample PDF output](./screenshots/sample-resume.png) -->

> Drop your screenshots/GIFs in a `screenshots/` folder in the project root and update the paths above once you have them.

## Features

- **Guest mode** — build and download a resume as a PDF instantly, with no account and nothing saved on the server.
- **User registration and login** — create an account to save resumes and come back to edit them later.
- **Per-user dashboard** — each account only ever sees and can access its own saved resumes; other users' resumes are not visible or reachable, even by guessing a URL.
- **Dynamic, repeatable sections** — add as many entries as you need for Work Experience, Personal Projects, and Extracurricular Activities via "+ Add" buttons — no fixed limit.
- **Built-in resume-writing guidance** — placeholder text in every bullet-point field demonstrates the XYZ format ("Accomplished [X], as measured by [Y], by doing [Z]") so the output reads like a strong, quantified resume even for a first-time user.
- **Clean, ATS-friendly PDF export** — bold section headers, horizontal rules, clickable LinkedIn/Gmail/GitHub links, and consistent left/right-aligned dates — generated server-side from HTML/CSS.
- **Edit and re-download** — saved resumes can be edited (pre-filling the form with existing data) and re-exported at any time.
- **Fully responsive UI** — usable on mobile, tablet, and desktop.

## Technologies Used

- **Backend:** Python, Django
- **Database:** SQLite (default, via Django ORM — swappable for PostgreSQL/MySQL with no code changes, just a settings update)
- **Frontend:** Django templates, HTML, Tailwind CSS (via CDN), vanilla JavaScript (for the dynamic "+ Add" form sections)
- **PDF generation:** [xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf) (renders an HTML/CSS template into a PDF)
- **Auth:** Django's built-in authentication system (`django.contrib.auth`)
- **Config/secrets:** [python-dotenv](https://github.com/theskumar/python-dotenv) (`.env` file, not committed to Git)

## Installation and Setup

These steps assume you have Python 3.10+ and `pip` installed.

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv env
   source env/bin/activate        # On Windows (PowerShell): env\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Copy the example file and fill in real values (see [Environment Variables](#environment-variables) below):
   ```bash
   cp .env.example .env
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **(Optional) Create an admin account**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. Open **http://127.0.0.1:8000/** in your browser.

## Environment Variables

This project keeps secrets out of the codebase using a `.env` file, which is listed in `.gitignore` and should **never** be committed. Copy `.env.example` to `.env` and set the following:

| Variable        | Required | Description                                                                 |
|-----------------|----------|-------------------------------------------------------------------------------|
| `SECRET_KEY`    | Yes      | Django's cryptographic signing key. Generate your own — never reuse the example value. |
| `DEBUG`         | Yes      | `True` for local development, `False` in production.                        |
| `ALLOWED_HOSTS` | Yes      | Comma-separated list of hosts allowed to serve the app (e.g. `127.0.0.1,localhost` locally, your real domain in production). |

Generate a secret key with:
```bash
python -c "import secrets,string; c=string.ascii_letters+string.digits+'!@#$%^&*(-_=+)'; print(''.join(secrets.choice(c) for _ in range(50)))"
```

No external API keys or third-party credentials are required to run this project locally — everything (auth, storage, PDF generation) runs with the packages in `requirements.txt` and the local SQLite database.

## How to Use It

1. **As a guest:** Go to the home page, fill in your details (contact info, education, work experience, projects, extracurriculars, skills), and click **Build & Download PDF**. Your resume downloads immediately — nothing is saved.
2. **To save your resumes:** Click **Sign up** in the top navigation and create an account (username + password, 8 characters minimum).
3. **Once logged in:** Fill in the same builder form and click **Save Resume** — it's added to your account instead of downloading right away.
4. **My Resumes dashboard:** After signing in, click **My Resumes** to see everything you've saved. From there you can:
   - **Edit** — reopens the builder pre-filled with that resume's data.
   - **Download PDF** — re-exports the current saved version.
   - **Delete** — permanently removes it from your account.
5. **Log out** any time from the top navigation — your saved resumes will still be there next time you log back in.

## Project Structure

```
mysite/
├── manage.py
├── requirements.txt
├── .env.example
├── mysite/            # Project-level settings, URLs, WSGI/ASGI entry points
└── myapp/              # The resume builder app
    ├── models.py       # Resume, Education, WorkExperience, Project, Extracurricular
    ├── views.py        # Auth, builder, save/download/delete logic
    ├── urls.py
    ├── templates/
    │   └── myapp/
    │       ├── base.html
    │       ├── builder.html
    │       ├── dashboard.html
    │       └── resume_pdf.html   # The PDF layout template
    └── templates/registration/
        ├── login.html
        └── signup.html
```

## Possible Future Improvements

- Multiple resume templates/themes to choose from
- Drag-and-drop reordering of bullet points and sections
- Export to Word (.docx) in addition to PDF
- Shareable public link for a saved resume
