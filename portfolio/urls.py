from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='portfolio-home'),
]

# portfolio_project/urls.py

from django.contrib import admin
from django.urls import path, include

# Import settings and static to serve media files during development.
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include the URL patterns from the 'projects_app'.
    # Any request to a URL starting with 'projects/' will be handed off
    # to the 'projects_app.urls' module for further processing.
    # For example:
    #   - /projects/       -> handled by projects_app.urls -> project_list view
    #   - /projects/123/   -> handled by projects_app.urls -> project_detail view
    path('projects/', include('projects_app.urls')),

    # Add other project-level paths here...
]

# This is a common pattern for serving media files (like project images)
# uploaded by users during development. This is NOT suitable for production.
# In a production environment, your web server (e.g., Nginx) should be
# configured to serve media files directly.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)