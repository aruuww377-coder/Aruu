# posdb/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ── Admin ─────────────────────────────
    path('admin/', admin.site.urls),

    # ── Apps ──────────────────────────────
    path('sales/', include('sales.urls')),
    path('wheel_timer/', include('wheel_timer.urls')),

    # ── Authentication (Django built-in) ──
    path('accounts/', include('django.contrib.auth.urls')),

    # ── Home redirect ──────────────────────
    # Option 1: like teacher (recommended for POS system)
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),

    # If you prefer your version instead, use this:
    # path('', RedirectView.as_view(url='/sales/products_list/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
