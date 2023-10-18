!pip install Django

import os
from django.core.management import call_command

# Create a new Django project
os.makedirs('myproject')
os.chdir('myproject')

# Initialize a new Django project
call_command('startproject', 'myproject')

# Change the working directory to the project's root
os.chdir('myproject')

# Define the models in 'models.py' of your app
with open('myapp/models.py', 'w') as f:
    f.write('''
from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=50)

class Student(models.Model):
    name = models.CharField(max_length=50)
    teachers = models.ManyToManyField(Teacher)
''')

# Create a superuser for the admin panel
call_command('createsuperuser', interactive=False, username='admin', email='', database='default')

# Apply migrations to create the database schema
call_command('makemigrations', 'myapp', interactive=False)
call_command('migrate', interactive=False)

# Create views in 'views.py' of your app
with open('myapp/views.py', 'w') as f:
    f.write('''
from django.shortcuts import render
from .models import Teacher, Student

def display_students_and_teachers(request):
    teachers = Teacher.objects.all()
    students = Student.objects.all()
    return render(request, 'display_students_teachers.html', {'teachers': teachers, 'students': students})
''')

# Create URL patterns in 'urls.py' of your app
with open('myapp/urls.py', 'w') as f:
    f.write('''
from django.urls import path
from . import views

urlpatterns = [
    path('display/', views.display_students_and_teachers, name='display_students_teachers'),
]
''')

# Create HTML templates
os.makedirs('myapp/templates')
os.makedirs('myapp/templates/myapp')
with open('myapp/templates/myapp/display_students_teachers.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Students and Teachers</title>
</head>
<body>
    <h1>Teachers</h1>
    <ul>
        {% for teacher in teachers %}
            <li>{{ teacher.name }}</li>
        {% endfor %}
    </ul>
    <h1>Students</h1>
    <ul>
        {% for student in students %}
            <li>{{ student.name }}</li>
        {% endfor %}
    </ul>
</body>
</html>
''')

# Run the Django development server
call_command('runserver', '0.0.0.0:8000')
