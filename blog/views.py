from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from blog.models import Blog


# Класс отображения страницы с блогами
class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


# Класс создания нового блога
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('blog:index')


# Класс обновления существующего блога
class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('blog:index')


# Класс удаления существующего блога
class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog')


# Класс просмотра выбранного блога
class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'


