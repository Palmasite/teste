# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

def jornal(request):
    a = "a"
    
    return render_to_response('jornal/Default.html', locals(), context_instance=RequestContext(request))

def papo(request):


    return render_to_response('papo_legal/Default.html', locals(), context_instance=RequestContext(request))

       
