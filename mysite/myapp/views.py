import io
import json

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Resume, Education, WorkExperience, Project, Extracurricular


# ---------- Auth ----------

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Account created. Your resumes will now be saved here.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('builder')


# ---------- Dashboard (only the logged-in user's own resumes) ----------

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(owner=request.user).order_by('-updated_at')
    return render(request, 'myapp/dashboard.html', {'resumes': resumes})


# ---------- Builder form ----------

def builder(request, resume_id=None):
    """Shows the blank builder for guests, or a pre-filled builder when
    editing one of the logged-in user's own saved resumes."""
    context = {'resume': None}
    if resume_id:
        if not request.user.is_authenticated:
            return redirect('login')
        resume = get_object_or_404(Resume, id=resume_id, owner=request.user)
        context = {
            'resume': resume,
            'education_json': json.dumps([
                {'school': e.school, 'degree': e.degree, 'location': e.location,
                 'dates': e.dates, 'coursework': e.coursework} for e in resume.education_set.all()]),
            'work_json': json.dumps([
                {'role': w.role, 'company': w.company, 'location': w.location,
                 'dates': w.dates, 'bullets_text': w.bullets} for w in resume.work_set.all()]),
            'projects_json': json.dumps([
                {'title': p.title, 'bullets_text': p.bullets} for p in resume.project_set.all()]),
            'extra_json': json.dumps([
                {'role': x.role, 'organization': x.organization, 'dates': x.dates,
                 'bullets_text': x.bullets} for x in resume.extracurricular_set.all()]),
        }
    return render(request, 'myapp/builder.html', context)


def _parse_form(request):
    """Pulls the dynamic (repeatable) sections out of request.POST into a
    plain dict structure shared by the guest PDF path and the DB-save path."""
    data = {
        'full_name': request.POST.get('full_name', '').strip(),
        'city': request.POST.get('city', '').strip(),
        'state': request.POST.get('state', '').strip(),
        'phone': request.POST.get('phone', '').strip(),
        'linkedin_url': request.POST.get('linkedin_url', '').strip(),
        'email': request.POST.get('email', '').strip(),
        'github_url': request.POST.get('github_url', '').strip(),
        'skills_technical': request.POST.get('skills_technical', '').strip(),
        'skills_soft': request.POST.get('skills_soft', '').strip(),
        'title': request.POST.get('title', 'My Resume').strip() or 'My Resume',
    }

    education = []
    schools = request.POST.getlist('edu_school')
    degrees = request.POST.getlist('edu_degree')
    edu_locations = request.POST.getlist('edu_location')
    edu_dates = request.POST.getlist('edu_dates')
    courseworks = request.POST.getlist('edu_coursework')
    for i in range(len(schools)):
        if not schools[i].strip():
            continue
        education.append({
            'school': schools[i].strip(),
            'degree': degrees[i].strip() if i < len(degrees) else '',
            'location': edu_locations[i].strip() if i < len(edu_locations) else '',
            'dates': edu_dates[i].strip() if i < len(edu_dates) else '',
            'coursework': courseworks[i].strip() if i < len(courseworks) else '',
        })
    data['education'] = education

    work = []
    roles = request.POST.getlist('work_role')
    companies = request.POST.getlist('work_company')
    work_locations = request.POST.getlist('work_location')
    work_dates = request.POST.getlist('work_dates')
    work_bullets = request.POST.getlist('work_bullets')
    for i in range(len(roles)):
        if not roles[i].strip():
            continue
        bullets = work_bullets[i] if i < len(work_bullets) else ''
        work.append({
            'role': roles[i].strip(),
            'company': companies[i].strip() if i < len(companies) else '',
            'location': work_locations[i].strip() if i < len(work_locations) else '',
            'dates': work_dates[i].strip() if i < len(work_dates) else '',
            'bullets': [b.strip() for b in bullets.splitlines() if b.strip()],
        })
    data['work'] = work

    projects = []
    proj_titles = request.POST.getlist('proj_title')
    proj_bullets = request.POST.getlist('proj_bullets')
    for i in range(len(proj_titles)):
        if not proj_titles[i].strip():
            continue
        bullets = proj_bullets[i] if i < len(proj_bullets) else ''
        projects.append({
            'title': proj_titles[i].strip(),
            'bullets': [b.strip() for b in bullets.splitlines() if b.strip()],
        })
    data['projects'] = projects

    extra = []
    extra_roles = request.POST.getlist('extra_role')
    extra_orgs = request.POST.getlist('extra_org')
    extra_dates = request.POST.getlist('extra_dates')
    extra_bullets = request.POST.getlist('extra_bullets')
    for i in range(len(extra_roles)):
        if not extra_roles[i].strip():
            continue
        bullets = extra_bullets[i] if i < len(extra_bullets) else ''
        extra.append({
            'role': extra_roles[i].strip(),
            'organization': extra_orgs[i].strip() if i < len(extra_orgs) else '',
            'dates': extra_dates[i].strip() if i < len(extra_dates) else '',
            'bullets': [b.strip() for b in bullets.splitlines() if b.strip()],
        })
    data['extracurricular'] = extra

    return data


