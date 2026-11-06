from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Resume(models.Model):
    """السيرة الذاتية الحيّة."""
    TEMPLATE_CHOICES = [
        ('classic', 'كلاسيكي'),
        ('modern', 'حديث'),
        ('minimal', 'بسيط'),
    ]
    LANGUAGE_CHOICES = [
        ('ar', 'العربية'),
        ('en', 'English'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='resumes')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    title = models.CharField(max_length=200, default='سيرتي الذاتية')
    full_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES,
                                default='modern')
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES,
                                default='ar')
    is_public = models.BooleanField(default=True)

    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    audio_intro = models.FileField(upload_to='audio/', blank=True, null=True)
    video_intro = models.FileField(upload_to='video/', blank=True, null=True)
    video_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'سيرة ذاتية'
        verbose_name_plural = 'السير الذاتية'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.full_name or self.user.username) or 'cv'
            slug = base
            counter = 1
            while Resume.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.full_name} — {self.title}'


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name='experiences')
    role = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    start_year = models.CharField(max_length=20, blank=True)
    end_year = models.CharField(max_length=20, blank=True, default='الآن')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'خبرة'
        verbose_name_plural = 'الخبرات'

    def __str__(self):
        return f'{self.role} @ {self.organization}'


class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name='skills')
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=80)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'مهارة'
        verbose_name_plural = 'المهارات'

    def __str__(self):
        return f'{self.name} ({self.level}%)'


class Certificate(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name='certificates')
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=10, blank=True)
    verify_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'شهادة'
        verbose_name_plural = 'الشهادات'

    def __str__(self):
        return self.name


class ResumeLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name='links')
    label = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.CharField(max_length=30, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'رابط'
        verbose_name_plural = 'الروابط'

    def __str__(self):
        return f'{self.label} → {self.url}'