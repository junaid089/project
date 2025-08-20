from django.shortcuts import render
from .models import Skill, Project

def home(request):
    skills = Skill.objects.all()
    projects = Project.objects.all()
    return render(request, 'portfolio/home.html', {'skills': skills, 'projects': projects})


# projects_app/views.py

from django.shortcuts import render, get_object_or_404
from .models import Project


def project_list(request):
    """
    Handles the request to display a list of all projects.

    1. Queries the database for all Project objects.
    2. Defines the context dictionary to pass the data to the template.
    3. Renders the 'project_list.html' template with the context.
    """
    # Retrieve all instances of the Project model from the database.
    # The '.objects.all()' is the standard Django ORM method for this.
    projects = Project.objects.all()

    # The context is a dictionary that maps variable names in the template
    # to Python objects. Here, the template will be able to access the
    # list of projects using the 'projects' variable.
    context = {
        'projects': projects
    }

    # The render function combines a given template with a given context
    # dictionary and returns an HttpResponse object with that rendered text.
    # The template path assumes a 'templates/projects_app/' directory structure.
    return render(request, 'projects_app/project_list.html', context)


def project_detail(request, pk):
    """
    Handles the request to display a single project, identified by its primary key (pk).

    1. Uses get_object_or_404 to retrieve a specific Project. This is a
       robust shortcut that raises an Http404 exception if the object is not found.
    2. Defines the context dictionary.
    3. Renders the 'project_detail.html' template with the context.
    """
    # Retrieve a single project by its primary key (pk).
    # If a project with the given pk does not exist, this will automatically
    # return a 404 Not Found page, which is a security and usability best practice.
    project = get_object_or_404(Project, pk=pk)

    # The context dictionary passes the single retrieved 'project' object
    # to the template.
    context = {
        'project': project
    }

    # Render the detail template with the specific project's data.
    return render(request, 'projects_app/project_detail.html', context)