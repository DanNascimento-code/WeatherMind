

"""PROJECT'S ROOT ROUTER FILE, DELEGATES ROUTES TO EACH APPLICATION

    /           → core (home)
   /dashboard/ → dashboard.urls
  /api/       → core.urls.insight_urls
 /admin/     → Django admin

"""


from django.contrib import admin
from django.urls import path, include
from core.views import home  # Import the home view from core.views.home.py


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),  # Defines the root URL route ('')
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('core.urls.insight_urls')),
]
