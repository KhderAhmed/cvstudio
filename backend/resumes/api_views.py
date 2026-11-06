from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from .models import Resume, Experience, Skill, Certificate, ResumeLink
from .serializers import (
    ResumeSerializer, PublicResumeSerializer, ExperienceSerializer,
    SkillSerializer, CertificateSerializer, ResumeLinkSerializer,
)


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Resume.objects.filter(user=self.request.user)
            .prefetch_related('experiences', 'skills', 'certificates', 'links')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ملكية السيرة يتحقق منها OwnedResumeMixin داخل الـ serializers،
# والـ queryset هنا يضمن أن المستخدم لا يرى إلا عناصر سيره.
class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(resume__user=self.request.user)


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(resume__user=self.request.user)


class CertificateViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(resume__user=self.request.user)


class ResumeLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResumeLink.objects.filter(resume__user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def public_resume(request, pk):
    """عرض السيرة العامة بدون مصادقة."""
    try:
        resume = Resume.objects.get(pk=pk, is_public=True)
    except Resume.DoesNotExist:
        return Response(
            {'detail': 'السيرة غير موجودة أو غير عامة'},
            status=404,
        )
    serializer = PublicResumeSerializer(resume, context={'request': request})
    return Response(serializer.data)
