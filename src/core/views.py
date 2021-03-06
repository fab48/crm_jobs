# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, get_object_or_404
from core.models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import operator


#Esta funcion se encarga de buscar las ofertas que se reciben a traves del request
def buscar_ofertas(request):
    tecnologias = Tecnologia.objects.all()
    niveles = NIVELES_DESARROLLADOR

    try:
        busqueda = request.POST['palabras'].replace(" ", "").split(",")
        tecnologia = request.POST['tecnologia']
        nivel = request.POST['nivel']
        print tecnologia
        ofertas = Oferta.objects.filter(reduce(operator.or_, ((Q(funciones__contains=x) | Q(empresa__contains=x)) for x in busqueda)) & Q(tecnologias__nombre=tecnologia))

    except Exception, e:
        print e
        ofertas = Oferta.objects.all()
    paginator = Paginator(ofertas, 25)
    try:
        pagina = request.GET.get('page')
    except:
        pagina = 1
    try:
        ofertas = paginator.page(pagina)
    except:
        ofertas = paginator.page(1)

    return render(request, 'lista_ofertas.html', {"ofertas": ofertas, 'origen': "Resultados de la busqueda", 'tecnologias': tecnologias, 'niveles': niveles})


#Esta funcion se encarga de enviar la oferta seleccionada de manera individual
def ver_oferta(request):
    try:
        identificador = request.GET['id']
        oferta = Oferta.objects.get(id=identificador)
        ofertas_similares = Oferta.objects.get(id=identificador).tags.similar_objects()
    except:
        oferta = None
    return render(request, 'oferta.html', {"oferta": oferta, "similares": ofertas_similares})

#Esta funcion se encarga de vincular al usuario a una oferta

@login_required(login_url="/login/")
def vincular_oferta(request):
    id_usuario = request.user.id
    id_oferta = request.POST['id_oferta']
    info_oferta = Oferta.objects.get(id=id_oferta)
    usuario = User.objects.get(id=id_usuario)
    #aplicante es un objeto tipo desarrollador
    aplicante = Desarrollador.objects.get(user=usuario)
    oferta = Oferta.objects.get(id=id_oferta)
    oferta.aplicantes.add(aplicante)
    oferta.save()
    return render(request, 'oferta.html', {"mensaje":"Aplicacion correcta", "msn":True, "oferta":info_oferta})
    print(oferta)

#login de usuarios
def login_user(request):
    if request.method == 'GET':
        return render(request, "login.html")
    else:
        username = request.POST['username']
        password = request.POST['password']
        print("user: "+username+" pass: "+password)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('landing')
            else:
                print("error usuario inactivo")
                return render(request, 'login.html')
        else:
            print("error asdf")
            return render(request, 'login.html')

#logout se encarga de finalizar la sesion del usuario y redirigirlo a la pagina principal
def logout_user(request):
    logout(request)
    return redirect('/')

#Esta funcion se encarga de retornar el perfil adecuado a mostrar en cada usuario
"""
Esta funcion recibe como parametro un mensaje en el get de la siguiente manera en ejemplo:
http://localhost:8000/perfil/user_id
"""
def perfil(request, user_id):
    usuario = User.objects.get(id=int(user_id))
    
    if hasattr(usuario, 'desarrollador'):
        if int(user_id) == request.user.id:
            return render(request, 'perfil_dev_priv.html', { "developer" : usuario.desarrollador })
        return render(request, 'perfil_dev_pub.html', { "developer" : usuario.desarrollador })
    elif hasattr(usuario, 'empresa'):
        if int(user_id) == request.user.id:
            return render(request, 'perfil_empresa_priv.html', {"empresa": usuario.empresa})
        return render(request, 'perfil_empresa_pub.html', { "empresa" : usuario.empresa })
    else:
        return rendirect('home')

def manejo_cuentas(request):
    if request.method == 'GET':
        return mostrar_cuentas(request)
    elif request.method == 'POST':
        return enlazar_cuentas

def mostrar_cuentas(request):
    d=Desarrollador.objects.get(user__id=request.user.id)
    github=d.perfil_github
    bitbucket=d.perfil_bitbucked
    linkedin=d.perfil_linkedin
    twitter=d.perfil_twitter
    return render(request, 'enlazar.html',{'github':github,'linkedin':linkedin,'twitter':twitter,'bitbucket':bitbucket})

def enlazar_cuentas(request):
    d=Desarrollador.objects.get(user__id=request.user.id)
    d.perfil_github = request.POST.get('github')
    d.perfil_bitbucked = request.POST.get('bitbucket')
    d.perfil_linkedin = request.POST.get('linkedin')
    d.perfil_twitter = request.POST.get('twitter')
    d.save()
    
    return render(request, 'home.html')

def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {'tecnos': Tecnologia.objects.all(), 
            'levels': NIVELES_DESARROLLADOR})

    elif request.method == 'POST':

        nombre = request.POST['firstname']
        apellido = request.POST['lastname']
        password = request.POST['password']
        email = request.POST['email']
        telefono = request.POST['telephone']
        tecnologias = {}

        # filtrar tecnologias desde el request
        habs = filter( (lambda key: 'tecno-' in  key or 'level-' in key), request.POST.keys())
        indexes = [x.replace('level-', '') for x in habs if x.startswith('level-')]

        for index in indexes:
            tecnologias[request.POST['tecno-'+index]] = request.POST['level-'+index]

        perfil = Desarrollador()

        perfil.user = User.objects.create_user(username=email, password=password)
        perfil.user.firstname = nombre
        perfil.user.lastname = apellido
        perfil.user.save()

        perfil.telefono = telefono
        perfil.save()
        
        #guardar tecnologias
        for tecno, nivel in tecnologias.items():
            TecnologiaDesarrollador(tecnologia=Tecnologia.objects.get(nombre=tecno),
                    desarrollador=perfil, nivel=nivel).save()

        return redirect('/login')
