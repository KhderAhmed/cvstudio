from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import (
    ResumeViewSet, ExperienceViewSet, SkillViewSet,
    CertificateViewSet, ResumeLinkViewSet, me, public_resume,
)
from .pdf_export import export_pdf_public, export_pdf_private
from .tts import generate_tts
from .ats import analyze_ats
from accounts.api import register
from accounts.admin_api import (
    admin_stats, admin_users, admin_toggle_user,
    admin_resumes, admin_delete_resume,
)
from analytics.api import resume_analytics, user_analytics

router = DefaultRouter()
router.register('resumes', ResumeViewSet, basename='resume')
router.register('experiences', ExperienceViewSet, basename='experience')
router.register('skills', SkillViewSet, basename='skill')
router.register('certificates', CertificateViewSet, basename='certificate')
router.register('links', ResumeLinkViewSet, basename='link')

urlpatterns = [
    path('auth/register/', register, name='register'),
    path('users/me/', me, name='me'),
    path('public/resumes/<int:pk>/', public_resume, name='public-resume'),
    path('public/resumes/<int:pk>/pdf/', export_pdf_public, name='pdf-public'),
    path('resumes/<int:pk>/pdf/', export_pdf_private, name='pdf-private'),
    path('resumes/<int:pk>/tts/', generate_tts, name='tts'),
    path('resumes/<int:pk>/ats/', analyze_ats, name='ats'),
    path('admin/stats/', admin_stats, name='admin-stats'),
    path('admin/users/', admin_users, name='admin-users'),
    path('admin/users/<int:pk>/toggle/', admin_toggle_user, name='admin-user-toggle'),
    path('admin/resumes/', admin_resumes, name='admin-resumes'),
    path('admin/resumes/<int:pk>/delete/', admin_delete_resume, name='admin-resume-delete'),
    path('analytics/resumes/<int:pk>/', resume_analytics, name='resume-analytics'),
    path('analytics/me/', user_analytics, name='user-analytics'),
] + router.urls