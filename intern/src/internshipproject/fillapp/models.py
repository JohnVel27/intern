from datetime import date
from django.db import models

class InternshipApplication(models.Model):
    APPLICATION_TYPE_CHOICES = [
        ('Voluntary', 'Voluntary'),
        ('Academic', 'Academic'),
    ]
    GENDER_TYPE_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    school = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year = models.IntegerField()
    birthdate = models.DateField()
    internship_position = models.CharField(max_length=100)
    internship_type = models.CharField(max_length=10, choices=APPLICATION_TYPE_CHOICES)
    gender_type = models.CharField(max_length=10, choices=GENDER_TYPE_CHOICES)
    required_hrs = models.PositiveIntegerField()
    resume_file_name = models.FileField(upload_to='resumes/')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # ← New image field
    application_date = models.DateField(auto_now_add=True)

    def get_age(self):
        today = date.today()
        return (
            today.year
            - self.birthdate.year
            - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        )
