from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="login")
def greet_user(request):
    username = request.user.username
    return render(request, 'users/hello.html', {'username': username})
