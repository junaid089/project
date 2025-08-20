import namespace

from pr1 import admin
from project.pr1.urls import urlpatterns
from startup.admin import SecondAdmin
from startup.models import Starter, second

urlpatterns=urlpatterns+[

    ('admin/', admin.site.urls),
    ('starter/', second)
]
# projects_app/urls.py

from django.urls import path
from . import views

# Namespacing the URLs for this app. This is crucial for larger projects
# to avoid name collisions between different apps' URLs.
app_name = 'projects_app'

urlpatterns = [
    # Path for the project list view.
    # The empty string '' corresponds to the root URL of this app (e.g., /projects/).
    # `views.project_list` is the view function that will handle requests to this URL.
    # `name='project_list'` provides a unique name for this URL pattern.
    path('', views.project_list, name='project_list'),

    # Path for the project detail view.
    # '<int:pk>/' is a path converter that captures an integer from the URL
    # and passes it as a keyword argument 'pk' to the view function.
    # Example: A request to /projects/5/ will call views.project_detail(request, pk=5).
    path('<int:pk>/', views.project_detail, name='project_detail'),
]