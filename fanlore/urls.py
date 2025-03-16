from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='content_list'),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/<int:user_id>/", views.ProfileView.as_view(), name="friend-profile"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name="signin"),
    path('friends/', views.FriendListView.as_view(), name="friends-list"),
    path("friends/add/<int:user_id>/", views.AddFriendView.as_view(),
         name="add-friend"),
    path("friends/remove/<int:user_id>/", views.RemoveFriendView.as_view(),
         name="remove-friend"),
    path("profile_edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    path('upload/', views.ContentUploadView.as_view(), name='upload_content'),
    path('post/<uuid:pk>/', views.ContentDetailView.as_view(), name='view_post'),
    path('delete_content/<uuid:content_id>/', views.ContentDeleteView.as_view(), name='content_delete'),
]
