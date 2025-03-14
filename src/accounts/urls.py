from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, SchoolAutocomplete, ActivateAccountView, validation_required_view, CustomLoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path("activate/<str:token>/", ActivateAccountView.as_view(), name="activate"),
    path("school-autocomplete/", SchoolAutocomplete.as_view(), name="school-autocomplete"),
    path("validation-required/", validation_required_view, name="validation_required"),

    path('login/', CustomLoginView.as_view(next_page='welcome'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path(
        "password_reset/", 
        auth_views.PasswordResetView.as_view(template_name="password_reset/password_reset_form.html"), 
        name="password_reset"
    ),
    path(
        "password_reset/done/", 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset/password_reset_done.html"), 
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/", 
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_confirm.html"), 
        name="password_reset_confirm"
    ),
    path(
        "reset/done/", 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset/password_reset_complete.html"), 
        name="password_reset_complete"
    ),
]

