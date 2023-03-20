from django import forms

from base.forms import StyleFormMixin
from blog.models import Blog


class BlogForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Blog
        exclude = ['owner',]