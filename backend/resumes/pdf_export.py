from urllib.parse import quote

from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Resume


def _content_disposition(filename):
    """اسم ملف آمن: بديل ASCII + نسخة UTF-8 (RFC 5987) للأسماء العربية."""
    return (
        'attachment; filename="resume.pdf"; '
        f"filename*=UTF-8''{quote(filename)}"
    )


def _build_pdf_response(resume, filename=None):
    """يبني HttpResponse يحتوي على PDF نصي."""
    from weasyprint import HTML

    html_string = render_to_string(
        'resumes/ats_pdf.html',
        {'resume': resume},
    )
    pdf_bytes = HTML(string=html_string).write_pdf()

    filename = filename or f"{resume.full_name or 'resume'}-CV.pdf"
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = _content_disposition(filename)
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
def export_pdf_public(request, pk):
    """تصدير PDF للسيرة العامة (بدون مصادقة)."""
    try:
        resume = Resume.objects.get(pk=pk, is_public=True)
    except Resume.DoesNotExist:
        return Response({'detail': 'السيرة غير موجودة أو غير عامة'}, status=404)
    return _build_pdf_response(resume)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_pdf_private(request, pk):
    """تصدير PDF للسيرة الخاصة (بعد تسجيل دخول)."""
    try:
        resume = Resume.objects.get(pk=pk, user=request.user)
    except Resume.DoesNotExist:
        return Response({'detail': 'غير موجودة'}, status=404)
    return _build_pdf_response(resume)
