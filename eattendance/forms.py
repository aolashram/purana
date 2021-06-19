from django.forms import fields
from .models.attendance import Roster, Shift
from django import forms
from Employee.models import Employee

class ShiftCreateForm(forms.ModelForm):
    SHIFT_CHOICES = (
        ('fixed-shift-time','Fixed Shift Time'),
    )
    shift_type = forms.ChoiceField(choices=SHIFT_CHOICES,required=True)
    shift_from = forms.TimeField(widget=forms.TextInput(attrs={'min':'00:00','max': '23:59','type': 'time'}), required=False)
    shift_to = forms.TimeField(widget=forms.TextInput(attrs={'min':'00:00','max': '23:59','type': 'time'}), required=False)
    margin_before = forms.TimeField(widget=forms.TextInput(attrs={'min':'00:00','max': '23:59','type': 'time'}), required=False)
    margin_after = forms.TimeField(widget=forms.TextInput(attrs={'min':'00:00','max': '23:59','type': 'time'}), required=False)
   
    class Meta:
        model = Shift
        exclude = ('created_date',)
        fields = (
            'name', 'shift_from','shift_to','shift_margin','margin_before','margin_after',
            'shift_type','created_by',
        )
    
    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop('user',[])
        super(ShiftCreateForm, self).__init__(*args, **kwargs)
        self.base_fields['shift_type'].initial = 'Fixed Shift Time'


class RosterCreateForm(forms.ModelForm):
    employee = forms.ModelChoiceField(None)
    duty_from = forms.DateField(required=True)
    duty_till = forms.DateField(required=True)
    
    class Meta:
        model = Roster
        exclude = ('created_date',)
        fields = ('employee','shift',)
    
    # def __init__(self, department, *args, **kwargs):
    #     super(RosterCreateForm, self).__init__(*args, **kwargs)
    #     self.fields['employee'].queryset = Employee.objects.filter(department__in=department)

