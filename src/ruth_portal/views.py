from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def root_redirect_view(request):
    if request.user.is_authenticated:
        return redirect("welcome") 
    return redirect("login")

@login_required 
def welcome_view(request):
    return render(request, "welcome.html")