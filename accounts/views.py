from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Bem-vindo ao sistema de gestão!")
            return redirect("listar_ocorrencias")
        
        else:
            messages.get_messages(request).used = True
            messages.error(request, "Usuário ou senha inválidos. Tente novamente.")

    return render(request, "accounts/login.html")


# ✅ Confirme que essa função está no arquivo antes de tentar importá-la!
def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu do sistema.")
    return redirect("login")
