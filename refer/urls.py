from django.urls import path
from .views import *
urlpatterns = [
    path('', CreateCode.as_view(), name='create_code'),
    path('<int:pk>/delete/', CodeDelete.as_view(), name='code_delete'),
    path('register/', RegisterApiView.as_view(), name='register'),
    path('referals/', ReferalsApiView.as_view(), name='referals'),
]