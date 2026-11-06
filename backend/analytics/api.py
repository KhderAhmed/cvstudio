from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
from .models import ResumeView
from resumes.models import Resume


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resume_analytics(request, pk):
    """إحصائيات سيرة معينة."""
    try:
        resume = Resume.objects.get(pk=pk, user=request.user)
    except Resume.DoesNotExist:
        return Response({'detail': 'غير موجودة'}, status=404)

    views = ResumeView.objects.filter(resume=resume)

    # إجمالي
    total_views = views.count()

    # آخر 7 أيام
    week_ago = timezone.now() - timedelta(days=7)
    views_week = views.filter(viewed_at__gte=week_ago).count()

    # آخر 30 يوم
    month_ago = timezone.now() - timedelta(days=30)
    views_month = views.filter(viewed_at__gte=month_ago).count()

    # حسب الجهاز
    device_stats = list(views.values('device').annotate(count=Count('id')))

    # حسب اليوم (آخر 14 يوم)
    daily = list(
        views.filter(viewed_at__gte=timezone.now() - timedelta(days=14))
        .annotate(date=TruncDate('viewed_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # آخر 10 مشاهدات
    recent = list(
        views.order_by('-viewed_at')[:10].values(
            'viewed_at', 'device', 'referrer'
        )
    )

    return Response({
        'total_views': total_views,
        'views_last_7_days': views_week,
        'views_last_30_days': views_month,
        'device_stats': device_stats,
        'daily_views': [
            {'date': str(d['date']), 'count': d['count']}
            for d in daily
        ],
        'recent_views': [
            {
                'viewed_at': r['viewed_at'].isoformat(),
                'device': r['device'],
                'referrer': r['referrer'],
            }
            for r in recent
        ],
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_analytics(request):
    """إحصائيات كل سير المستخدم."""
    resumes = Resume.objects.filter(user=request.user)
    views = ResumeView.objects.filter(resume__in=resumes)

    total = views.count()
    week_ago = timezone.now() - timedelta(days=7)
    week = views.filter(viewed_at__gte=week_ago).count()

    per_resume = list(
        resumes.annotate(views_count=Count('views'))
        .values('id', 'full_name', 'views_count')
        .order_by('-views_count')
    )

    return Response({
        'total_views': total,
        'views_last_7_days': week,
        'total_resumes': resumes.count(),
        'per_resume': per_resume,
    })