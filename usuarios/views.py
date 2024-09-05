from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from .models import CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model


def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def cadastro_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('usuarios:listar_usuarios')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

@user_passes_test(is_superuser)
def listar_usuarios(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})




def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login_usuario.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('index')


class LoginView(FormView):
    template_name = 'login_usuario.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


def user_menu(request):
    user = request.user
    return render(request, 'user_menu.html', {'user': user})


def return_index(request):
    return render(request, 'index.html')



def assign_superuser_group(user):
    superuser_group = Group.objects.get(name='SuperUser')
    user.groups.add(superuser_group)

def assign_limited_group(user):
    limited_group = Group.objects.get(name='LimitedUser')
    user.groups.add(limited_group)



@user_passes_test(lambda u: u.is_superuser)
def deletar_usuario(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, "Você não pode deletar seu próprio usuário.")
        return redirect('usuarios:listar_usuarios')

    user.delete()
    messages.success(request, f"Usuário {user.username} deletado com sucesso.")
    return redirect('usuarios:listar_usuarios')



