import base64
from tornado.gen import coroutine
from .managers import *
from ..usuarios.managers import *
from ..operaciones.managers import *
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from ..common.controllers import CrudController, SuperController, ApiController
from xhtml2pdf import pisa
import os.path
import requests
from PIL import Image
import io
from ..mcatalogo.managers import *
import dropbox
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
global report
report = Report()
global image_report
image_report = "../server/common/resources/images/sabsa.jpg"

global api
#afuera de la empresa Tupperware
api ="https://181.115.203.250:5050/api/"
#dentro de la empresa Tupperware
#api = "http://192.168.1.200:4040/api/"



class AyudaVentasController(CrudController):
    manager = AyudaVentasManager
    html_index = "mayudaventas/views/ayudaventas/index.html"
    html_table = "mayudaventas/views/ayudaventas/table.html"
    routes = {
        '/ayudaventas': {'GET': 'index', 'POST': 'table'},
        '/ayudaventas_insert': {'POST': 'insert'},
        '/ayudaventas_update': {'PUT': 'edit', 'POST': 'update'},
        '/ayudaventas_delete': {'POST': 'delete'},
        '/ayudaventas_servicio': {'POST': 'ayudaventas_servicio'},
        '/ayudaventas_cat_filter': {'POST': 'ayudaventas_cat_filter'}
    }

    def ayudaventas_servicio(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            # url = ruta
            gestion = diccionary['Gestion']
            catalogo = diccionary['Numerocatalogo']
            cat = CatalogoManager(self.db).get_cat_id(gestion, catalogo)
            url = api+"AyuVtas/ListAyuVtas/"+str(gestion)+"/"+cat.Numerocatalogo
            headers = {'Content-Type': 'application/json'}
            string = dict()
            cadena = json.dumps(string)
            body = cadena
            resp = requests.get(url, data=body, headers=headers, verify=False)
            response = json.loads(resp.text)
            ip = diccionary['ip']
            ip = self.manager(self.db).obtener_ip(ip)
            prod = AyudaVentasManager(self.db).validar_productos(response, int(cat.Numerocatalogo))
            for diccionary in prod:
                diccionary['catalogo'] = cat.id
                diccionary['gestion'] = gestion
                diccionary['user'] = self.get_user_id()
                diccionary['ip'] = ip
                objeto = AyudaVentasManager(self.db).entity(**diccionary)
                AyudaVentasManager(self.db).insert(objeto)
            self.respond(success=True, message='Insertado correctamente.')
            self.db.close()
        except Exception as e:
            print("Error: " + str(e))


    def get_extra_data(self):
      aux = super().get_extra_data()
      aux['catalogo'] = CatalogoManager(self.db).get_all()
      aux['catalogounico'] = CatalogoManager(self.db).get_all_distinct()
      aux['ayudaventas'] = AyudaVentasManager(self.db).get_all()
      return aux

    def index(self):
        self.set_session()
        self.verif_privileges()
        cat = CatalogoManager(self.db).get_cat_by_fecha_actual(FECHA_HOY)
        usuario = self.get_user()
        if usuario.id == 1:
            result = self.manager(self.db).list_all()
        else:
            if cat is not None:
                result = self.manager(self.db).list_all_ayudaventas_index(cat.Gestion, cat.id)
            else:
                result = self.manager(self.db).lista_vacio()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        diccionary['gestion'] = int(diccionary['gestion'])
        diccionary['catalogo'] = int(diccionary['catalogo'])
        diccionary['codigo'] = int(diccionary['codigo'])
        if "archivo" in self.request.files:
            fileinfo = self.request.files["archivo"][0]
            diccionary['foto'] = self.manager(self.db).imagen(fileinfo)
        else:
            link = ' '
            diccionary['foto'] = link
        # cat = CatalogoManager(self.db).get_cat_id(diccionary['gestion'], diccionary['catalogo'])
        # diccionary['catalogo'] = cat.id
        objeto = self.manager(self.db).entity(**diccionary)
        AyudaVentasManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

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
        AyudaVentasManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
        self.db.close()

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            ip = diccionary['ip']
            diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
            AyudaVentasManager(self.db).delete(diccionary['id'], diccionary['user'], diccionary['ip'], diccionary['enabled'])
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response="No existe", success=False, message="Not Found")
        self.db.close()

    def edit(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtain(diccionary['id'])
        cat_id = CatalogoManager(self.db).get_by_id(indicted_object.catalogo)
        indicted_object.catalogo = cat_id.Numerocatalogo
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operación exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def ayudaventas_cat_filter(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        gestion = diccionary['gestion']
        catalogo = diccionary['catalogo']
        indicted_object = AyudaVentasManager(self.db).get_ayudaventas_by_catalogo(gestion, catalogo)
        response = []
        for ayudaventas in indicted_object:
            dic = dict(id=ayudaventas.id,
                       nombre=ayudaventas.nombre,
                       codigo=ayudaventas.codigo,
                       codvta=ayudaventas.codvta,
                       precio=ayudaventas.precio,
                       prepro=ayudaventas.prepro,
                       retail=ayudaventas.retail,
                       bonifi=ayudaventas.bonifi,
                       gestion=ayudaventas.gestion,
                       catalogo=ayudaventas.catalogo,
                       foto=ayudaventas.foto
                     )
            response.append(dic)
        self.respond(response=response, success=True, message='AyudaVentas del catalogo.')
        self.db.close()


class ApiAyudaVentasController(ApiController):
    manager = AyudaVentasManager

    routes = {
        '/api/v1/ayudaventas_insert': {'POST': 'insert'},
        '/api/v1/ayudaventas_update': {'POST': 'update'},
        '/api/v1/ayudaventas_delete': {'POST': 'delete'},
        '/api/v1/listar_ayudaventas': {'GET': 'listar_ayudaventas'},
    }

    def check_xsrf_cookie(self):
        return

    # Falta implementar la IP de donde
    def insert(self):
        data = json.loads(self.request.body.decode('utf-8'))
        iduser = data['iduser']
        self.set_session()
        # token = UsuarioManager(self.db).user_token(iduser)
        # if data['id'] == "":
        # data['id'] = None
        try:
            dic = dict(nombre=str(data['nombre']),
                       codigo=str(data['codigo']),
                       codvta=str(data['codvta']), precio=str(data['precio']),
                       prepro=str(data['prepro']), retail=str(data['retail']),
                       bonifi=str(data['bonifi']), foto=str(data['foto']),
                       user=str(data['iduser']))
            objeto = self.manager(self.db).entity(**dic)
            AyudaVentasManager(self.db).insert(objeto)
            self.respond(success=True, message='Insertado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response="No existe", success=False, message="Not Found")
        self.db.close()

    def listar_ayudaventas(self):
        self.set_session()
        try:
            result = self.manager(self.db).get_all()
            response = []
            for objeto in result:
                dic = dict(id=str(objeto.id), nombre=str(objeto.nombre),
                           codigo=str(objeto.codigo),
                           codvta=str(objeto.codvta), precio=str(objeto.precio),
                           prepro=str(objeto.prepro), retail=str(objeto.retail),
                           bonifi=str(objeto.bonifi), foto=str(objeto.foto))
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="Lista de AyudaVentas recuperadas correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=0, success=False, message="Not Found")
        self.db.close()

