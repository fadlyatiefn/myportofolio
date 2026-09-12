from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Projects
from datetime import datetime

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            started_at=timezone.now(),
            category="part-time",
        )

        self.projects = Projects.objects.create(
            project_name="BertsLounge",
            project_desc="Membuat web berisi redirect link untuk suatu artist",
            project_start=datetime(2025, 2, 12, tzinfo=timezone.UTC),
            thumbnail="/static/img/bertslounge.png",
            project_link="https://bertslounge.vercel.app/",
        )
        

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_projects_model(self):
        self.assertEqual(str(self.projects), "BertsLounge")
        self.assertEqual(self.projects.project_desc, "Membuat web berisi redirect link untuk suatu artist")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_empty_projects_section(self):
            Projects.objects.all().delete()
            response = self.client.get(reverse("main:show_main"))
    
            self.assertContains(response, "Belum ada project yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_completed_projects(self):
            self.projects.project_end = timezone.now()
            self.projects.save()
            response = self.client.get(reverse("main:show_main"))
    
            self.assertFalse(self.projects.is_ongoing)
            self.assertContains(response, "Feb. 12, 2025, midnight")
            self.assertNotContains(response, "Sedang berlangsung")