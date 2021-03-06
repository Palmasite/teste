# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from django.utils import simplejson
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.redirects.models import Redirect
from django.core import serializers
from django.utils import simplejson

from urllib2 import HTTPRedirectHandler

from datetime import datetime
import datetime

from link.models import Link, Categoria
from noticia.models import Noticia
from bancoimagem.models import BancoImagem, Galeria
from paginasstaticas.models import Pagina, Categoria
from video.models import Video
from noticia.models import Noticia
from agenda.models import Eventos
from enquete.models import Enquete, Escolha
from publicidade.models import Publicidade



def index(request):
    #verifica se ta authenticado
    #if request.user.is_authenticated():
     #    auth = request.user
         
   
    
    #lista galeria
    lista_galeria = Galeria.objects.all()[:3]
    lista_imagem = BancoImagem.objects.all()
    
    
    #noticias_destque
    noticias_destaque = Noticia.objects.filter(boo_ativo=True).filter(boo_destaque=True);
    
    #lista de noticias       
    outras_noticias = Noticia.objects.filter(boo_ativo=True).filter(boo_destaque=False)
   
    #eventos
    ultimos_eventos = Eventos.objects.filter(inicio__gt=datetime.date.today())
    
    
    # Menu Vertical
    categorias = Categoria.objects.all()
    paginas = Pagina.objects.all()

    #lista Links
    
    link_servico_destaque = Link.objects.filter(boo_destaque = True).filter(categoria = 3)[:6]# para servicos
    link_rapidos = Link.objects.filter(categoria = 4) #links rapidos
    link_rapidos_destaque = Link.objects.filter(categoria = 1) #links rapidos destaque

    
    
    
    
    
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def logar(request):
    
    mimetype = 'application/javascript'  
    
    user = request.POST['username']
    passw = request.POST['password']
    message = ""        
    user_login = authenticate(username=user, password=passw)    
    if user_login is not None:
        if user_login.is_active:
            retorno = {'status':'ok', 'message':'<span>Seja bem vindo : <strong>' + user_login.username + '</strong></span>'}
            request.session['username'] = user
            login(request, user_login)
        else:
            retorno = {'status':'no', 'message':'<span style="color:#A20000">usario não ativo<span>'}
    else:
        retorno = {'status':'no', 'message':'<span style="color:#A20000">Usuário ou senha inválido<span>'}
    
    return HttpResponse(simplejson.dumps(retorno), mimetype)

def sair(request):
    logout(request)
    return redirect('/index')
