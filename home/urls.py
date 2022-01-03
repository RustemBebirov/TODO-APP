from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('detail/<int:pk>/',views.detail,name='detail_task'),
    path('update/<int:pk>/',views.update_task,name='update_task'),
    path('delete/<int:pk>/',views.delete_task,name='delete_task'),
    path('privacy/<int:pk>/',views.privacy_task,name='privacy_task'),
    path('share/<int:pk>/',views.share_task,name='share_task'),
    path('shared-tasks-list/',views.shared_task_list,name='shared_task_list'),
    path('delete_friend/<int:pk>/',views.delete_friend,name='delete_friend'),
    path('history/',views.history,name='history'),
]
