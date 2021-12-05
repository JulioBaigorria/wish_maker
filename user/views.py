# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import auth
from user import models


def main(request):
    return render(request, 'main.html', context={"respuesta": "respuesta", })


def dashboard(request):
    username = request.session['username']
    userobj = models.User.objects.get(username=username)
    user_wishes = userobj.items.all()
    all_wishes = models.Wish.objects.all()
    for wish in user_wishes:
        all_wishes = all_wishes.exclude(id=wish.id)
    return render(request, 'dashboard.html', context={"myitems": user_wishes, "allwishes": all_wishes})

def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = None
        try:
            user = models.User.objects.get(username=username)
        except Exception as e:
            messages.error(request, "No se encuentra el usuario", extra_tags="login")
            return redirect('/')
        if password != user.password:
            messages.error(request, "Contraseña incorrecta", extra_tags="login")
            return redirect('/')
        request.session['username'] = username
    return redirect('../../dashboard/')


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        date_hired = request.POST['date_hired']
        user = None
        try:
            user = models.User.objects.get(username=username)
            messages.error(request, "ya existe el usuario", extra_tags="register")
            return redirect('/')
        except Exception as e:
            print(e)

        if len(name) < 3 or len(username) < 3:
            messages.error(request, "Usuario o nombre menor a 3 digitos", extra_tags="register")
            return redirect('/')
        print(password1.isalpha())
        if password1 != password2 or len(password1) < 8 or not password1.isalpha:
            messages.error(request, "Problema en la contraseña", extra_tags="register")
            return redirect('/')
        messages.success(request, "Usuario registrado exitosamente", extra_tags="register")

        models.User.objects.create(name=name, username=username, password=password1, date_hired=date_hired)
        user = models.User.objects.get(username=username)
        return redirect('/')

def wish_detail(request,id):
    wish = models.Wish.objects.get(id=id)
    return render(request, 'wish_items.html', context={"wish":wish})


def wish_item(request):
    if request.method == 'POST':
        item = request.POST['item']
        if len(item) < 3 or not item:
            messages.error(request, "Nombre invalido", extra_tags="register")
            return redirect('../../wish_items/create/')
        username = request.session['username']
        user = models.User.objects.get(username=username)
        models.Wish.objects.create(name=item, added_by=user)

        wish = models.Wish.objects.get(name=item)
        user.items.add(wish)
        return redirect('/dashboard')

    return render(request, 'wi_create.html', context={"asd": "asd"})


def remove_wish(request, id):
    username = request.session['username']
    user = models.User.objects.get(username=username)
    favorite = models.Wish.objects.get(id=id)
    user.items.remove(favorite)
    return redirect('/dashboard')


def delete_wish(request, id):
    wish = models.Wish.objects.get(id=id)
    wish.delete()
    return redirect('/dashboard')


def add_wish(request, id):
    wish = models.Wish.objects.get(id=id)
    username = request.session['username']
    user = models.User.objects.get(username=username)
    user.items.add(wish)
    return redirect('/dashboard')
