"""
Middleware يسجّل كل مشاهدة لصفحة سيرة عامة.
"""
from .models import ResumeView
from resumes.models import Resume


class TrackResumeViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # سجّل فقط GET على /api/public/resumes/<id>/
        if (request.method == 'GET'
                and request.path.startswith('/api/public/resumes/')
                and response.status_code == 200):
            try:
                # استخرج pk من المسار
                parts = request.path.strip('/').split('/')
                # /api/public/resumes/1/ → ['api', 'public', 'resumes', '1']
                if len(parts) >= 4:
                    pk = int(parts[3])
                    resume = Resume.objects.get(pk=pk, is_public=True)
                    self.log_view(request, resume)
            except (ValueError, Resume.DoesNotExist, IndexError):
                pass

        return response

    def log_view(self, request, resume):
        # تجنّب تسجيل نفس المشاهدة من نفس IP في آخر 5 دقائق
        ip = self.get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')

        from django.utils import timezone
        from datetime import timedelta
        recent = ResumeView.objects.filter(
            resume=resume,
            ip_address=ip,
            viewed_at__gte=timezone.now() - timedelta(minutes=5),
        ).exists()

        if recent:
            return

        ResumeView.objects.create(
            resume=resume,
            ip_address=ip,
            user_agent=ua[:500],
            device=self.detect_device(ua),
            referrer=request.META.get('HTTP_REFERER', '')[:500],
        )

    def get_client_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    def detect_device(self, ua):
        ua_lower = ua.lower()
        if 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
            return 'mobile'
        if 'tablet' in ua_lower or 'ipad' in ua_lower:
            return 'tablet'
        return 'desktop'