# coding: utf-8

from django import forms
from models import Blog, User


class LoginSystem(forms.Form):
	username = forms.CharField(label=u'用户名', max_length=255)
	password = forms.CharField(label=u'密码', max_length=50, widget=forms.PasswordInput)


class BlogChange(forms.ModelForm):
	class Meta:
		model = Blog
		fields = ('title', 'content')


class BlogAdd(forms.ModelForm):
	class Meta:
		model = Blog
		fields = ('title', 'content', 'author')


class UserRegist(forms.ModelForm):
	class Meta:
		model = User
		fields = ('name', 'password', 'qq', 'phone', 'email')

	def clean_name(self):
		username = self.cleaned_data.get('name', '')
		u_names = User.objects.filter(name=username)
		if u_names:
			self.add_error('name', u'该用户名已被注册')
		return username
