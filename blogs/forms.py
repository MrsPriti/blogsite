from django import forms
from .models import Comment, Post, Category

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'cat', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title', 'class': 'validate'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your story...', 'class': 'materialize-textarea'}),
            'cat': forms.Select(attrs={'class': 'browser-default'}),
        }