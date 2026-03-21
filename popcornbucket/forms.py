from django import forms
from popcornbucket.models import Film, Review
from .models import UserProfile

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