from dal import autocomplete
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Member
from schools.models import School

class AccountCreationForm(UserCreationForm):
    
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="school-autocomplete",
            attrs={
                "data-placeholder": "Select a school..."
            }
        ),
        required=True,
    )

    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=True)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_school(self):
        school = self.cleaned_data.get("school")
        if not school or not School.objects.filter(urn=school.urn).exists():
            raise forms.ValidationError("Invalid school selection.")
        return school

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.is_active = False

        if commit:
            user.save()
            Member.objects.create(user=user, school=self.cleaned_data["school"], birth_date=self.cleaned_data["birth_date"])
        return user
        
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]