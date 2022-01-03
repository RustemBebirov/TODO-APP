from django.urls import path
from . import views

urlpatterns = [
    path('',views.trash_list,name='trash_list'),
    path('save-task/<int:pk>/',views.save_task,name='save_task'),
    path('task-done/<int:pk>/',views.done_task,name='done_task'),

]
