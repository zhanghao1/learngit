# coding: utf-8
from django.shortcuts import render, render_to_response
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse, FileResponse
from models import Blog, User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from forms import LoginSystem, BlogChange, BlogAdd, UserRegist

# Create your views here.


def showBlog(request, blogId):
	t = loader.get_template('blog.html')
	try:
		blog = Blog.objects.get(id=blogId)
	except Blog.DoesNotExist:
		return HttpResponse(u'您访问的博客不存在<a href="javascript:history.go(-1)">返回</a>', status=403)
	blog.counter += 1
	blog.save()
	context = {'blog': blog}
	html = t.render(context)
	return HttpResponse(html)


@csrf_exempt
def showBlogList(request):
	t = loader.get_template('blog_list.html')
	blogs = Blog.objects.all()
	context = {'blog': blogs}
	html = t.render(context)
	return HttpResponse(html)


@csrf_exempt
def loginIn(request):
	if request.method == 'POST':
		form = LoginSystem(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			# user = authenticate(username=username, password=password)
			try:
				user = User.objects.get(name=username, password=password)
			except User.DoesNotExist:
				context = {
					'form': form,
					'errors': u'用户名或密码错误',
				}
				return render_to_response('login.html', context)
			if user:
				blogs = Blog.objects.all()
				context = {'blog': blogs}
				# return render_to_response('blog_list.html', context, context_instance=RequestContext(request))
				return HttpResponseRedirect('/bloglist')
			
		else:
			context = {
				'form': form,
				'errors': form.errors,
			}
			return render_to_response('login.html', context)
	else:
		form = LoginSystem()
		context = {
			'form': form
		}
		# return render_to_response('login.html', context)
		return render(request, 'login.html', context)


@csrf_exempt
def edit_blog(request, blogId):
	if request.method == 'POST':
		b = Blog.objects.get(id=blogId)
		form = BlogChange(request.POST, instance=b)
		if form.is_valid():
			form.save()
			# return render_to_response('blog_list.html', context)
			return HttpResponseRedirect('/bloglist')
		else:
			content = {
				'form': form,
				'error': form.errors,
			}
			return render_to_response('edit_blog.html', content)
	else:
		b = Blog.objects.get(id=blogId)
		form = BlogChange(instance=b)
		content = {
			'form': form
		}
		return render_to_response('edit_blog.html', content)


@csrf_exempt
def delete_blog(request, blogId):
	try:
		b = Blog.objects.get(id=blogId)
	except Blog.DoesNotExist:
		return HttpResponse('删除的博客不存在！')
	b.delete()
	return HttpResponseRedirect('/bloglist')


@csrf_exempt
def add_blog(request):
	if request.method == 'POST':
		form = BlogAdd(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/bloglist')
		else:
			content = {
				'form': form,
				'errors': form.errors
			}
			return render_to_response('add_blog.html', content)
	else:
		form = BlogAdd()
		content = {
			'form': form
		}
		return render_to_response('add_blog.html', content)


@csrf_exempt
def register(request):
	if request.method == 'POST':
		form = UserRegist(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/login')
		else:
			content = {
				'form': form,
				'errors': form.errors
			}
			return render(request, 'regist.html', content)
	else:
		form = UserRegist()
		content = {
			'form': form
		}
		return render(request, 'regist.html', content)