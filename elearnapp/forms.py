from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = student_details
        fields = ['s_name', 's_id', 's_email', 's_password', 's_qualification', 'course']
        widgets = {
            'course': forms.CheckboxSelectMultiple(),
            's_password':forms.PasswordInput()
        }
class courseform(forms.ModelForm):
    class Meta:
        model=course_details
        fields='__all__'

class std(forms.forms):
    s_name=forms.CharField()