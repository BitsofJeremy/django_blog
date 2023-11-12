from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    """ Build a form """
    # rendered type="text" HTML element
    name = forms.CharField(max_length=25)
    # rendered as text, but has email address validation
    email = forms.EmailField()
    to = forms.EmailField()
    # rendered <textarea> HTML element
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )


class CommentForm(forms.ModelForm):
    class Meta:
        # use the Comment model to create the form
        model = Comment
        # What form fields to use
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()

