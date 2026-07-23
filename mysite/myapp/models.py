from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    """Top-level resume/CV. Owned by a user once saved; guest resumes are
    never written here (they're built and downloaded on the fly, not persisted)."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100, default='My Resume', blank=True)

    full_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    linkedin_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)

    skills_technical = models.CharField(max_length=300, blank=True)
    skills_soft = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.title}"


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education_set')
    school = models.CharField(max_length=150)
    degree = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=100, blank=True)
    dates = models.CharField(max_length=100, blank=True)
    coursework = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work_set')
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=100, blank=True)
    dates = models.CharField(max_length=100, blank=True)
    bullets = models.TextField(blank=True, help_text='One bullet per line')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def bullet_list(self):
        return [b.strip() for b in self.bullets.splitlines() if b.strip()]


class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='project_set')
    title = models.CharField(max_length=150)
    bullets = models.TextField(blank=True, help_text='One bullet per line')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def bullet_list(self):
        return [b.strip() for b in self.bullets.splitlines() if b.strip()]


class Extracurricular(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='extracurricular_set')
    role = models.CharField(max_length=150)
    organization = models.CharField(max_length=150, blank=True)
    dates = models.CharField(max_length=100, blank=True)
    bullets = models.TextField(blank=True, help_text='One bullet per line')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def bullet_list(self):
        return [b.strip() for b in self.bullets.splitlines() if b.strip()]
