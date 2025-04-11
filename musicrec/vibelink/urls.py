from django.urls import path

from .views import test_function

urlpatterns = [
    path('test/', test_function, name='test_function'),
]