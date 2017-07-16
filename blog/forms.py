from django import forms
from .models import Comments,Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = [
            'ip',
            'postInformation',
            'commentsAllow',
        ]
