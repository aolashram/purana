from django import forms
from .models import LeaveRequest
from django.db.models import Q

class LeaveRequestForm(forms.ModelForm):
    leavefrom = forms.DateField(required=True)
    leavetill = forms.DateField(required=True)
    is_sick = forms.TypedChoiceField(choices=LeaveRequest.YESNO, initial=LeaveRequest.NO)
    comments= forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":20}))
    emp_hd = forms.HiddenInput()
    
    class Meta:
        model = LeaveRequest
        fields = [
            'leavefrom',
            'leavetill',
            'purpose',
            'is_sick',
            'comments',
        ]
    # def clean(self,**kwargs):
    #     leavefrom = self.cleaned_data['leavefrom']
    #     leavetill = self.cleaned_data['leavetill']
    #     #employee = self.cleaned_data['employee']
    #     id_ = self.kwargs.get("id")
    #     employee = get_object_or_404(Employee, id=id_)
    #     if leavefrom and leavetill and empid:
    #         query = Q(employee=employee)
    #         query.add(Q(leavetill__gte=leavefrom), Q.AND)
    #         query.add(Q(leavefrom__lte=leavetill), Q.AND)
    #         lreq = LeaveRequest.objects.filter(query)

    #         print(lreq.exists())
    #         data =False
    #         if lreq.exists():
    #             self.add_error('leavetill','Leave has already applied in the given range, please check and apply !')

    # def dclean_leavefrom(self):
    #     leavefrom = self.cleaned_data['leavefrom']
    #     leavetill = self.cleaned_data['leavetill']
    #     employee = self.cleaned_data['employee']
    #     leaverequests = LeaveRequest.objects.filter(employee=employee, leavetill__gte = leavefrom, leavefrom__lte = leavetill )
    #     if leaverequests.exists():
    #         raise ValidationError('Already applied leave on the same period')
    #     return message