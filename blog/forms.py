from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "thumbnail_image", "tags"]

class CommentForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)