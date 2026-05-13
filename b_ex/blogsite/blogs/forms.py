from django import forms
from .models import Comment,Post,Contact

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'url', 'cat', 'image']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

        

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField()

class CustomSetPasswordForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField(max_length=6)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
