from django import forms
from .models import Employee
from django.forms.models import inlineformset_factory

class EmployeeModelForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'title',
            'first_name',
            'middle_name', 
            'last_name',
            'sur_name',
            'date_of_birth', 
            'gender',
            'email',
            'marital_status',
            'address',
            'country',
            'state',
            'district',
            'pincode',
            'aadhaar_number',
            'pan_number',
            'qualification',
            'father_name',
            'mother_name',
            'registration_details',
            'emp_code',
            'department',
            'designation',
            'ccim_employment_status',
            'bank_name',
            'branch_name',
            'ifsc_code',
            'account_no',
            'date_of_join',
            'date_of_confirmation',
            'employment_status',
            'pf_number',
            'esi_number',
            'line_manager',
        ]