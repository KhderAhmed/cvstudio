from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # لوحة Django على /django-admin/ حتى لا تتعارض مع صفحة /admin في الفرونت (Vue)
    path('django-admin/', admin.site.urls),
    path('api/', include('resumes.api_urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # الملفات المرفوعة (صوت، صور، فيديو). تعمل أيضاً عندما DEBUG=False
    # حتى يخدمها nginx عبر proxy. للتحميل الكبير الأفضل لاحقاً تخديمها من nginx مباشرة.
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
