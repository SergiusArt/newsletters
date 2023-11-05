from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from blog.models import Blog


# Является ли пользователь менеджером
def is_manager(user):
    return user.groups.filter(name='Manager').exists()


# Является ли пользователь контент-менеджером
def is_content_manager(user):
    return user.groups.filter(name='Content_manager').exists()


# Класс отображения страницы с блогами
class BlogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def test_func(self):
        return is_content_manager(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Класс создания нового блога
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Класс обновления существующего блога
class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Класс удаления существующего блога
class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Класс просмотра выбранного блога
class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


