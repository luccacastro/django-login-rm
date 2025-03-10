import logging
from dal import autocomplete

from django.http import JsonResponse
from django.views.generic.edit import CreateView, View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.signing import Signer, BadSignature
from django.contrib.auth.views import LoginView

from .forms import AccountCreationForm
from .models import Member
from schools.models import School

signer = Signer()
logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("welcome")
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):

    def get(self, request):
        form = AccountCreationForm()
        return render(request, "registration/signup.html", {"form": form})

    def post(self, request):
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            self.send_confirmation_email(user)
            return redirect("validation_required")
        return render(request, "registration/signup.html", {"form": form})

    def send_confirmation_email(self, user):
        """Generate confirmation token and send activation email."""
        token = signer.sign(user.email)
        activation_link = self.request.build_absolute_uri(reverse("activate", args=[token]))

        subject = "Confirm Your Email"
        message = f"Hi {user.first_name},\n\nClick the link below to confirm your email:\n{activation_link}\n\nThank you!"
        
        # JUST SO YOU DON'T NEED TO ADD MAIL TRAP
        logging.error(f"ACTIVATION LINK: {activation_link}")

        send_mail(subject, message, "no-reply@ruthmiskin.com", [user.email])

class ActivateAccountView(View):
    """Handles email confirmation and displays an activation message."""

    def get(self, request, token):
        try:
            email = signer.unsign(token)
            user = User.objects.get(email=email)
            if user.member.user.is_active:
                return render(request, "activation/activation_success.html", {"message": "Your account is already activated."})
            else:
                user.is_active = True
                user.save()
                return render(request, "activation/activation_success.html", {"message": "Your account has been successfully activated. You can now log in."})
        except (User.DoesNotExist, BadSignature):
            return render(request, "activation/activation_failed.html", {"message": "Invalid or expired activation link."})

class SchoolAutocomplete(autocomplete.Select2QuerySetView):
    """Auxiliary view for django autocomplete light to easily fetch school data."""
    
    def get_queryset(self):
        qs = School.objects.filter(close_date__isnull=True).order_by("name")

        search_query = self.q
        if search_query:
            qs = qs.filter(name__icontains=search_query)

        return qs


def validation_required_view(request):
    return render(request, "registration/validation_required.html")
