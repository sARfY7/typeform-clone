"""typeform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

def raise_zero_division_error(request):
    division_by_zero = 1 / 0

def raise_overflow_error(request):
    raise OverflowError('Result too large to be represented')

def raise_floating_point_error(request):
    raise FloatingPointError('Floating point operation failed')

def raise_attribute_error(request):
    raise AttributeError('Attribute not found')

def raise_import_error(request):
    raise ImportError("Import can't find module, or can't find name in module")

def raise_index_error(request):
    raise IndexError('Sequence index out of range')

def raise_key_error(request):
    raise KeyError('Mapping key not found')

def raise_name_error(request):
    raise NameError('Name not found globally')

def raise_type_error(request):
    raise TypeError('Inappropriate argument type')

def raise_value_error(request):
    raise ValueError('Inappropriate argument value (of correct type)')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('zero-division-error/', raise_zero_division_error),
    path('floating-point-error/', raise_floating_point_error),
    path('attribute-error/', raise_attribute_error),
    path('import-error/', raise_import_error),
    path('index-error/', raise_index_error),
    path('key-error/', raise_key_error),
    path('name-error/', raise_name_error),
    path('type-error/', raise_type_error),
    path('value-error/', raise_value_error),
    path('', include('tform.urls'))
]
