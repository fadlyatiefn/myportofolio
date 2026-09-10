from django.contrib import admin

# Register your models here.
from .models import Experience, Projects

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'started_at', 'ended_at', 'is_ongoing']
    list_filter = ['category']
    search_fields = ['title', 'description']

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'project_start', 'project_end', 'is_ongoing', 'have_project_link']
    search_fields = ['project_name', 'project_desc']