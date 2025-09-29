from django.urls import path
from . import views
from .password_reset_views import password_reset_request, password_reset_confirm, password_reset_validate_token

urlpatterns = [
    path("accounts/", views.AccountListCreate.as_view(), name="account-list"),
    path("accounts/<int:pk>/", views.AccountRetrieveUpdate.as_view(), name="account-detail"),
    path("accounts/delete/<int:pk>/", views.AccountDelete.as_view(), name="delete-account"),
    path("accounts/<int:pk>/fetch-favicon/", views.fetch_account_favicon, name="fetch-account-favicon"),
    
    # Authentication endpoints
    path("login/", views.login_view, name="login"),
    path("user/register/", views.CreateUserView.as_view(), name="register"),
    
    # Password reset endpoints
    path("password-reset/", password_reset_request, name="password-reset-request"),
    path("password-reset/confirm/", password_reset_confirm, name="password-reset-confirm"),
    path("password-reset/validate-token/", password_reset_validate_token, name="password-reset-validate-token"),
    
    # Favicon endpoints
    path("fetch-favicon/", views.fetch_favicon, name="fetch-favicon"),
]
