from django import forms
from django.forms import fields

from .models import Department, DietOrder, Doctor, Patient,Visit,Room,Bed,Area,ItemCategory

class PatientCreateForm(forms.ModelForm):
    MALE='Male'
    FEMALE='Female'
    OTHER = 'Other'
    GENDER = (
        (MALE,MALE),
        (FEMALE,FEMALE),
        (OTHER,OTHER),
    )
    fullname = forms.CharField(max_length=120, required=True)
    mrno = forms.CharField(max_length=15, required=True)
    gender = forms.ChoiceField(choices=GENDER,required=True)
    age = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.all()
        self.fields['bedno'].queryset = Bed.objects.all()

    class Meta:
        model = Visit
        exclude = ()
        fields = ('fullname','mrno','gender','age','ipno','building_floor','room','bedno','department')

class DietOrderForm(forms.ModelForm):
    MALE='Male'
    FEMALE='Female'
    OTHER = 'Other'
    GENDER = (
        (MALE,MALE),
        (FEMALE,FEMALE),
        (OTHER,OTHER),
    )
    DIET_SLOT = (
        ('-1','SELECT A SLOT'),
        ('Breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner'),
        ('Special','Special'),
    )
    fullname = forms.CharField(max_length=120, required=True)
    mrno = forms.CharField(max_length=15, required=True)
    gender = forms.ChoiceField(choices=GENDER,required=True)
    age = forms.IntegerField(required=True)
    ipno = forms.CharField(max_length=10)
    department = forms.ModelChoiceField(queryset=Department.objects.all(),required=False)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())
    building_floor = forms.ModelChoiceField(queryset=Area.objects.all())
    room = forms.ModelChoiceField(queryset=Room.objects.all())
    bedno = forms.ModelChoiceField(queryset=Bed.objects.all())
    slot = forms.ChoiceField(choices=DIET_SLOT,required=True,widget=forms.Select(attrs={'onchange':'isSlotAvailable()'}))
    category = forms.ModelChoiceField(queryset=ItemCategory.objects.filter(active=True))
    special_instruction = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    quantity = forms.IntegerField(required=True)
    delivery_date = forms.DateField()
    patient = forms.CharField(widget = forms.HiddenInput(), required = False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.all()
        self.fields['bedno'].queryset = Bed.objects.all()
        self.fields['quantity'].initial = 1

    class Meta:
        model = DietOrder
        exclude = ('created_date',)
        fields = ('fullname','mrno','gender','age','ipno','department',
                    'room','bedno','category','item','building_floor',
                    'special_instruction','slot','quantity','delivery_date')

class DietOrderUpdateForm(forms.ModelForm):
    MALE='Male'
    FEMALE='Female'
    OTHER = 'Other'
    GENDER = (
        (MALE,MALE),
        (FEMALE,FEMALE),
        (OTHER,OTHER),
    )
    DIET_SLOT = (
        ('-1','SELECT A SLOT'),
        ('Breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner'),
        ('Special','Special'),
    )
    fullname = forms.CharField(max_length=120,disabled=True)
    mrno = forms.CharField(max_length=15,disabled=True)
    gender = forms.ChoiceField(choices=GENDER,disabled=True)
    age = forms.IntegerField(disabled=True)
    ipno = forms.CharField(disabled=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(),disabled=True)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),disabled=True)
    building_floor = forms.ModelChoiceField(queryset=Area.objects.all(),disabled=True)
    room = forms.ModelChoiceField(queryset=Room.objects.all(),disabled=True)
    bedno = forms.ModelChoiceField(queryset=Bed.objects.all(),disabled=True)
    slot = forms.ChoiceField(choices=DIET_SLOT)
    category = forms.ModelChoiceField(queryset=ItemCategory.objects.filter(active=True))
    special_instruction = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    quantity = forms.IntegerField(required=True)
    patient = forms.CharField(widget = forms.HiddenInput(),disabled=True)
    doid = forms.IntegerField(widget = forms.HiddenInput(),disabled=True)
    delivery_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.all()
        self.fields['bedno'].queryset = Bed.objects.all()
        self.fields['quantity'].initial = 1

    class Meta:
        model = DietOrder
        exclude = ('created_date',)
        fields = ('fullname','mrno','gender','age','ipno','department',
                    'room','bedno','category','item','building_floor',
                    'special_instruction','slot','quantity','delivery_date')