"""
API مخصص للإدارة — متاح فقط للمستخدمين بـ is_staff=True.
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count
from resumes.models import Resume
from resumes.serializers import ResumeSerializer

User = get_user_model()


class IsAdmin(permissions.BasePermission):
    """يسمح فقط للمديرين."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_stats(request):
    """إحصائيات المنصة."""
    total_users = User.objects.count()
    total_resumes = Resume.objects.count()
    public_resumes = Resume.objects.filter(is_public=True).count()
    active_users = User.objects.filter(is_active=True).count()

    # آخر 7 مستخدمين
    recent_users = User.objects.order_by('-created_at')[:7].values(
        'id', 'username', 'email', 'first_name', 'last_name',
        'plan', 'created_at', 'is_active', 'is_staff'
    )

    # آخر 7 سير
    recent_resumes = Resume.objects.order_by('-updated_at')[:7].values(
        'id', 'full_name', 'job_title', 'is_public', 'updated_at',
        'user__username'
    )

    return Response({
        'total_users': total_users,
        'total_resumes': total_resumes,
        'public_resumes': public_resumes,
        'active_users': active_users,
        'recent_users': list(recent_users),
        'recent_resumes': list(recent_resumes),
    })


@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_users(request):
    """قائمة كل المستخدمين."""
    users = User.objects.order_by('-created_at').values(
        'id', 'username', 'email', 'first_name', 'last_name',
        'plan', 'created_at', 'last_login', 'is_active', 'is_staff'
    )
    return Response(list(users))


@api_view(['PATCH'])
@permission_classes([IsAdmin])
def admin_toggle_user(request, pk):
    """تفعيل/تعطيل مستخدم."""
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'detail': 'غير موجود'}, status=404)

    if user == request.user:
        return Response({'detail': 'لا يمكنك تعطيل نفسك'}, status=400)

    user.is_active = not user.is_active
    user.save()
    return Response({
        'id': user.id,
        'is_active': user.is_active,
    })


@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_resumes(request):
    """كل السير في المنصة."""
    resumes = Resume.objects.select_related('user').order_by('-updated_at')
    data = [{
        'id': r.id,
        'full_name': r.full_name,
        'job_title': r.job_title,
        'is_public': r.is_public,
        'template': r.template,
        'language': r.language,
        'updated_at': r.updated_at,
        'username': r.user.username,
        'user_id': r.user.id,
    } for r in resumes]
    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAdmin])
def admin_delete_resume(request, pk):
    """حذف سيرة (إداري)."""
    try:
        resume = Resume.objects.get(pk=pk)
    except Resume.DoesNotExist:
        return Response({'detail': 'غير موجود'}, status=404)
    resume.delete()
    return Response({'deleted': True})