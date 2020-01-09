from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_list, name='form_list'),
    path('form/new', views.form_new, name='form_new'),
    path('form/<int:id>', views.form_view, name='form_view'),
    path('form/<int:id>/delete', views.form_delete, name='form_delete'),
    path('form/<int:id>/publish', views.form_publish, name='form_publish'),
    path('form/<int:id>/response', views.response_list, name='response_list'),
    path('form/<int:id>/response/download', views.response_download, name='response_download'),
    path('form/<int:form_id>/response/<int:id>', views.response_view, name='response_view'),
    path('form/<int:id>/edit', views.form_edit, name='form_edit'),
    path('form/<int:id>/textfield/new', views.textfield_new, name='textfield_new'),
    path('form/<int:form_id>/textfield/<int:id>/edit', views.textfield_edit, name='textfield_edit'),
    path('form/<int:form_id>/textfield/<int:id>/delete', views.textfield_delete, name='textfield_delete'),
    path('form/<int:id>/mcqfield/new', views.mcqfield_new, name='mcqfield_new'),
    path('form/<int:form_id>/mcqfield/<int:id>/edit', views.mcqfield_edit, name='mcqfield_edit'),
    path('form/<int:form_id>/mcqfield/<int:id>/delete', views.mcqfield_delete, name='mcqfield_delete'),
    path('signup/', views.signup, name='signup'),
]
