from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from thumbs import ImageWithThumbsField
import os
from operator import itemgetter 
from itertools import groupby 

def modulos():
    list_modulos = ContentType.objects.all().order_by('app_label')
    modulos = ()
    for l in list_modulos:
        modulos = modulos + ((l.app_label, l.app_label),)
    
    # Cremover itens repetido de uma lista 
    modulo = list(map(itemgetter(0), groupby(modulos)))
    return modulo

class Modulo(models.Model):
    listmodulos = modulos()
    idmodulo = models.AutoField(primary_key=True)
    modulo = models.CharField("Modulo", max_length=200, choices=listmodulos)

    def __unicode__(self):
        return self.modulo
    
    
def upload_to_foto_topobg(instance, name):
    img = str(instance.img_topobg)
    if img != '':
        nome = 'topo_bg'
    extensao = os.path.splitext(name)[-1]
    return os.path.join('images_portal/', '%s%s' % (nome, extensao))

def upload_to_foto_img_topo(instance, name):
    img = str(instance.img_topo)
    if img != '':
        nome = 'head_bg'
    extensao = os.path.splitext(name)[-1]
    return os.path.join('images_portal/', '%s%s' % (nome, extensao))


def upload_to_foto_img_logo(instance, name):
    img = str(instance.img_topobg)
    if img != '':
        nome = 'logo'
    extensao = os.path.splitext(name)[-1]
    return os.path.join('images_portal/', '%s%s' % (nome, extensao))


def upload_to_foto_img_menufundo(instance, name):
    img = str(instance.img_topobg)
    if img != '':
        nome = 'menu_bg'
    extensao = os.path.splitext(name)[-1]
    
    return os.path.join('images_portal/', '%s%s' % (nome, extensao))

class Layout(models.Model):
    idlayout = models.AutoField(primary_key=True)
    #topo_bg.png
    img_topobg = ImageWithThumbsField(verbose_name="Background do topo ", upload_to=upload_to_foto_topobg, null=True, blank=True,)
    #head_bg.png
    img_topo = ImageWithThumbsField(verbose_name="Imagem topo", upload_to=upload_to_foto_img_topo, null=True, blank=True,)
    #logo.jpg
    img_logo = ImageWithThumbsField(verbose_name="Logo ", upload_to=upload_to_foto_img_logo, null=True, blank=True,)
    #menu_bg.png
    img_menufundo = ImageWithThumbsField(verbose_name="Background do menu", upload_to=upload_to_foto_img_menufundo, null=True, blank=True,)
        
    
    """ funcao que coloca as imagens no campo img_foto na consulta """
    def topobg(self):
        foto = str(self.img_topobg)
        img = '<img style="width:100px;heigth:100px" src="/espiga/media/' + foto + '"/>'       
        return img
    topobg.allow_tags = True
    topobg.short_description = u'Topo Background'
    
    def topo(self):
        foto = str(self.img_topo)
        img = '<img style="width:100px;heigth:100px" src="/espiga/media/' + foto + '"/>'
        return img
    topo.allow_tags = True
    topo.short_descritpion = u'Topo'
    
    def logo(self):
        foto = str(self.img_logo)
        img = '<img style="width:100px;heigth:100px" src="/espiga/media/' + foto + '"/>'
        return img
    logo.allow_tags = True
    logo.short_descritpion = u'Logo'
    
    def menufundo(self):
        foto = str(self.img_menufundo)
        img = '<img style="width:100px;heigth:100px" src="/espiga/media/' + foto + '"/>'
        return img
    menufundo.allow_tags = True
    menufundo.short_descritpion = u'Fundo_do_menu'
        
    '''def save(self):
        super(Layout,self).save()
        imgtopobg_old = str(self.img_topobg)
        #imgotopo = str(self.img_topo)
        #imglogo = str(self.img_logo)
        #imgmenufundo = str(self.img_menufundo)
        if imgtopobg_old != '':
            ftpbg = str(imgtopobg_old).split('/')
            raise Exception(ftpbg)
            nome = ftpbg[0]+'/topo_bg.png'
            self.img_topobg = nome
            super(Layout, self).save()
            os.remove(settings.MEDIA_ROOT+'/'+imgtopobg_old)

    
    
       def save(self, force_insert=False, force_update=False):
        super(Layout,self).save(force_insert,force_update)
        imgtopobg_old = str(self.img_topobg)
        #imgotopo = str(self.img_topo)
        #imglogo = str(self.img_logo)
        #imgmenufundo = str(self.img_menufundo)
        if imgtopobg_old != '':
            
            ftpbg = str(imgtopobg_old).split('/')
            nome = ftpbg[0]+'/topo_bg.png'
            
            self.img_topobg = nome
            #raise Exception(imgtopobg_old)
            #raise Exception(os.path.join('images_portal/','%s'%(nome)))
            #os.remove(settings.MEDIA_ROOT+'/'+imgtopobg)
            super(Layout, self).save()
            os.remove(settings.MEDIA_ROOT+'/'+imgtopobg_old)
            #os.path.join('images_portal/','%s'%(imgtopobg_old))
        else: 
            super(Layout, self).save(force_insert, force_update)
        
            raise Exception(ftpbg)'''

class Menu(models.Model):
    list_tipo = (('1','Horizontal'), ('2','Vertical'), ('3','Rodape'))
    nome = models.CharField("Nome", max_length=250)
    tipo = models.CharField("Tipo de Menu", max_length=1, choices=list_tipo,)
    submenu = models.ForeignKey('Menu',blank = True,null = True )
  
    def __unicode__(self):
        return self.nome
    
    def itens(self):
        item = Item_Menu.objects.filter(menu = self).filter(subitem = None)
        return item
    
    class Meta:
        ordering = ('id',)
        verbose_name = "Menu"
        
class Item_Menu(models.Model):
    menu = models.ForeignKey(Menu)
    nome = models.CharField("Titulo", max_length=250)
    url = models.CharField("Url", max_length=250,blank = True,null = True,default = "#")
    subitem = models.ForeignKey('Item_Menu',blank = True,null = True )
   
    def __unicode__(self):
        return self.nome      
    
    def subitems(self):
        return Item_Menu.objects.filter(subitem = self) 
        
    class Meta:
        ordering = ('id',)

