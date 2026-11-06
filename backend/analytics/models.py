from django.db import models
from resumes.models import Resume


class ResumeView(models.Model):
    """سجل مشاهدة سيرة."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name='views')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device = models.CharField(max_length=20, blank=True)  # desktop/mobile/tablet
    referrer = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        verbose_name = 'مشاهدة'
        verbose_name_plural = 'المشاهدات'

    def __str__(self):
        return f'{self.resume.full_name} — {self.viewed_at:%Y-%m-%d %H:%M}'