"""
محلل ATS — يحسب درجة توافق السيرة مع وصف وظيفي.
"""
import re
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Resume


STOP_WORDS = {
    # articles & prepositions
    'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were',
    'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
    'the', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
    'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
    'his', 'its', 'our', 'their', 'what', 'which', 'who', 'when', 'where',
    'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
    'so', 'than', 'too', 'very', 'just', 'also', 'about', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'up', 'down', 'out',
    'off', 'over', 'under', 'again', 'further', 'then', 'once',
    # job description filler words (ليست مهارات)
    'ideal', 'candidate', 'looking', 'required', 'requirements',
    'responsibilities', 'role', 'position', 'job', 'work', 'working',
    'experience', 'experienced', 'years', 'year', 'strong', 'skills',
    'knowledge', 'ability', 'team', 'teams', 'using', 'use', 'used',
    'building', 'build', 'built', 'plus', 'good', 'great', 'excellent',
    'must', 'should', 'will', 'need', 'needs', 'want', 'wants',
    'passionate', 'skilled', 'solving', 'problem', 'collaboration',
    'collaborate', 'communication', 'web', 'applications', 'application',
    'developer', 'developers', 'develop', 'development',
    'engineer', 'engineers', 'engineering',
    'senior', 'junior', 'mid', 'lead', 'principal', 'staff',
}


ARABIC_STOP_WORDS = {
    'في', 'من', 'على', 'الى', 'إلى', 'عن', 'مع', 'هذا', 'هذه', 'ذلك', 'تلك',
    'التي', 'الذي', 'الذين', 'أو', 'او', 'أن', 'ان', 'إن', 'كان', 'يجب',
    'لدى', 'عند', 'كل', 'بين', 'أي', 'ذات', 'ذو', 'لا', 'ما', 'هو', 'هي',
    'نحن', 'أنت', 'كما', 'حيث', 'أيضا', 'أيضاً', 'ثم', 'قد', 'لقد', 'بعد',
    'قبل', 'خلال', 'عبر', 'حول', 'فقط', 'جدا', 'جداً',
    # كلمات شائعة في إعلانات الوظائف (ليست مهارات)
    'خبرة', 'سنوات', 'سنة', 'مطلوب', 'المطلوب', 'متطلبات', 'وظيفة', 'فريق',
    'القدرة', 'معرفة', 'مهارات', 'جيدة', 'قوية', 'ممتازة', 'مسؤوليات',
    'المسؤوليات', 'المرشح', 'نبحث', 'تطوير', 'مطور', 'مهندس',
}

_ARABIC_MARKS = re.compile(r'[\u064B-\u0652\u0640]')  # التشكيل والتطويل


def extract_keywords(text):
    """يستخرج الكلمات المفتاحية (إنكليزية + عربية)."""
    if not text:
        return set()
    text = _ARABIC_MARKS.sub('', text.lower())
    # اترك: حروف لاتينية، أرقام، حروف عربية، ورموز تقنية (+ # . -)
    cleaned = re.sub(r"[^a-z0-9\u0600-\u06FF+#.\-]+", " ", text)
    keywords = set()
    for w in cleaned.split():
        w = w.strip('.-')  # "python." في نهاية الجملة يصير "python"
        if len(w) > 2 and w not in STOP_WORDS and w not in ARABIC_STOP_WORDS:
            keywords.add(w)
    return keywords


def get_resume_text(resume):
    """يجمع كل نص السيرة."""
    parts = [
        resume.full_name or '',
        resume.job_title or '',
        resume.bio or '',
    ]
    for exp in resume.experiences.all():
        parts.append(exp.role or '')
        parts.append(exp.organization or '')
        parts.append(exp.description or '')
    for skill in resume.skills.all():
        parts.append(skill.name or '')
    for cert in resume.certificates.all():
        parts.append(cert.name or '')
        parts.append(cert.issuer or '')
    return ' '.join(parts)


def calculate_ats_score(resume, job_description):
    """يحسب درجة ATS بواقعية (0-95)."""
    jd_keywords = extract_keywords(job_description)
    resume_text = get_resume_text(resume)
    resume_keywords = extract_keywords(resume_text)

    if not jd_keywords:
        return {
            'score': 0,
            'error': 'الوصف الوظيفي فارغ أو لا يحتوي كلمات مفتاحية',
        }

    matched = jd_keywords & resume_keywords
    missing = jd_keywords - resume_keywords

    base_score = (len(matched) / len(jd_keywords)) * 100

    # ===== عقوبات =====
    penalty = 0
    if len(resume.bio or '') < 100:
        penalty += 10
    if resume.experiences.count() == 0:
        penalty += 15
    if resume.skills.count() < 3:
        penalty += 10
    if len(resume_text) < 300:
        penalty += 10
    if len(jd_keywords) > 0 and len(missing) > len(jd_keywords) / 2:
        penalty += 5

    # ===== مكافآت =====
    bonus = 0
    if len(resume.bio or '') > 200:
        bonus += 3
    if resume.experiences.count() >= 2:
        bonus += 3
    if resume.skills.count() >= 5:
        bonus += 4

    score = int(base_score + bonus - penalty)
    score = max(0, min(95, score))

    jd_lower = job_description.lower()
    missing_sorted = sorted(missing, key=lambda w: -jd_lower.count(w))[:20]
    matched_sorted = sorted(matched, key=lambda w: -jd_lower.count(w))[:20]

    return {
        'score': score,
        'base_score': int(base_score),
        'bonus': bonus,
        'penalty': penalty,
        'matched_keywords': matched_sorted,
        'missing_keywords': missing_sorted,
        'total_jd_keywords': len(jd_keywords),
        'matched_count': len(matched),
        'missing_count': len(missing),
        'tips': generate_tips(score, missing_sorted),
    }


def generate_tips(score, missing):
    """اقتراحات واقعية."""
    tips = []

    if score >= 80:
        tips.append('✅ سيرتك متوافقة بشكل ممتاز. أرسلها بثقة!')
    elif score >= 60:
        tips.append('👍 سيرتك جيدة، لكن يمكن تحسينها بإضافة كلمات مفتاحية.')
    elif score >= 40:
        tips.append('⚠️ سيرتك تحتاج تحسيناً. أضف مهارات وخبرات مرتبطة بالوظيفة.')
    else:
        tips.append('🔴 سيرتك ضعيفة التوافق. راجع المحتوى وأضف الكلمات المفقودة.')

    if missing:
        display = ', '.join(missing[:8])
        tips.append(f'أضف هذه الكلمات المفتاحية: {display}')

    if score < 70:
        tips.append('أضف وصفاً مفصلاً للخبرات (3-5 نقاط لكل خبرة).')
        tips.append('اذكر المهارات التقنية بأسمائها الدقيقة (Python, Django, PostgreSQL).')
        tips.append('اكتب نبذة من 100-200 كلمة تصف خبراتك وأهدافك.')

    return tips


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_ats(request, pk):
    """يحلل توافق السيرة مع وصف وظيفي."""
    try:
        resume = Resume.objects.get(pk=pk, user=request.user)
    except Resume.DoesNotExist:
        return Response({'detail': 'السيرة غير موجودة'}, status=404)

    job_description = (request.data.get('job_description') or '').strip()

    if not job_description:
        return Response(
            {'detail': 'أرسل الوصف الوظيفي في "job_description"'},
            status=400,
        )

    result = calculate_ats_score(resume, job_description)
    return Response(result)