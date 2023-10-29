from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView, BlogDetailView

app_name = BlogConfig.name

# url адресация в приложении
urlpatterns = [
    path('', BlogListView.as_view(), name='index'),
    # Создать Блог
    path('create/', BlogCreateView.as_view(), name='create'),
    # Обновить Блог
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='update'),
    # Удалить Блог
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    # Просмотр Блога
    path('view/<int:pk>/', BlogDetailView.as_view(), name='view'),
]
