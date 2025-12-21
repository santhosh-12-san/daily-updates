from django.shortcuts import render
from .models import Student

def student_list(request):
    students = Student.objects.all()   # Fetch all rows
    return render(request, 'home/students.html', {
        'students': students
    })
