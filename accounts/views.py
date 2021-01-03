from django.contrib.auth.decorators import login_required

from .models import User
from products.models import Group
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        User.objects.create_user(request.POST.get('username', ''),
                                 password=request.POST.get('password1', ''),
                                 email=request.POST.get('email', ''))
        return redirect('/')
    return render(request, 'registration/signup.html')


@login_required
def user_profile(request, username):
    groups = Group.objects.all()
    if request.method == 'POST':
        form_dict = dict(request.POST)
        for key in form_dict.keys():
            val = form_dict[key]
            if isinstance(val, list):
                form_dict[key] = val[0]
        form_dict.pop('csrfmiddlewaretoken')
        print(form_dict)
        User.objects.filter(username=username).update(**form_dict)
        print(request.user)
    return render(request, 'registration/profile.html', {'user': request.user, 'groups': groups})
