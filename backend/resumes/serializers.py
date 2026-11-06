from rest_framework import serializers
from .models import Resume, Experience, Skill, Certificate, ResumeLink


class OwnedResumeMixin:
    """يتأكد أن السيرة المرتبط بها العنصر تخص المستخدم الحالي (إنشاء وتعديل)."""

    def validate_resume(self, resume):
        request = self.context.get('request')
        if request is None or resume.user_id != request.user.id:
            raise serializers.ValidationError('غير مسموح بالتعديل على هذه السيرة.')
        return resume


class ExperienceSerializer(OwnedResumeMixin, serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'resume', 'role', 'organization', 'start_year',
                  'end_year', 'description', 'order']
        extra_kwargs = {
            'organization': {'required': False, 'allow_blank': True},
            'start_year': {'required': False, 'allow_blank': True},
            'end_year': {'required': False, 'allow_blank': True},
            'description': {'required': False, 'allow_blank': True},
        }


class SkillSerializer(OwnedResumeMixin, serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'resume', 'name', 'level', 'order']


class CertificateSerializer(OwnedResumeMixin, serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'resume', 'name', 'issuer', 'year',
                  'verify_url', 'order']
        extra_kwargs = {
            'issuer': {'required': False, 'allow_blank': True},
            'year': {'required': False, 'allow_blank': True},
            'verify_url': {'required': False, 'allow_blank': True},
        }


class ResumeLinkSerializer(OwnedResumeMixin, serializers.ModelSerializer):
    class Meta:
        model = ResumeLink
        fields = ['id', 'resume', 'label', 'url', 'icon', 'order']
        extra_kwargs = {
            'icon': {'required': False, 'allow_blank': True},
        }


class ResumeSerializer(serializers.ModelSerializer):
    experiences = ExperienceSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    certificates = CertificateSerializer(many=True, read_only=True)
    links = ResumeLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class PublicResumeSerializer(ResumeSerializer):
    """نسخة للعرض العام: بدون رقم المستخدم صاحب السيرة."""

    class Meta(ResumeSerializer.Meta):
        fields = None
        exclude = ['user']
