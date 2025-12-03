from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from authy.views import UserProfile, EditProfile, get_followers, get_following

urlpatterns = [
    # Profile Section
    path('profile/edit', EditProfile, name="editprofile"),

    # User Authentication
    path('sign-up/', views.register, name="sign-up"),
    path('sign-in/', auth_views.LoginView.as_view(template_name="sign-in.html", redirect_authenticated_user=True), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(), name='sign-out'),
    #path('sign-out/', auth_views.LogoutView.as_view(template_name="sign-out.html"), name='sign-out'), # Ten nie działa
    path("followers/", get_followers, name="get_followers"),
    path("following/", get_following, name="get_following"),
]
 