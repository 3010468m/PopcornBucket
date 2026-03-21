from django import forms
from popcornbucket.models import Film, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review_text', 'rating', )
        