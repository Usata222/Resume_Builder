from django.contrib import admin
from .models import Resume, Education, WorkExperience, Project, Extracurricular

admin.site.register(Resume)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(Project)
admin.site.register(Extracurricular)
