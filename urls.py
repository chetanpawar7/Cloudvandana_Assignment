from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^depo/v1/register/$', views.RegisterApiView.as_view(), name='depo_register'),
    url(r'^depo/v1/userlist/$', views.UserListApiView.as_view(), name='User_list'),
    url(r'^depo/v1/login/$', views.LoginApiView.as_view(), name='depo_login'),
    url(r'^depo/v1/logout/$', views.LogOutView.as_view(), name='depo_logout'),
    url(r'^depo/v1/refresh_token/$', views.RefreshTokenView.as_view(), name='refresh_token'),
    url(r'^depo/v1/role_list/$', views.RoleListApiView.as_view(), name='role_list'),
    url(r'^depo/v1/test/$', views.TestApiView.as_view(), name='test'),
    url(r'^depo/v1/update/user/$', views.UpdateUserApiView.as_view(),name='update_user'),
    url(r'^depo/v1/admin_login/$', views.AdminLoginApiView.as_view(), name='admin_login'),
    url(r'^depo/v1/admin_login/$', views.AdminLoginApiView.as_view(), name='admin_login'),
    url(r'^depo/v1/reset_password/$', views.ResetPasswordApiView.as_view(), name='reset_password'),
    url(r'^depo/v1/reset_password_verify/$', views.ResetPasswordVerifyApiView.as_view(), name='reset_password_verify'),
]
