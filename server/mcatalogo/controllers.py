import base64
from tornado.gen import coroutine

from server.mcatalogo.models import Catalogo
from .managers import *
from ..usuarios.managers import *
from ..operaciones.managers import *
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from ..common.controllers import CrudController, SuperController, ApiController
from xhtml2pdf import pisa
import requests
import os.path
import dropbox
from PIL import Image
import io
from datetime import date


FECHA_HOY = date.today()
class Report:
    def html_to_pdf(self, sourceHtml, nombre):
        outputFilename = 'server/common/resources/downloads/' + nombre

        resultFile = open(outputFilename, "w+b")
        pisaStatus = pisa.CreatePDF(
            sourceHtml,
            dest=resultFile)
        resultFile.close()

        return pisaStatus.err
global api
#afuera de la empresa Tupperware
api ="https://181.115.203.250:5050/api/"
#dentro de la empresa Tupperware
#api = "http://192.168.1.200:4040/api/"

class CatalogoController(CrudController):
    manager = CatalogoManager
    html_index = "mcatalogo/views/catalogo/index.html"
    html_table = "mcatalogo/views/catalogo/table.html"
    routes = {
        '/catalogo': {'GET': 'index', 'POST': 'table'},
        '/catalogo_insert': {'POST': 'insert'},
        '/catalogo_update': {'PUT': 'edit', 'POST': 'update'},
        '/catalogo_delete': {'POST': 'delete'},
        '/catalogo_update_paginas': {'POST': 'update_paginas'},
        '/catalogo_filter': {'POST': 'catalogo_filter'},
    }

    def get_extra(self):
        aux = super().get_extra_data()
        aux['catalogo'] = CatalogoManager(self.db).obtener_registro()
        aux['catalogos'] = CatalogoManager(self.db).get_all()
        aux['catalogounico'] = CatalogoManager(self.db).get_all_distinct()
        id = 0
        for a in aux['catalogo']:
            id = a.id
        aux['catalogo'] = id
        return aux

    def index(self):
        self.set_session()
        self.verif_privileges()
        usuario = self.get_user()
        if usuario.id == 1:
            result = self.manager(self.db).list_all()
        else:
            a = self.manager(self.db).get_cat_by_fecha_actual(FECHA_HOY)
            if a == None:
                result = self.manager(self.db).listar_vacio()
            else:
                result = self.manager(self.db).Mostrar_catalogo_actual(FECHA_HOY)
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        for a in result['objects']:
            a.FechaFinal = a.FechaFinal.strftime("%d/%m/%Y")
            a.FechaInicio = a.FechaInicio.strftime("%d/%m/%Y")
        self.render(self.html_index, **result)
        self.db.close()

    def insert(self):
      self.set_session()
      diccionary = json.loads(self.get_argument("object"))
      diccionario = {'numero': int(diccionary['NumeroPaginas'])}
      diccionary['user'] = self.get_user_id()
      ip = diccionary['ip']
      diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
      diccionary['TipoProducto'] = 2
      diccionary['Estado'] = bool(diccionary['Estado'])
      if "archivo" in self.request.files:
          fileinfo = self.request.files["archivo"][0]
          diccionary['portada'] = self.manager(self.db).imagen(fileinfo)
      else:
        link = ' '
        diccionary['portada'] = link
      objeto = self.manager(self.db).entity(**diccionary)
      CatalogoManager(self.db).insert(objeto)
      a = self.get_extra()
      diccionario['user'] = self.get_user_id()
      diccionario['ip'] = diccionary['ip']
      diccionario['fkcatalogo'] = int(a['catalogo'])
      diccionario['inicio'] = 0
      PaginaController.insertarPagina(self, diccionario)
      self.respond(response=0,success=True, message='Insertado correctamente.')
      self.db.close()

    def update(self):
      self.set_session()
      diccionary = json.loads(self.get_argument("object"))
      ip = diccionary['ip']
      diccionary['ip']  = self.manager(self.db).obtener_ip(ip)
      diccionary['user'] = self.get_user_id()
      if "archivo" in self.request.files:
          fileinfo = self.request.files["archivo"][0]
          diccionary['portada'] = self.manager(self.db).imagen(fileinfo)
      diccionary['Estado'] = bool(diccionary['Estado'])
      objeto = self.manager(self.db).entity(**diccionary)
      pagina = CatalogoManager(self.db).validarPagina(objeto);
      if pagina['paginas'] > 0:
        diccionario = {'numero': pagina['paginas']}
        a = diccionary['id']
        diccionario['user'] = self.get_user_id()
        diccionario['ip'] = self.request.remote_ip
        diccionario['fkcatalogo'] = a
        diccionario['inicio'] = pagina['numero']
        PaginaController.insertarPagina(self, diccionario)
      elif pagina['paginas'] < 0:
          diccionario = {'numero': pagina['paginas']}
          a = diccionary['id']
          diccionario['user'] = self.get_user_id()
          diccionario['ip'] = self.request.remote_ip
          diccionario['fkcatalogo'] = a
          diccionario['inicio'] = pagina['numero']
          PaginaController.editar_Pagina(self, diccionario)
      CatalogoManager(self.db).update(objeto)
      self.respond(response= 0,success=True, message='Modificado correctamente.')
      self.db.close()

    def update_paginas(self):
      self.set_session()
      diccionary = json.loads(self.get_argument("object"))
      diccionary['user'] = self.get_user_id()
      ip = diccionary['ip']
      diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
      if "archivo_paginas" in self.request.files:
          fileinfo = self.request.files["archivo"][0]
          diccionary['portada'] = self.manager(self.db).imagen(fileinfo)
      objeto = PaginaManager(self.db).entity(**diccionary)
      ProductoManager(self.db).update(objeto)
      self.respond(success=True, message='Modificado correctamente.')

    def delete(self):
      try:
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        CatalogoManager(self.db).delete(diccionary['id'], diccionary['user'], diccionary['ip'],
                                           diccionary['enabled'])

        PaginaController.deleteCatalogoPagina(self, diccionary['id'], diccionary)
        self.respond(success=True, message='Eliminado correctamente.')
      except Exception as e:
        print(e)
        self.respond(response="No existe", success=False, message="Not Found")
      self.db.close()

    def catalogo_filter(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        gestion = diccionary['gestion']
        indicted_object = CatalogoManager(self.db).get_all_cat_by_gestion(gestion)
        response = []
        for cat in indicted_object:
            dic = dict(id=cat.id,
                       Gestion=cat.Gestion,
                       FechaInicio=str(cat.FechaInicio),
                       FechaFinal=str(cat.FechaFinal),
                       Numerocatalogo=cat.Numerocatalogo,
                       NumeroPaginas=cat.NumeroPaginas,
                     )
            response.append(dic)
        self.respond(response=response, success=True, message='Catálogo de la gestión '+str(gestion))
        self.db.close()


class PaginaController(CrudController):
    manager = PaginaManager
    html_index = "mcatalogo/views/pagina/index.html"
    html_table = "mcatalogo/views/pagina/table.html"
    routes = {
        '/pagina': {'GET': 'index', 'POST': 'table'},
        '/pagina_insert': {'POST': 'insert'},
        '/pagina_update': {'PUT': 'edit', 'POST': 'update'},
        '/pagina_delete': {'POST': 'delete'},
        '/pagina_search': {'POST': 'pagina_search'},
        '/pagina_cat_filter': {'POST': 'pagina_cat_filter'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['catalogos'] = CatalogoManager(self.db).get_all()
        aux['producto'] = ProductoManager(self.db).get_all()
        aux['catalogounico'] = CatalogoManager(self.db).get_all_distinct()
        return aux

    def pagina_search(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        result = self.manager(self.db).list_all()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def edit(self):
      self.set_session()
      self.verif_privileges()
      ins_manager = self.manager(self.db)
      diccionary = json.loads(self.get_argument("object"))
      indicted_object = ins_manager.obtain(diccionary['id'])
      producto = ProductoManager(self.db).get_producto(diccionary['id'])
      if len(ins_manager.errors) == 0:
        self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
      else:
        self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
      self.db.close()

    def index(self):
        self.set_session()
        self.verif_privileges()
        usuario = self.get_user()
        if usuario.id == 1:
            result = self.manager(self.db).list_all()
        else:
            cat = CatalogoManager(self.db).get_cat_by_fecha_actual(FECHA_HOY)
            if (cat != None):
                result = self.manager(self.db).list_all_pagina_index(cat.id)
            else:
                result = self.manager(self.db).listar_vacio()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def editar_Pagina(self,objeto):
        numero = objeto['numero']
        i = objeto['inicio']+1
        catalogo = objeto['fkcatalogo']
        pagina = PaginaManager(self.db).listar_paginas(catalogo)
        log = 0
        for pag in pagina['objects']:
            log+=1
        log = log+numero
        for pag in pagina['objects']:
            if pag.numero > log:
                pag.enabled = False
                pag.fkcatalogo = None
                PaginaManager(self.db).editar_paginas(pag)
        print("Programa terminado")


    def insertarPagina(self,objeto):
        numero = objeto['numero']
        i = objeto['inicio']+1
        numero = numero + i-1
        a = PaginaManager(self.db).insertar_pagina(objeto,i,numero)


    def deleteCatalogoPagina(self, idCatalogo, diccionary):
        listaPagina = PaginaManager(self.db).get_all_by_id(idCatalogo)
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        print(listaPagina)
        # print(listaPagina[0].id)
        if len(listaPagina) > 0:
          for i in listaPagina:
            PaginaManager(self.db).delete(i.id, diccionary['user'], diccionary['ip'], False)
        print("ok")


    def insert(self):
      self.set_session()
      diccionary = json.loads(self.get_argument("object"))
      catalogo = diccionary['fkcatalogo']
      ip = diccionary['ip']
      diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
      diccionary['user'] = self.get_user_id()
      if "archivo" in self.request.files:
          fileinfo = self.request.files["archivo"][0]
          diccionary['portada'] = self.manager(self.db).imagen(fileinfo)
      else:
        link = ' '
        diccionary['portada'] = link
      objeto = self.manager(self.db).entity(**diccionary)
      PaginaManager(self.db).insert(objeto)
      self.respond(response=0 ,success=True, message='Insertado correctamente.')
      self.db.close()

    def update(self):
      self.set_session()
      diccionary = json.loads(self.get_argument("object"))
      diccionary['user'] = self.get_user_id()
      ip = diccionary['ip']
      diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
      if "archivo" in self.request.files:
          fileinfo = self.request.files["archivo"][0]
          diccionary['portada'] = self.manager(self.db).imagen(fileinfo)
      pagina = self.manager(self.db).validar(diccionary)
      diccionary['fkcatalogo'] = pagina
      objeto = self.manager(self.db).entity(**diccionary)
      PaginaManager(self.db).update(objeto)
      orden = diccionary['producto']
      # se encarga de colocar orden a los productos por el id 
      if (len(orden)>0):
          for producto in orden:
              dic_producto = dict()
              dic_producto['id'] = producto['id']
              dic_producto['orden'] = producto['orden']
              dic_producto['user'] = self.get_user_id()
              dic_producto['ip'] = self.request.remote_ip
              objeto = ProductoManager(self.db).entity(**dic_producto)
              ProductoManager(self.db).update(objeto)
      self.respond(response=0, success=True, message='Modificado correctamente.')
      self.db.close()

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            ip = diccionary['ip']
            diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
            PaginaManager(self.db).delete(diccionary['id'], diccionary['user'], diccionary['ip'],
                                               diccionary['enabled'])
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response="No existe", success=False, message="Not Found")
        self.db.close()

    def pagina_cat_filter(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        id_catalogo = diccionary['id_catalogo']
        cat = CatalogoManager(self.db).get_by_id(id_catalogo)
        indicted_object = PaginaManager(self.db).get_all_paginas_by_catalogo(id_catalogo)
        response = []
        for pagina in indicted_object:
            dic = dict(id=pagina.id,
                       numero=pagina.numero,
                       portada=pagina.portada,
                       fkcatalogo=pagina.fkcatalogo,
                     )
            response.append(dic)
        catalogo = dict(
            id=cat.id,
            gestion=cat.Gestion,
            fechainicio=str(cat.FechaInicio),
            fechafinal=str(cat.FechaFinal),
            numerocatalogo=cat.Numerocatalogo,
            numeropaginas=cat.NumeroPaginas
        )
        response.append(catalogo)
        self.respond(response=response, success=True, message='Páginas del catálogo.')
        self.db.close()

class ProductoController(CrudController):
    manager = ProductoManager
    html_index = "mcatalogo/views/producto/index.html"
    html_table = "mcatalogo/views/producto/table.html"
    routes = {
        '/producto': {'GET': 'index', 'POST': 'table'},
        '/producto_insert': {'POST': 'insert'},
        '/producto_servicios': {'POST': 'producto_servicio'},
        '/producto_update': {'PUT': 'edit', 'POST': 'update'},
        '/producto_delete': {'POST': 'delete'},
        '/producto_cat_filter': {'POST': 'producto_cat_filter'},
        '/orden_producto': {'POST': 'orden_producto'},

    }

    def get_extra_data(self):
      aux = super().get_extra_data()
      aux['catalogo'] = CatalogoManager(self.db).get_all()
      aux['producto'] = ProductoManager(self.db).get_all()
      aux['catalogounico'] = CatalogoManager(self.db).get_all_distinct()
      return aux

    def producto_servicio(self ):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            # url = ruta
            gestion = diccionary['Gestion']
            catalogo = diccionary['Numerocatalogo']
            cat = CatalogoManager(self.db).get_cat_id(gestion, catalogo)
            headers = {'Content-Type': 'application/json'}
            url = api+"ListProds/Catalogo/"+str(gestion)+"/"+cat.Numerocatalogo
            string = dict()
            cadena = json.dumps(string)
            body = cadena
            resp = requests.get(url, data=body, headers=headers, verify=False)
            response = json.loads(resp.text)
            i = 0
            prod = ProductoManager(self.db).validarProducto(response)
            catalogos = CatalogoManager(self.db).catalogo(gestion, cat.Numerocatalogo)
            ip = diccionary['ip']
            ip= self.manager(self.db).obtener_ip(ip)
            for diccionary in prod:
                # diccionary = CatalogoManager(self.db).validar(diccionary,catalogo)
                self.set_session()
                diccionary['catalogo'] = cat.id
                diccionary['gestion'] = cat.Gestion
                diccionary['user'] = self.get_user_id()
                diccionary['ip']=ip
                diccionary['TipoProducto'] = 1
                objeto = ProductoManager(self.db).entity(**diccionary)
                pagina = PaginaManager(self.db).productopagina(objeto)
                if pagina != None:
                  diccionary['pagina'] = pagina.id
                  a = ProductoManager(self.db).insert(objeto)
            print("termino")
            self.respond(success=True, message='Insertado correctamente.')
            # self.db.close()
        except Exception as e:
            print("Error: " + str(e))
            self.respond(success=False, message='Ocurrio un problema y no se pudo insertar correctamente'+str(e)+'.')
        self.db.close()
    def index(self):
        self.set_session()
        self.verif_privileges()
        usuario = self.get_user()
        if usuario.id == 1:
            result = self.manager(self.db).list_all()
        else:
            cat = CatalogoManager(self.db).get_cat_by_fecha_actual(FECHA_HOY)
            if cat != None:
                result = self.manager(self.db).list_all_productos_index(cat.Gestion, cat.id, 1)
            else:
                result = self.manager(self.db).lista_vacio()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def edit(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtain(diccionary['id'])
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        diccionary['TipoProducto'] = 1
        diccionary['remplazo'] = int(diccionary['remplazo'])
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        else:
            link = ' '
            diccionary['foto'] = link
        ins_manager = self.manager(self.db)
        indicted_object = ins_manager.obtain(diccionary['remplazo'])
        diccionarioTest = indicted_object.get_dict()
        diccionary['gestion'] = diccionarioTest['gestion']
        diccionary['catalogo'] = diccionarioTest['catalogo']
        diccionary['pagina'] = diccionarioTest['pagina']
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')
        self.db.close()

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
        self.db.close()

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            ip = diccionary['ip']
            diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
            NivelManager(self.db).delete(diccionary['id'], diccionary['user'], diccionary['ip'], diccionary['enabled'])
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response="No existe", success=False, message="Not Found")
        self.db.close()


    def producto_cat_filter(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        gestion = diccionary['gestion']
        catalogo = diccionary['catalogo']
        indicted_object = ProductoManager(self.db).get_producto_by_catalogo(gestion, catalogo, 1)
        response = []
        for prod in indicted_object:
            dic = dict(id=prod.id,
                       nombre=prod.nombre,
                       codigo=prod.codigo,
                       codvta=prod.codvta,
                       precio=prod.precio,
                       prepro=prod.prepro,
                       retail=prod.retail,
                       bonifi=prod.bonifi,
                       impini=prod.impini,
                       impfin=prod.impfin,
                       gesini=prod.gesini,
                       gesfin=prod.gesfin,
                       semini=prod.semini,
                       semfin=prod.semfin,
                       TipoProducto=prod.TipoProducto,
                       foto=prod.foto,
                       catalogo=prod.catalogo,
                       pagina=prod.pagina,
                       orden=prod.orden,
                       remplazo=prod.remplazo
                     )
            response.append(dic)
        self.respond(response=response, success=True, message='Productos del catálogo.')
        self.db.close()

    def orden_producto(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['id'] = diccionary['id_producto']
        diccionary['orden'] = diccionary['orden_producto']
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).update(objeto)
        response = []
        self.respond(response=response, success=True, message='Productos del catálogo.')
        self.db.close()


class NivelController(CrudController):
    manager = ProductoManager
    html_index = "mcatalogo/views/producto/nivel.html"
    html_table = "mcatalogo/views/producto/nivel.html"
    routes = {
        '/nivel': {'GET': 'index', 'POST': 'table'},
        '/nivel_insert': {'POST': 'insert'},
        '/nivel_update': {'PUT': 'edit', 'POST': 'update'},
        '/nivel_delete': {'POST': 'delete'},
        '/nivel_servicio': {'POST': 'nivel_servicio'},
        '/nivel_cat_filter': {'POST': 'nivel_cat_filter'},
        '/prueba_servicio': {'POST': 'prueba_servicio'},
    }


    # def nivel_servicio(self):
    #     #     try:
    #     #         self.set_session()
    #     #         diccionary = json.loads(self.get_argument("object"))
    #     #         # url = ruta
    #     #         gestion = diccionary['Gestion']
    #     #         catalogo = diccionary['Numerocatalogo']
    #     #         cat = CatalogoManager(self.db).get_cat_id(gestion, catalogo)
    #     #         url = api+"niveles/ListNivel/"+str(gestion)+"/"+cat.Numerocatalogo
    #     #         headers = {'Content-Type': 'application/json'}
    #     #         string = dict()
    #     #         cadena = json.dumps(string)
    #     #         body = cadena
    #     #         resp = requests.get(url, data=body, headers=headers, verify=False)
    #     #         response = json.loads(resp.text)
    #     #         print(response)
    #     #         tipo = 2
    #     #         ip = diccionary['ip']
    #     #         ip = self.manager(self.db).obtener_ip(ip)
    #     #         prod = ProductoManager(self.db).validarniveles(response,tipo)
    #     #         #catalogos = CatalogoManager(self.db).catalogo(gestion,catalogo)
    #     #         for diccionary in prod:
    #     #             diccionary['catalogo'] = cat.id
    #     #             diccionary['user'] = self.get_user_id()
    #     #             diccionary['ip'] = ip
    #     #             diccionary['TipoProducto'] = tipo
    #     #            # catalogo = CatalogoManager(self.db).get_cat_id(diccionary['gestion'], diccionary['catalogo'])
    #     #             #diccionary['catalogo'] = catalogo.id
    #     #             objeto = ProductoManager(self.db).entity(**diccionary)
    #     #             ProductoManager(self.db).insert(objeto)
    #     #         print("termino")
    #     #         self.respond(success=True, message='Insertado correctamente.')
    #     #         # self.db.close()
    #     #     except Exception as e:
    #     #         print("Error: " + str(e))
    #     #         self.respond(success=False, message='ocurrio un problema.')
    #     #     self.db.close()


    def prueba_servicio(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            # url = ruta
            gestion = diccionary['Gestion']
            catalogo = diccionary['Numerocatalogo']
            url = "https://181.115.203.250:5050/api/Ventas/Validacion"
            headers = {'Content-Type': 'application/json'}
            Venta = list()

            Venta = dict(usuario = 75,
                        codigorol=3,
                        noventa=0,
                        tipodocumento= "",
                        documento= "09001",
                        fechavta= "2020-2-11",
                        gestion= 2020,
                        semana= 6,
                        unidad= 93,
                        cliente= 75,
                        nombre= "LINA MARBEL TORREZ MORALES",
                        mtobruto= 66,
                        mtodescuento= 0,
                        mtoneto= 48.06,
                        mtobonificable= 48.06,
                        mtonobonificable= 0,
                        mtoretail= 66,
                        sumaretail= 0,
                        literal= "",
                        retailpromo= "",
                        estados= 0,
                        mensaje= ""  )
            DetalleVenta = list()
            DetalleVenta.append(dict(codinterno=10210,
                      codigovta= "S566",
                      producto= "TERMO FIT DECO ELLA",
                      cantidad= 3,
                      preciounitario= 22,
                      preciopromotora= 16.02,
                      importebruto= 66,
                      montobonificacion= 0,
                      importedscto= 0,
                      importeneto= 48.06,
                      retail= 1,
                      bonificacion= 1,
                      estado= ""
                ))
            data = dict()
            data["Venta"] = Venta
            data["DetalleVenta"]=DetalleVenta
            string = dict()
            cadena = json.dumps(string)
            body = cadena
            data = json.dumps(data)
            resp = requests.post(url,data = data,headers=headers,verify=False)
            response = json.loads(resp.text)
            print(response)
            print("termino")
            self.respond( response=response , success=True,message=str(response))
            # self.db.close()
        except Exception as e:
            print("Error: " + str(e))
            self.respond(success=False, message='ocurrio un problema.')
        self.db.close()



    def index(self):
        self.set_session()
        self.verif_privileges()
        usuario = self.get_user()
        cat = CatalogoManager(self.db).get_cat_by_fecha_actual(FECHA_HOY)
        if usuario.id == 1:
            result = self.manager(self.db).listar_tipo(2)
        else:
            if(cat != None):
                result = self.manager(self.db).list_all_productos_index(cat.Gestion, cat.id, 2)
            else:
                result = self.manager(self.db).lista_vacio()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def edit(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtain(diccionary['id'])
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['catalogo'] = CatalogoManager(self.db).get_all()
        aux['catalogounico'] = CatalogoManager(self.db).get_all_distinct()
        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        diccionary['TipoProducto'] = 2
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        else:
            link = ' '
            diccionary['foto'] = link
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')
        self.db.close()



    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
        self.db.close()

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            ip = diccionary['ip']
            diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
            NivelManager(self.db).delete(diccionary['id'], diccionary['user'], diccionary['ip'], diccionary['enabled'])
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response="No existe", success=False, message="Not Found")
        self.db.close()

    def nivel_cat_filter(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        gestion = diccionary['gestion']
        catalogo = diccionary['catalogo']
        indicted_object = ProductoManager(self.db).get_producto_by_catalogo(gestion, catalogo, 2)
        response = []
        for prod in indicted_object:
            dic = dict(id=prod.id,
                       nombre=prod.nombre,
                       codigo=prod.codigo,
                       codvta=prod.codvta,
                       precio=prod.precio,
                       prepro=prod.prepro,
                       retail=prod.retail,
                       bonifi=prod.bonifi,
                       impini=prod.impini,
                       impfin=prod.impfin,
                       gesini=prod.gesini,
                       gesfin=prod.gesfin,
                       semini=prod.semini,
                       semfin=prod.semfin,
                       TipoProducto=prod.TipoProducto,
                       foto=prod.foto,
                       catalogo=prod.catalogo,
                       pagina=prod.pagina,
                       orden=prod.orden,
                       remplazo=prod.remplazo
                     )
            response.append(dic)
        self.respond(response=response, success=True, message='Nivel del catálogo.')
        self.db.close()


class PromocionController(CrudController):
    manager = ProductoManager
    html_index = "mcatalogo/views/producto/promocion.html"
    html_table = "mcatalogo/views/producto/promocion_table.html"
    routes = {
        '/promocion': {'GET': 'index', 'POST': 'table'},
        '/promocion_insert': {'POST': 'insert'},
        '/promocion_update': {'PUT': 'edit', 'POST': 'update'},
        '/promocion_delete': {'POST': 'delete'},
        '/promocion_servicio': {'POST': 'promocion_servicio'},
        '/promocion_cat_filter': {'POST': 'promocion_cat_filter'},
    }

    def promocion_servicio(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            # url = ruta
            gestion = diccionary['Gestion']
            catalogo = diccionary['Numerocatalogo']
            cat = CatalogoManager(self.db).get_cat_id(gestion, catalogo)
            url = api+"Promocions/ListPromocion/"+str(gestion)+"/"+cat.Numerocatalogo
            headers = {'Content-Type': 'application/json'}
            string = dict()
            cadena = json.dumps(string)
            body = cadena
            resp = requests.get(url, data=body, headers=headers, verify=False)
            response = json.loads(resp.text)
            print(response)
            tipo =3
            prod = ProductoManager(self.db).validarniveles(response,tipo)
            i = 0
            ip = diccionary['ip']
            ip = self.manager(self.db).obtener_ip(ip)
            for diccionary in prod:
                diccionary['catalogo'] = cat.id
                diccionary['user'] = self.get_user_id()
                diccionary['gestion'] = gestion
                diccionary['ip'] = ip
                diccionary['TipoProducto'] = tipo
                objeto = ProductoManager(self.db).entity(**diccionary)
                ProductoManager(self.db).insert(objeto)
            print("termino")
            self.respond(success=True, message='Insertado correctamente.')
            # self.db.close()
        except Exception as e:
            print("Error: " + str(e))
            self.respond(success=False, message='Ocurrio un problema al insertar.')

    def index(self):
        self.set_session()
        self.verif_privileges()
        cat = CatalogoManager(self.db).get_cat_by_fecha_actual(FECHA_HOY)
        usuario = self.get_user()
        if usuario.id == 1:
            result = self.manager(self.db).listar_tipo(3)
        else:
            if cat != None:
                result = self.manager(self.db).list_all_productos_index(cat.Gestion, cat.id, 3)
            else:
                result = self.manager(self.db).lista_vacio()
        # result = self.manager(self.db).list_all_promocion()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def edit(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtain(diccionary['id'])
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['catalogo'] = CatalogoManager(self.db).get_all()
        aux['catalogounico'] = CatalogoManager(self.db).get_all_distinct()
        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        diccionary['TipoProducto'] = 3
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')
        self.db.close()

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
        self.db.close()

    def delete(self):
      try:
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        ProductoManager(self.db).delete(diccionary['id'], diccionary['user'], diccionary['ip'],
                                        diccionary['enabled'])
        self.respond(success=True, message='Eliminado correctamente.')
      except Exception as e:
        print(e)
        self.respond(response="No existe", success=False, message="Not Found")
      self.db.close()

    def promocion_cat_filter(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        gestion = diccionary['gestion']
        catalogo = diccionary['catalogo']
        indicted_object = ProductoManager(self.db).get_producto_by_catalogo(gestion, catalogo, 3)
        response = []
        for prod in indicted_object:
            dic = dict(id=prod.id,
                       nombre=prod.nombre,
                       codigo=prod.codigo,
                       codvta=prod.codvta,
                       precio=prod.precio,
                       prepro=prod.prepro,
                       retail=prod.retail,
                       bonifi=prod.bonifi,
                       impini=prod.impini,
                       impfin=prod.impfin,
                       gesini=prod.gesini,
                       gesfin=prod.gesfin,
                       semini=prod.semini,
                       semfin=prod.semfin,
                       TipoProducto=prod.TipoProducto,
                       foto=prod.foto,
                       catalogo=prod.catalogo,
                       pagina=prod.pagina,
                       orden=prod.orden,
                       remplazo=prod.remplazo
                     )
            response.append(dic)
        self.respond(response=response, success=True, message='Promoción del catalogo.')
        self.db.close()


class OfertaController(CrudController):
    manager = ProductoManager
    html_index = "mcatalogo/views/producto/oferta.html"
    html_table = "mcatalogo/views/producto/oferta_table.html"
    routes = {
        '/oferta': {'GET': 'index', 'POST': 'table'},
        '/oferta_insert': {'POST': 'insert'},
        '/oferta_update': {'PUT': 'edit', 'POST': 'update'},
        '/oferta_delete': {'POST': 'delete'},
        '/oferta_servicio': {'POST': 'oferta_servicio'},
        '/oferta_cat_filter': {'POST': 'oferta_cat_filter'},
    }

    def oferta_servicio(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            # url = ruta
            gestion = diccionary['Gestion']
            catalogo = diccionary['Numerocatalogo']
            cat = CatalogoManager(self.db).get_cat_id(gestion, catalogo)
            url = api+"Promocions/ListOfertas/"+str(gestion)+"/"+cat.Numerocatalogo
            headers = {'Content-Type': 'application/json'}
            string = dict()
            cadena = json.dumps(string)
            body = cadena
            resp = requests.get(url, data=body, headers=headers, verify=False)
            response = json.loads(resp.text)
            tipo = 4
            prod = ProductoManager(self.db).validarniveles(response,tipo)
            i = 0
            ip = diccionary['ip']
            ip = self.manager(self.db).obtener_ip(ip)
            for diccionary in prod:
                diccionary['catalogo'] = cat.id
                # diccionary['gestion'] = gestion
                diccionary['user'] = self.get_user_id()
                diccionary['gestion'] = gestion
                diccionary['ip'] = ip
                diccionary['TipoProducto'] = tipo
                objeto = ProductoManager(self.db).entity(**diccionary)
                ProductoManager(self.db).insert(objeto)
            print("termino")
            self.respond(success=True, message='Insertado correctamente.')
            # self.db.close()
        except Exception as e:
            print("Error: " + str(e))
            self.respond(success=False, message='Se Produjo un error.')
        self.db.close()

    def index(self):
        self.set_session()
        self.verif_privileges()
        usuario = self.get_user()
        if usuario.id == 1:
            result = self.manager(self.db).listar_tipo(4)
        else:
            cat = CatalogoManager(self.db).get_cat_by_fecha_actual(FECHA_HOY)
            if cat != None:
                result = self.manager(self.db).list_all_productos_index(cat.Gestion, cat.id, 4)
            else:
                result = self.manager(self.db).lista_vacio()
        # result = self.manager(self.db).list_all_oferta()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def edit(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtain(diccionary['id'])
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['catalogo'] = CatalogoManager(self.db).get_all()
        aux['catalogounico'] = CatalogoManager(self.db).get_all_distinct()
        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        diccionary['TipoProducto'] = 4
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        else:
            link = ' '
            diccionary['foto'] = link
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')
        self.db.close()

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
        self.db.close()

    def delete(self):
      try:
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        ProductoManager(self.db).delete(diccionary['id'], diccionary['user'], diccionary['ip'],
                                           diccionary['enabled'])
        self.respond(success=True, message='Eliminado correctamente.')
      except Exception as e:
        print(e)
        self.respond(response="No existe", success=False, message="Not Found")
      self.db.close()

    def oferta_cat_filter(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        gestion = diccionary['gestion']
        catalogo = diccionary['catalogo']
        indicted_object = ProductoManager(self.db).get_producto_by_catalogo(gestion, catalogo, 4)
        response = []
        for prod in indicted_object:
            dic = dict(id=prod.id,
                       nombre=prod.nombre,
                       codigo=prod.codigo,
                       codvta=prod.codvta,
                       precio=prod.precio,
                       prepro=prod.prepro,
                       retail=prod.retail,
                       bonifi=prod.bonifi,
                       impini=prod.impini,
                       impfin=prod.impfin,
                       gesini=prod.gesini,
                       gesfin=prod.gesfin,
                       semini=prod.semini,
                       semfin=prod.semfin,
                       TipoProducto=prod.TipoProducto,
                       foto=prod.foto,
                       catalogo=prod.catalogo,
                       pagina=prod.pagina,
                       orden=prod.orden,
                       remplazo=prod.remplazo
                     )
            response.append(dic)
        self.respond(response=response, success=True, message='Oferta del catalogo.')
        self.db.close()


class OfertaWebController(CrudController):
    manager = ProductoManager
    html_index = "mcatalogo/views/producto/ofertaweb.html"
    html_table = "mcatalogo/views/producto/ofertaweb_table.html"
    routes = {
        '/ofertaweb': {'GET': 'index', 'POST': 'table'},
        '/ofertaweb_insert': {'POST': 'insert'},
        '/ofertaweb_update': {'PUT': 'edit', 'POST': 'update'},
        '/ofertaweb_delete': {'POST': 'delete'},
        '/ofertaweb_servicio': {'POST': 'ofertaweb_servicio'},
        '/ofertaweb_cat_filter': {'POST': 'ofertaweb_cat_filter'},
    }

    def ofertaweb_servicio(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            # url = ruta
            gestion = diccionary['Gestion']
            catalogo = diccionary['Numerocatalogo']
            cat = CatalogoManager(self.db).get_cat_id(gestion, catalogo)
            url = api+"Promocions/ListOfertWeb/"+str(gestion)+"/"+cat.Numerocatalogo
            headers = {'Content-Type': 'application/json'}
            string = dict()
            cadena = json.dumps(string)
            body = cadena
            resp = requests.get(url, data=body, headers=headers, verify=False)
            response = json.loads(resp.text)
            tipo = 6
            ip = diccionary['ip']
            ip = self.manager(self.db).obtener_ip(ip)
            prod = ProductoManager(self.db).validarniveles(response, tipo)
            for diccionary in prod:
               # diccionary = CatalogoManager(self.db).validar(diccionary, catalogo)
                diccionary['catalogo'] = cat.id
                diccionary['user'] = self.get_user_id()
                diccionary['ip'] = ip
                diccionary['TipoProducto'] = tipo
                objeto = ProductoManager(self.db).entity(**diccionary)
                ProductoManager(self.db).insert(objeto)
            print("termino")
            self.respond(success=True, message='Insertado correctamente.')
            # self.db.close()
        except Exception as e:
            print("Error: " + str(e))
            self.respond(success=False, message='Se produjo un error.')
        self.db.close()

    def index(self):
        self.set_session()
        self.verif_privileges()
        cat = CatalogoManager(self.db).get_cat_by_fecha_actual(FECHA_HOY)
        usuario = self.get_user()
        if usuario.id == 1:
            result = self.manager(self.db).listar_tipo(6)
        else:
            if cat != None:
                result = self.manager(self.db).list_all_productos_index(cat.Gestion, cat.id, 6)
            else:
                result = self.manager(self.db).lista_vacio()
        # result = self.manager(self.db).list_all_ofertaweb()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def edit(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtain(diccionary['id'])
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operación exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['catalogo'] = CatalogoManager(self.db).get_all()
        aux['catalogounico'] = CatalogoManager(self.db).get_all_distinct()
        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        diccionary['TipoProducto'] = 6
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        else:
            link = ' '
            diccionary['foto'] = link
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')
        self.db.close()

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        objeto = self.manager(self.db).entity(**diccionary)
        ProductoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
        self.db.close()

    def delete(self):
      try:
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        ProductoManager(self.db).delete(diccionary['id'], diccionary['user'], diccionary['ip'],
                                           diccionary['enabled'])
        self.respond(success=True, message='Eliminado correctamente.')
      except Exception as e:
        print(e)
        self.respond(response="No existe", success=False, message="Not Found")
      self.db.close()

    def ofertaweb_cat_filter(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        gestion = diccionary['gestion']
        catalogo = diccionary['catalogo']
        indicted_object = ProductoManager(self.db).get_producto_by_catalogo(gestion, catalogo, 6)
        response = []
        for prod in indicted_object:
            dic = dict(id=prod.id,
                       nombre=prod.nombre,
                       codigo=prod.codigo,
                       codvta=prod.codvta,
                       precio=prod.precio,
                       prepro=prod.prepro,
                       retail=prod.retail,
                       bonifi=prod.bonifi,
                       impini=prod.impini,
                       impfin=prod.impfin,
                       gesini=prod.gesini,
                       gesfin=prod.gesfin,
                       semini=prod.semini,
                       semfin=prod.semfin,
                       TipoProducto=prod.TipoProducto,
                       foto=prod.foto,
                       catalogo=prod.catalogo,
                       pagina=prod.pagina,
                       orden=prod.orden,
                       remplazo=prod.remplazo
                     )
            response.append(dic)
        self.respond(response=response, success=True, message='OfertaWeb del catalogo.')
        self.db.close()
#servicios de producto




