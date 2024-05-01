from django.urls import path
from . import views
from django.conf import settings # access to settings.py file
from django.conf.urls.static import static # access to static files

urlpatterns = [
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.LogoutUser, name = 'logout'),

    path('register/', views.registerUser, name = 'register'),
    path('profile<str:pk>/', views.userProfile, name = 'user-profile'),
    path('update-user/', views.updateUser, name="edit-user"),
    
    path('', views.home, name = 'home'),
    path('room/<str:pk>', views.room, name = 'room'),
    
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),

    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity")
]

# for user uploaded profile images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# set the url and get the file from media root