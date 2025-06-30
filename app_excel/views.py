from docx import Document
from docxtpl import DocxTemplate
import openpyxl
from django.http import HttpResponse
from .models import Student
import io, os, zipfile
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .serializers import StudentSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentListCreateAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return None

    def get(self, request, pk):
        student = self.get_object(pk)
        if not student:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)
        if not student:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        if not student:
            return Response(status=status.HTTP_404_NOT_FOUND)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



def format_uzbek_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        oylar = [
            "yanvar", "fevral", "mart", "aprel", "may", "iyun",
            "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr"
        ]
        return f"{date_obj.year}-yil «{date_obj.day}» {oylar[date_obj.month - 1]}"
    except Exception:
        return ""


@login_required(login_url='login')
def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        filename = uploaded_file.name.lower()
        course = int(request.POST.get("course", 4))
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")

        Student.objects.all().delete()

        try:
            if filename.endswith('.xlsx'):
                wb = openpyxl.load_workbook(uploaded_file)
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if not row[1]:
                        continue
                    Student.objects.create(
                        full_name=row[1],
                        group=row[2],
                        company=row[3],
                        company_address=row[4],
                        company_director=row[5],
                        company_phone=row[6],
                        practice_supervisor=row[7],
                        faculty=row[8],
                    )

            elif filename.endswith('.docx'):
                doc = Document(uploaded_file)
                table = doc.tables[0]
                for row in table.rows[1:]:
                    cells = row.cells
                    Student.objects.create(
                        full_name=cells[1].text.strip(),
                        group=cells[2].text.strip(),
                        company=cells[3].text.strip(),
                        company_address=cells[4].text.strip(),
                        company_director=cells[5].text.strip(),
                        company_phone=cells[6].text.strip(),
                        practice_supervisor=cells[7].text.strip(),
                        faculty=cells[8].text.strip(),
                    )
            else:
                return render(request, 'app_excel/upload.html', {
                    'error': 'Faqat .xlsx yoki .docx fayl yuklash mumkin.'
                })

            request.session['uploaded'] = True
            request.session['course'] = course
            request.session['start_date'] = start_date
            request.session['end_date'] = end_date
            return redirect('upload_excel')

        except Exception as e:
            return render(request, 'app_excel/upload.html', {'error': str(e)})

    uploaded = request.session.pop('uploaded', False)
    return render(request, 'app_excel/upload.html', {'uploaded': uploaded})


@login_required(login_url='login')
def export_all_documents_zip(request):
    students = Student.objects.all()
    if not students.exists():
        return HttpResponse("Hali hech qanday talaba ma'lumotlari mavjud emas.")


    course = int(request.session.get("course", 4))
    start_date_str = request.session.get("start_date", "2025-02-17")
    end_date_str = request.session.get("end_date", "2025-04-26")


    OY_NOMLARI = {
        "January": "yanvar", "February": "fevral", "March": "mart",
        "April": "aprel", "May": "may", "June": "iyun", "July": "iyul",
        "August": "avgust", "September": "sentabr", "October": "oktabr",
        "November": "noyabr", "December": "dekabr"
    }

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    start_oy = OY_NOMLARI[start_date.strftime("%B")]
    end_oy = OY_NOMLARI[end_date.strftime("%B")]

    formatted_start = f"{start_date.year}-yil «{start_date.day:02}» {start_oy}"
    formatted_end = f"{end_date.year}-yil «{end_date.day:02}» {end_oy}"


    practice_type = "Ishlab chiqarish amaliyoti" if course == 3 else "Bitiruv oldi amaliyoti"


    shartnoma_path = os.path.join(settings.BASE_DIR, 'app_excel', 'templates', 'app_excel', 'shartnoma_template.docx')
    kundalik_path = os.path.join(settings.BASE_DIR, 'app_excel', 'templates', 'app_excel', 'kundalik_template.docx')
    yollanma_path = os.path.join(settings.BASE_DIR, 'app_excel', 'templates', 'app_excel', 'yollanma_template.docx')


    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for index, student in enumerate(students, start=1):
            folder_name = f"Hujjatlar/{index}"
            context = {
                'FULL_NAME': student.full_name,
                'GROUP': student.group,
                'COMPANY': student.company,
                'ADDRESS': student.company_address,
                'DIRECTOR': student.company_director,
                'PHONE': student.company_phone,
                'SUPERVISOR': student.practice_supervisor,
                'FACULTY': student.faculty,
                'COURSE': course,
                'PRACTICE_TYPE': practice_type,
                'STUDENT_COUNT': 1,
                'START_DATE': formatted_start,
                'END_DATE': formatted_end,
            }


            doc_shart = DocxTemplate(shartnoma_path)
            doc_shart.render(context)
            io_shart = io.BytesIO()
            doc_shart.save(io_shart)
            io_shart.seek(0)
            zip_file.writestr(f"{folder_name}/shartnoma.docx", io_shart.read())


            doc_kundalik = DocxTemplate(kundalik_path)
            doc_kundalik.render(context)
            io_kundalik = io.BytesIO()
            doc_kundalik.save(io_kundalik)
            io_kundalik.seek(0)
            zip_file.writestr(f"{folder_name}/kundalik.docx", io_kundalik.read())


            doc_yollanma = DocxTemplate(yollanma_path)
            doc_yollanma.render(context)
            io_yollanma = io.BytesIO()
            doc_yollanma.save(io_yollanma)
            io_yollanma.seek(0)
            zip_file.writestr(f"{folder_name}/yollanma.docx", io_yollanma.read())

    Student.objects.all().delete()

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=Hujjatlar.zip'
    return response



