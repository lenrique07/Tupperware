import base64
from tornado.gen import coroutine

from server.mcatalogo.models import Catalogo
from .managers import *
from ..usuarios.managers import *
from ..operaciones.managers import *
from ..common.controllers import CrudController, SuperController, ApiController



class ConfiguracionController(CrudController):
    manager = ConfiguracionManager
    html_index = "configuracion/views/index.html"
    html_table = "configuracion/views/index.html"
    routes = {
        '/configuracion': {'GET': 'index', 'POST': 'table'},
        '/configuracion_insert': {'POST': 'insert'},
        '/configuracion_update': {'PUT': 'edit', 'POST': 'update'},
        '/configuracion_delete': {'POST': 'delete'},
    }

    def index(self):
        self.set_session()
        self.verif_privileges()
        usuario = self.get_user()
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
        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def get_extra_data(self):
        aux = super().get_extra_data()
        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        objeto = self.manager(self.db).entity(**diccionary)
        self.manager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')
        self.db.close()

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        objeto = self.manager(self.db).entity(**diccionary)
        self.manager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
        self.db.close()

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            ip = diccionary['ip']
            diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
            self.manager(self.db).delete(diccionary['id'], diccionary['user'], diccionary['ip'], diccionary['enabled'])
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response="No existe", success=False, message="Not Found")
        self.db.close()



class FinancieroController(CrudController):
    manager = FinancieroManager
    html_index = "configuracion/views/financiero/index.html"
    html_table = "configuracion/views/financiero/table.html"
    routes = {
        '/financiero': {'GET': 'index', 'POST': 'table'},
        '/financiero_insert': {'POST': 'insert'},
        '/financiero_update': {'PUT': 'edit', 'POST': 'update'},
        '/financiero_delete': {'POST': 'delete'},
    }

    def index(self):
        self.set_session()
        self.verif_privileges()
        usuario = self.get_user()
        result = self.manager(self.db).list_all()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def edit(self):
        self.set_session()
        try:
            self.verif_privileges()
            ins_manager = self.manager(self.db)
            diccionary = json.loads(self.get_argument("object"))
            indicted_object = ins_manager.obtain(diccionary['id'])
            if len(ins_manager.errors) == 0:
                self.respond(indicted_object.get_dict(), message='Operacion exitosa!')
            else:
                self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        except Exception as e:
            print(e)
            self.respond(response="Error", message=str(e))
        self.db.close()

    def get_extra_data(self):
        aux = super().get_extra_data()
        return aux

    def insert(self):
        self.set_session()
        try:
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            ip = diccionary['ip']
            diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
            if "archivo" in self.request.files:
                fileinfo = self.request.files["archivo"][0]
                diccionary['imagen'] = self.manager(self.db).imagen(fileinfo)
            objeto = self.manager(self.db).entity(**diccionary)
            inser = self.manager(self.db).insert(objeto)
            inser  = inser.get_dict()
            self.respond(response=inser,success=True, message='Insertado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response="Error ",success=False,  message=str(e))
        self.db.close()

    def update(self):
        self.set_session()
        try:
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            ip = diccionary['ip']
            diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
            if "archivo" in self.request.files:
                fileinfo = self.request.files["archivo"][0]
                diccionary['imagen'] = self.manager(self.db).imagen(fileinfo)
            objeto = self.manager(self.db).entity(**diccionary)
            update = self.manager(self.db).update(objeto)
            update = update.get_dict()
            self.respond(response=update, success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response="Error ", success=False, message=str(e))
        self.db.close()

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            ip = diccionary['ip']
            diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
            self.manager(self.db).delete(diccionary['id'], diccionary['user'], diccionary['ip'], diccionary['enabled'])
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response="No existe", success=False, message="Not Found")
        self.db.close()
