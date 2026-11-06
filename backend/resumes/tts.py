"""
خدمة تحويل النص إلى صوت باستخدام gTTS.
"""
import logging
from io import BytesIO

from django.core.files.base import ContentFile
from django.utils.text import slugify
from gtts import gTTS
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Resume

logger = logging.getLogger(__name__)

MAX_CHARS = 5000
SUPPORTED_LANGS = ('ar', 'en', 'fr', 'es', 'de')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_tts(request, pk):
    """
    يولّد ملف صوتي من نص ويحفظه في السيرة.
    Body: {"text": "..."} أو {"use_bio": true}
    """
    try:
        resume = Resume.objects.get(pk=pk, user=request.user)
    except Resume.DoesNotExist:
        return Response({'detail': 'السيرة غير موجودة'}, status=404)

    text = (request.data.get('text') or '').strip()
    use_bio = request.data.get('use_bio', False)

    if use_bio and resume.bio:
        text = resume.bio.strip()

    if not text:
        return Response({'detail': 'لم يتم تزويد نص'}, status=400)

    text = text[:MAX_CHARS]

    lang = resume.language or 'ar'
    if lang not in SUPPORTED_LANGS:
        lang = 'ar'

    try:
        buffer = BytesIO()
        gTTS(text=text, lang=lang, slow=False).write_to_fp(buffer)
        buffer.seek(0)

        base_name = slugify(resume.full_name) or 'intro'
        filename = f'{base_name}-{pk}-tts.mp3'

        if resume.audio_intro:
            try:
                resume.audio_intro.delete(save=False)
            except Exception:
                logger.warning('Could not delete old audio for resume %s', pk)

        resume.audio_intro.save(filename, ContentFile(buffer.read()), save=True)

        return Response({
            'success': True,
            'audio_url': resume.audio_intro.url,
            'text_used': text[:100] + ('...' if len(text) > 100 else ''),
            'characters': len(text),
        })

    except Exception:
        # التفاصيل في السجلات فقط، لا نرسلها للمستخدم
        logger.exception('TTS generation failed for resume %s', pk)
        return Response(
            {'detail': 'فشل توليد الصوت، حاول مرة أخرى لاحقاً'},
            status=500,
        )
