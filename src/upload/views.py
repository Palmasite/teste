from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings 


from upload.models import *


def arquivos(request,idgaleria = None,nome_galeria = None):

    if idgaleria:
        lista_galeria  = Galeria.objects.filter(pk = idgaleria)
    else:
        lista_galeria  = Galeria.objects.all()
    
   
    doc = settings.MEDIA_URL +'images_portal/upload/word.png'
    excel = settings.MEDIA_URL +'images_portal/upload/excel.png'
    pdf  = settings.MEDIA_URL +'images_portal/upload/pdf.png'
    point = settings.MEDIA_URL +'images_portal/upload/powerpoint.png'
    
    
    
    arquivos = Arquivo.objects.all()
    
    lista_arquivo_mes = arquivos.dates('dat_publicacao','month').reverse()

    lista_arquivo = ()
     
    for a in arquivos:
        if a.vch_arquivo:
            #raise Exception(a.vch_arquivo)
            extensao = str(a.vch_arquivo).split('.')[-1]
            
            if extensao == 'doc' or extensao == 'docx':
                lista_arquivo = lista_arquivo + ((a.int_idarquivo,a.vch_titulo,a.txt_resumo,a.vch_arquivo,doc,a.galeria.idgaleria,a.dat_publicacao),)
                
            if extensao == 'pdf':
                lista_arquivo = lista_arquivo + ((a.int_idarquivo,a.vch_titulo,a.txt_resumo,a.vch_arquivo,pdf,a.galeria.idgaleria,a.dat_publicacao),)
            if extensao == 'xls' or extensao == 'xlsx':
                lista_arquivo = lista_arquivo + ((a.int_idarquivo,a.vch_titulo,a.txt_resumo,a.vch_arquivo,excel,a.galeria.idgaleria,a.dat_publicacao),)
       

    return render_to_response('arquivos.html', locals(), context_instance=RequestContext(request))



