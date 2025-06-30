from django.db import models


class Student(models.Model):
    full_name = models.CharField(max_length=255)
    group = models.CharField(max_length=50)
    company = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_director = models.CharField(max_length=255)
    company_phone = models.CharField(max_length=50)
    practice_supervisor = models.CharField(max_length=255)
    faculty = models.CharField(max_length=150)

    def __str__(self):
        return self.full_name
