from django import forms
from wtforms import Form, StringField, SelectField
from Base.models import School, Destination
from .models import UserProfile
from django.contrib.auth.forms import AuthenticationForm


class PickyAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                code='inactive',
            )
        if user.username.startswith('b'):
            raise forms.ValidationError(
                code='no_b_users',
            )


class CreateSchool(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'


class CreateDestination(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'


class AddUser(forms.Form):
    first_name = forms.CharField(max_length=50, label="نام", widget=forms.TextInput(attrs={'placeholder': '  '}))
    last_name = forms.CharField(max_length=50, label="نام خانوادگی",
                                widget=forms.TextInput(attrs={'placeholder': '  '}))
    username = forms.CharField()
    password = forms.CharField()


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
        labels = {
            'name_school': 'نام مدرسه',
            'mobile_school': ('تلفن مدرسه')
        }


class AddForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="نام", widget=forms.TextInput(attrs={'placeholder': '  '}))
    last_name = forms.CharField(max_length=50, label="نام خانوادگی",
                                widget=forms.TextInput(attrs={'placeholder': '  '}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': '  '}))
    mobile = forms.CharField(max_length=11, min_length=11, label="موبایل",
                             widget=forms.TextInput(attrs={'placeholder': '  '}))
    # name_school = forms.ModelChoiceField(queryset=School.objects.all())


class StudentForm(forms.Form):
    entryStatus_TYPE = (
        (1, "ورود"),
        (2, "خروج"),
    )
    name = forms.CharField(max_length=50, label="نام و نام خانوادگی",
                           widget=forms.TextInput(attrs={'placeholder': '  '}))
    className = forms.CharField(max_length=50, label="نام کلاس",
                                widget=forms.TextInput(attrs={'placeholder': '  '}))
    is_active = forms.BooleanField(widget=forms.TextInput(attrs={'placeholder': '  '}))
    title = forms.CharField(max_length=50, label="نام مقصد",
                            widget=forms.TextInput(attrs={'placeholder': '  '}))
    latitude = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': '  '}))
    longitude = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': '  '}))

    latitudeDelta = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': '  '}))
    longitudeDelta = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': '  '}))

    def __init__(self, *args, **kwargs):
        schoolid = kwargs.pop('schoolid', None)
        super(StudentForm, self).__init__(*args, **kwargs)

        if schoolid:
            self.fields['school_name'].queryset = School.objects.filter(id=schoolid)


class HeadmasterForm(AddForm, forms.Form):
    USER_TYPE = (
        (1, "مدیر"),
        (5, "ادمین"),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE, label="نوع کاربر")


class ParentForm(AddForm, forms.Form):
    USER_TYPE = (
        (4, "والدین"),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE, label="نوع کاربر")


class DriverForm(AddForm, forms.Form):
    USER_TYPE = (
        (3, "راننده"),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE, label="نوع کاربر")


class loginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  '}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  '}))


class DriverSearch(forms.Form):
    search = forms.CharField(label='سرچ',
                             widget=forms.TextInput(attrs={'placeholder': 'شماره موبایل'}))
