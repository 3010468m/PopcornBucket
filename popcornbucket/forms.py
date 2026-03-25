from django import forms
from popcornbucket.models import Film, Review
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review_text', 'rating', )
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']