def _render_pdf(data, filename):
    template = get_template('myapp/resume_pdf.html')
    html = template.render({'r': data})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('UTF-8')), dest=response, encoding='UTF-8')
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response


def submit_resume(request, resume_id=None):
    """Handles the builder form submit.
    - Not logged in: generate the PDF straight away, nothing is saved.
    - Logged in: save (or update) the resume to the account, then redirect
      to the dashboard where it shows up under that user only.
    """
    if request.method != 'POST':
        return redirect('builder')

    data = _parse_form(request)

    if not request.user.is_authenticated:
        filename = f"{(data['full_name'] or 'resume').replace(' ', '_')}_CV.pdf"
        return _render_pdf(data, filename)

    # Logged in -> persist to this user's account only.
    if resume_id:
        resume = get_object_or_404(Resume, id=resume_id, owner=request.user)
        resume.education_set.all().delete()
        resume.work_set.all().delete()
        resume.project_set.all().delete()
        resume.extracurricular_set.all().delete()
    else:
        resume = Resume(owner=request.user)

    resume.title = data['title']
    resume.full_name = data['full_name']
    resume.city = data['city']
    resume.state = data['state']
    resume.phone = data['phone']
    resume.linkedin_url = data['linkedin_url']
    resume.email = data['email']
    resume.github_url = data['github_url']
    resume.skills_technical = data['skills_technical']
    resume.skills_soft = data['skills_soft']
    resume.save()

    for i, e in enumerate(data['education']):
        Education.objects.create(resume=resume, order=i, **e)
    for i, w in enumerate(data['work']):
        WorkExperience.objects.create(
            resume=resume, order=i, role=w['role'], company=w['company'],
            location=w['location'], dates=w['dates'], bullets='\n'.join(w['bullets']))
    for i, p in enumerate(data['projects']):
        Project.objects.create(
            resume=resume, order=i, title=p['title'], bullets='\n'.join(p['bullets']))
    for i, x in enumerate(data['extracurricular']):
        Extracurricular.objects.create(
            resume=resume, order=i, role=x['role'], organization=x['organization'],
            dates=x['dates'], bullets='\n'.join(x['bullets']))

    messages.success(request, 'Resume saved to your account.')
    return redirect('dashboard')


def _resume_to_dict(resume):
    return {
        'full_name': resume.full_name,
        'city': resume.city,
        'state': resume.state,
        'phone': resume.phone,
        'linkedin_url': resume.linkedin_url,
        'email': resume.email,
        'github_url': resume.github_url,
        'skills_technical': resume.skills_technical,
        'skills_soft': resume.skills_soft,
        'education': [{'school': e.school, 'degree': e.degree, 'location': e.location,
                       'dates': e.dates, 'coursework': e.coursework} for e in resume.education_set.all()],
        'work': [{'role': w.role, 'company': w.company, 'location': w.location,
                  'dates': w.dates, 'bullets': w.bullet_list()} for w in resume.work_set.all()],
        'projects': [{'title': p.title, 'bullets': p.bullet_list()} for p in resume.project_set.all()],
        'extracurricular': [{'role': x.role, 'organization': x.organization, 'dates': x.dates,
                              'bullets': x.bullet_list()} for x in resume.extracurricular_set.all()],
    }


@login_required
def download_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, owner=request.user)
    data = _resume_to_dict(resume)
    filename = f"{(resume.full_name or 'resume').replace(' ', '_')}_CV.pdf"
    return _render_pdf(data, filename)


@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, owner=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted.')
    return redirect('dashboard')
