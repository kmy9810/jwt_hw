from django.urls import path
from todoes import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.TodoView.as_view(), name='todo_view'),
    path('<int:todo_id>/', views.TodoDetailView.as_view(), name='todo_detail_view'),
]
