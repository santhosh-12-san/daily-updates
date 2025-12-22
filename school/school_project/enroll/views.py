from django.shortcuts import render, redirect
from .models import Student

def student_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')

        Student.objects.create(
            name=name,
            age=age,
            email=email
        )

        return redirect('student_form')

    students = Student.objects.all()
    return render(request, 'students.html', {'students': students})
