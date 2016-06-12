from django.db import models
from django.utils import timezone

# Create your models here.


class Author(models.Model):
	name = models.CharField(max_length=50)
	age = models.IntegerField()

	def __unicode__(self):
		return self.name


class Blog(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	counter = models.IntegerField(default=0)
	pubDate = models.DateField(auto_now_add=True)
	author = models.ForeignKey(Author)

	def __unicode__(self):
		return self.title


class User(models.Model):
	name = models.CharField(max_length=255)
	qq = models.CharField(max_length=20, blank=True, null=True)
	phone = models.CharField(max_length=20, null=True, blank=True)
	register_time = models.DateTimeField(auto_now_add=True)
	email = models.EmailField(blank=True, null=True)
	password = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name