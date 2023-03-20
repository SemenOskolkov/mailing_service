from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_publication=Blog.STATUS_ACTIVE)
        return queryset


class BlogCreateView(UserPassesTestMixin, CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated


class BlogUpdateView(UserPassesTestMixin, UpdateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')

    def test_func(self):
        prod = self.get_object()
        return prod.user == self.request.user or self.request.user.has_perm('blog.change_blog')


class BlogDetailView(UserPassesTestMixin, DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    success_url = reverse_lazy('blog:blog_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.number_views += 1
        obj.save()
        return obj

    def get_blog_detail_from_cache(self):
        queryset = Blog.objects.all()
        if settings.CACHE_ENABLED:
            key = f'product_detail_{self.object.pk}'
            cache_data = cache.get(key)
            if cache_data is None:
                cache_data = queryset
                cache.set(key, cache_data)

            return cache_data

        return queryset

    def test_func(self):
        return self.request.user.is_authenticated


class BlogDeleteView(UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')

    def test_func(self):
        blog = self.get_object()
        return blog.user == self.request.user or self.request.user.has_perm('blog.delete_blog')


@permission_required(perm='blog.change_blog')
def change_status_blog(request, pk):
    '''Смена статуса публикации'''
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.status == Blog.STATUS_INACTIV:
        blog_item.status = Blog.STATUS_ACTIV
    else:
        blog_item.status = Blog.STATUS_ACTIV
    blog_item.save()
    return redirect(request.META.get('HTTP_REFERER'))
