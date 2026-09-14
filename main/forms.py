from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Projects

class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = [
            "project_name",
            "project_desc",
            "tech_stack",
            "project_link",
            "thumbnail",
        ]

        labels = {
            "project_name": "Nama Proyek",
            "project_desc": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_link": "URL Proyek",
            "thumbnail": "URL Gambar Proyek",
        }

        widgets = {
            "project_name": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "project_desc": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_link": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }