from django.urls import path
from .views import user_login, user_profile, registr_user, SignUpView, editUser, EditUser
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,\
    PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    #path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('change-password-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/',PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('dashboard/', user_profile, name='user_profile'),
    path('sigin-up/', registr_user, name='sign-up'),
    # path('edit/', EditUser.as_view(), name='account_edit'),
    path('edit/', editUser, name='account_edit'),
]