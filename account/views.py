from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.auth.models import User
from .form import loginForm, RegistrForm, ProfilEditForm, UserEditForm
from .models import ProfileUser

def user_login(request):
    if request.method=='POST':
        form=loginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request,
                              username=data['username'],
                              password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Muvaffaqiyatli login amalga oshirildi")
                else:
                    return HttpResponse("Hisob faol emas")
            else:
                return HttpResponse("Hisob mavjud emas")
        else:
            return HttpResponse("Maydonlarni to'ldiring")
    else:
        form=loginForm()
        context={
            'form' : form,
        }
    return render(request, 'account/login.html', context=context)


@login_required
def user_profile(request):
    user=request.user
    profile=ProfileUser.objects.get(user=user)


    context={
        'user':user,
        'profile':profile,
    }

    return render(request, 'pages/user_profile.html', context=context)

def registr_user(request):
    if request.method=='POST':
        user_form=RegistrForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(
                user_form.cleaned_data['password']
            )
            user.save()
            ProfileUser.objects.create(user=user)
            context= {
                'user':user,
            }
            return render(request, 'registration/registr_done.html', context=context)
    else:
        user_form=RegistrForm()
        context={
            'form':user_form,
        }
    return render(request, 'registration/registr.html', context=context)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registr.html'

@login_required
def editUser(request):
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user, data=request.POST)
        profile_form=ProfilEditForm(instance=request.user.profileuser, data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfilEditForm(instance=request.user.profileuser)
    return render(request, 'registration/account_edit.html', context={"user_form": user_form, "profile_form":profile_form})

class EditUser(LoginRequiredMixin, View):

    def get(self,request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfilEditForm(instance=request.user.profileuser)
        return render(request, 'registration/account_edit.html',
                  context={"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfilEditForm(instance=request.user.profileuser, data=request.POST,
                                      files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect('user_profile')

