import namespace

from pr1 import admin
from project.pr1.urls import urlpatterns
from startup.admin import SecondAdmin
from startup.models import Starter

urlpatterns=urlpatterns+[

    ('admin/', admin.site.urls),
    ('login/', Starter)
]