from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from main.models import Experience, Projects

full_name = "Fadly Atief Nauval"
name = "Fadly"
npm = "2506624940"
study_program = "S1 Information System"
def show_main(request):
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
        "projects": Projects.objects.all(),
        "skills_bio": "Welcome to my digital playground! Here’s what I use to code, design, and build cool stuff.",
        "projects_bio": "Here are all my projects i've made untill now!",
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": name,
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


