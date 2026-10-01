import datetime
from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from main.models import Experience, Projects
from main.forms import ProjectForm, ExperienceForm

full_name = "Fadly Atief Nauval"
name = "Fadly"
npm = "2506624940"
study_program = "S1 Information System"
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "full_name": full_name,
        "name": name,
        "npm": npm,
        "study_program": study_program,
        "bio": (
            "I am a second-year Information Systems student at Universitas Indonesia who is enthusiastic about the dynamic intersection of technology, design, and business. I believe that truly great products are born from a perfect harmony of solid backend systems, engaging visuals, and strong business value. I am actively translating this passion into various digital design and development projects to build my expertise."
        ),
        "skills_1": ["Python", "Equipped with a solid foundation in programming principles, utilizing Python for scripting and logical problem-solving.", "/static/img/python.png"],
        "skills_2": ["Java", "Familiar with Object-Oriented Programming (OOP) concepts, writing structured code, and implementing basic unit tests.", "/static/img/java.png"],
        "skills_3": ["UI/UX", "Experienced in translating ideas into interactive prototypes using Figma and applying design thinking frameworks.", "/static/img/figma.png"],
        "skills_bio": "Welcome to my digital playground! Here’s what I use to code, design, and build cool stuff.",
        "projects_bio": "Here are all my projects i've made untill now!",
        "top3_projects": Projects.objects.all().order_by('-uploaded_date')[:3],
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    is_editor = request.user.groups.filter(name='Editor').exists()
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": name,
        "title_query": title_query,
        "is_editor": is_editor,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

def show_projects(request):
    title_query = request.GET.get("project_name", "").strip()
    
    context = {
        "name": name,
        "projects_bio": "Here are all my projects i've made untill now!",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": name,
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("project_name", "").strip()
    projects = Projects.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(project_name__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "project_name": project.project_name,
                "project_desc": project.project_desc,
                "tech_stack": project.tech_stack,
                "uploaded_date": project.uploaded_date,
                "thumbnail": project.thumbnail,
                "project_link": project.project_link,
                "star_count": len(starred_users),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Projects, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": name,
        "form": form,
    }
    return render(request, "experiences_form.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related("starred_by")

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for exp in experiences:
        starred_users = list(exp.starred_by.all())  # pakai cache prefetch, tanpa query tambahan
        is_starred = (
            request.user in starred_users if request.user.is_authenticated else False
        )

        data.append({
            "pk": str(exp.id),
            "fields": {
                "title": exp.title,
                "description": exp.description,
                "category": exp.category,
                "category_display": exp.get_category_display(),
                "thumbnail": exp.thumbnail or "",
                "started_at": exp.started_at.isoformat(),
                "ended_at": exp.ended_at.isoformat() if exp.ended_at else None,
                "is_ongoing": exp.is_ongoing,
                "star_count": len(starred_users),
                "is_starred": is_starred,
                "starred_by_names": ", ".join(u.username for u in starred_users),
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    is_editor = request.user.groups.filter(name='Editor').exists()
    if not request.user.is_superuser and not is_editor:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diupdate!")
        return redirect("main:show_experience")

    context = {
        "name": name,
        "form": form,
        "experience": experience,
        "is_editor": is_editor,
    }
    return render(request, "experiences_form.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": name,
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": name,
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Projects, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def toggle_star_exp(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

from django.views.decorators.http import require_POST

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan experience."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)