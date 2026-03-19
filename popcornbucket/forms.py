from django import forms
from popcornbucket.models import Film, Review
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):

    #rating = forms.IntegerField(min_value=1, max_value=5, initial = 1) # change widget to 5 stars? styling widgets
    review_text = forms.CharField(widget=forms.Textarea, 
                                  max_length=Review.TEXT_MAX_LENGTH, 
                                  help_text="Leave your review...") # max length ok?

    class Meta:
        model = Review
        fields = ('review_text', )



