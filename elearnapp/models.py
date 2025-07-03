from django.db import models
from django.utils import timezone
class course_details(models.Model):
    course_name=models.CharField(max_length=50)
    course_id=models.IntegerField()
    course_video=models.URLField()
    def __str__(self):
        return self.course_name
    class Meta:
        db_table="course_details"
class student_details(models.Model):
    s_name=models.CharField(max_length=50)
    s_id=models.IntegerField()
    s_email=models.EmailField()
    s_password=models.IntegerField(unique=True)
    s_qualification=models.CharField(max_length=50)
    course=models.ManyToManyField(course_details)
    status=models.TextField(default="pending")
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table="student_details"

    