@login_required(login_url='login')
def export_to_word(request):
    students = Student.objects.all()
    if not students.exists():
        return HttpResponse("Hali hech qanday talaba ma'lumotlari mavjud emas.")

    course = int(request.GET.get("course", 4))
    start_date_str = request.GET.get("start_date")  # foydalanuvchidan kelgan sana
    formatted_start = format_uzbek_date(start_date_str)

    practice_type = "Ishlab chiqarish amaliyoti" if course == 3 else "Bitiruv oldi amaliyoti"
    student_count = students.count()
    first_student = students.first()

    doc_path = os.path.join(settings.BASE_DIR, 'app_excel', 'templates', 'app_excel', 'shartnoma_template.docx')
    doc = DocxTemplate(doc_path)

    context = {
        'COMPANY': first_student.company,
        'ADDRESS': first_student.company_address,
        'DIRECTOR': first_student.company_director,
        'PHONE': first_student.company_phone,
        'SUPERVISOR': first_student.practice_supervisor,
        'FACULTY': first_student.faculty,
        'COURSE': course,
        'PRACTICE_TYPE': practice_type,
        'STUDENT_COUNT': student_count,
        'START_DATE': formatted_start,
    }

    doc.render(context)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    Student.objects.all().delete()

    response = HttpResponse(
        buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{first_student.company.replace(" ", "_")}_shartnoma.docx"'
    return response


@login_required(login_url='login')
def generate_contract_for_company(request, company_name):
    students = Student.objects.filter(company=company_name)
    if not students.exists():
        return HttpResponse(" Bu korxona bo‘yicha talabalar topilmadi.")

    course = int(request.GET.get("course", 4))
    practice_type = "Ishlab chiqarish amaliyoti" if course == 3 else "Bitiruv oldi amaliyoti"

    first_student = students.first()
    student_count = students.count()

    doc = DocxTemplate(os.path.join(
        settings.BASE_DIR, 'app_excel', 'templates', 'app_excel', 'shartnoma_template.docx'))

    context = {
        'COMPANY': first_student.company,
        'ADDRESS': first_student.company_address,
        'DIRECTOR': first_student.company_director,
        'PHONE': first_student.company_phone,
        'SUPERVISOR': first_student.practice_supervisor,
        'FACULTY': first_student.faculty,
        'COURSE': course,
        'PRACTICE_TYPE': practice_type,
        'STUDENT_COUNT': student_count,
    }

    doc.render(context)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{company_name.replace(" ", "_")}_shartnoma.docx"'
    return response


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("upload_excel")  # Asosiy sahifaga yo'naltirish
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")

    return render(request, "app_excel/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Parollar mos emas!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Bu login allaqachon mavjud!")
        else:
            User.objects.create_user(username=username, password=password1)
            messages.success(request, "Muvaffaqiyatli ro‘yxatdan o‘tildi. Endi kirishingiz mumkin.")
            return redirect("login")

    return render(request, "app_excel/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")