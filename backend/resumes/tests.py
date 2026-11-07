from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .ats import calculate_ats_score, extract_keywords
from .models import Experience, Resume, Skill

User = get_user_model()


class ResumeAPITests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="Strong-Test-Password!42",
            email="owner@example.com",
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="Strong-Test-Password!42",
            email="other@example.com",
        )
        self.resume = Resume.objects.create(
            user=self.owner,
            full_name="Amina Engineer",
            job_title="Software Engineer",
            bio="Backend and frontend developer",
            is_public=True,
        )
        self.client = APIClient()

    def test_resume_list_requires_authentication(self):
        response = self.client.get(reverse("resume-list"))
        self.assertEqual(response.status_code, 401)

    def test_owner_can_create_update_and_delete_resume(self):
        self.client.force_authenticate(user=self.owner)

        create_response = self.client.post(
            reverse("resume-list"),
            {"full_name": "New Resume", "title": "Engineering CV"},
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        new_id = create_response.data["id"]
        self.assertEqual(Resume.objects.get(pk=new_id).user, self.owner)

        detail_url = reverse("resume-detail", args=[new_id])
        update_response = self.client.patch(
            detail_url,
            {"job_title": "Python Engineer"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["job_title"], "Python Engineer")

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Resume.objects.filter(pk=new_id).exists())

    def test_other_user_cannot_access_owner_resume(self):
        self.client.force_authenticate(user=self.other_user)
        detail_url = reverse("resume-detail", args=[self.resume.pk])

        self.assertEqual(self.client.get(detail_url).status_code, 404)
        self.assertEqual(
            self.client.patch(detail_url, {"title": "Hijacked"}, format="json").status_code,
            404,
        )
        self.assertEqual(self.client.delete(detail_url).status_code, 404)

        list_response = self.client.get(reverse("resume-list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data, [])

    def test_skill_assignment_restricted_to_owner(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(
            reverse("skill-list"),
            {"resume": self.resume.pk, "name": "Python", "level": 90},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Skill.objects.exists())

    def test_public_resume_endpoint_omits_owner_and_respects_is_public(self):
        public_url = reverse("public-resume", args=[self.resume.pk])

        self.resume.is_public = False
        self.resume.save(update_fields=["is_public"])
        self.assertEqual(self.client.get(public_url).status_code, 404)

        self.resume.is_public = True
        self.resume.save(update_fields=["is_public"])
        response = self.client.get(public_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["full_name"], self.resume.full_name)
        self.assertNotIn("user", response.data)

    @patch("resumes.pdf_export._build_pdf_response")
    def test_private_pdf_requires_owner(self, build_pdf):
        build_pdf.return_value = HttpResponse(b"%PDF-test", content_type="application/pdf")
        pdf_url = reverse("pdf-private", args=[self.resume.pk])

        self.assertEqual(self.client.get(pdf_url).status_code, 401)

        self.client.force_authenticate(user=self.other_user)
        self.assertEqual(self.client.get(pdf_url).status_code, 404)

        self.client.force_authenticate(user=self.owner)
        response = self.client.get(pdf_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        build_pdf.assert_called_once()

    @patch("resumes.pdf_export._build_pdf_response")
    def test_public_pdf_only_returns_public_resume(self, build_pdf):
        build_pdf.return_value = HttpResponse(b"%PDF-test", content_type="application/pdf")
        public_pdf_url = reverse("pdf-public", args=[self.resume.pk])

        self.resume.is_public = False
        self.resume.save(update_fields=["is_public"])
        self.assertEqual(self.client.get(public_pdf_url).status_code, 404)
        build_pdf.assert_not_called()

        self.resume.is_public = True
        self.resume.save(update_fields=["is_public"])
        response = self.client.get(public_pdf_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")


class ATSKeywordTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="ats-user",
            password="Strong-Test-Password!42",
            email="ats@example.com",
        )
        self.resume = Resume.objects.create(
            user=self.user,
            full_name="Amina Engineer",
            job_title="Python Developer",
            bio="Experienced Python and Django engineer building reliable APIs.",
            is_public=True,
        )
        Experience.objects.create(
            resume=self.resume,
            role="Backend Engineer",
            organization="Example Co",
            description="Built REST APIs with Django and PostgreSQL.",
        )
        Skill.objects.create(resume=self.resume, name="Python")
        Skill.objects.create(resume=self.resume, name="Django")
        Skill.objects.create(resume=self.resume, name="PostgreSQL")

    def test_keyword_extraction_handles_english_arabic_and_stop_words(self):
        keywords = extract_keywords("The Python, Django, PostgreSQL and قواعد APIs")

        self.assertIn("python", keywords)
        self.assertIn("django", keywords)
        self.assertIn("postgresql", keywords)
        self.assertIn("قواعد", keywords)
        self.assertNotIn("the", keywords)
        self.assertNotIn("and", keywords)

    def test_calculate_ats_score_returns_expected_values(self):
        result = calculate_ats_score(
            self.resume,
            "Python Django PostgreSQL Kubernetes",
        )

        self.assertIn("score", result)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 95)
        self.assertIn("python", result["matched_keywords"])
        self.assertIn("django", result["matched_keywords"])
        self.assertIn("postgresql", result["matched_keywords"])
        self.assertIn("kubernetes", result["missing_keywords"])

    def test_empty_or_stop_word_only_job_description_returns_error(self):
        result = calculate_ats_score(self.resume, "the and for")
        self.assertEqual(result["score"], 0)
        self.assertIn("error", result)