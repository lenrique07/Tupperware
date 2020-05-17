from .models import *
from tornado.gen import coroutine
from ..operaciones.managers import *
from .managers import *
from ..common.controllers import CrudController, SuperController, ApiController
import json
import requests
import os.path
import dropbox

global api
#afuera de la empresa Tupperware
api ="https://181.115.203.250:5050/api/"
#dentro de la empresa Tupperware
#api = "http://192.168.1.200:4040/api/"


class UsuarioController(CrudController):
    manager = UsuarioManager
    html_index = "usuarios/views/usuario/index.html"
    html_table = "usuarios/views/usuario/table.html"
    routes = {
        '/usuario': {'GET': 'index', 'POST': 'table'},
        '/usuario_insert': {'POST': 'insert'},
        '/usuario_update': {'PUT': 'edit', 'POST': 'update'},
        '/usuario_delete': {'POST': 'delete_user'},
        '/usuario_activate': {'POST': 'activate_user'},
        '/usuario_profile': {'GET': 'usuario_profile'},
        '/usuario_update_profile': {'POST': 'user_update_profile'},
        '/usuario_update_password': {'POST': 'user_update_password'},
        '/usuario_reset_password': {'POST': 'usuario_reset_password'},
        '/usuario_codigo_reset': {'POST': 'usuario_codigo_reset'},
        '/usuario_servicio': {'POST': 'usuarioServicio'},
        '/limpiar_usuario': {'POST': 'limpiar_usuario'}
    }

    def limpiar_usuario(self):
        try:
            self.set_session()
            # url = ruta
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user_id'] = self.get_user_id()
            ip = diccionary['ip']
            diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
            url = api+"Usuarios/Limpieza"
            headers = {'Content-Type': 'application/json'}
            string = dict()
            cadena = json.dumps(string)
            body = cadena
            resp = requests.get(url, data=body, headers=headers, verify=False)
            response = json.loads(resp.text)
            diccionary ['user_id']=self.get_user_id()
            diccionary['nombre']= response
            objeto = self.manager(self.db).entity(**diccionary)
            UsuarioManager(self.db).bitacora(objeto)
            self.respond(success=True, message='Se Limpio los Usuarios Correctamente.')
        except Exception as e:
            print("Error: " + str(e))
            self.respond(success=False, message='Error al limpiar'+str(e)+'.')
        self.db.close()


    def usuarioServicio(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            # url = ruta
            url = api+"Usuarios"
            headers = {'Content-Type': 'application/json'}
            string = dict()
            cadena = json.dumps(string)
            body = cadena
            resp = requests.get(url, data=body, headers=headers, verify=False)
            response = json.loads(resp.text)
            rol = RolManager(self.db).list_all()
            print("inicio validacion")
            prod = self.manager(self.db).validar_usuario_servicio(response,rol)
            #prod = response
            ip = diccionary['ip']
            ip = self.manager(self.db).obtener_ip(ip)
            if prod != False:
                if prod != [] :
                    user = self.get_user_id()
                    response = UsuarioManager(self.db).insertar_usuario(prod,user,ip)
                    print("termino")
                    self.respond(success=True, message='Insertado correctamente.')
                else:
                    self.respond(success=False, message='No hay Usuarios Nuevos.')
            else:
                self.respond(success=False, message='Necesita Crear un Nuevos Roles.')
        except Exception as e:
            print("Error: " + str(e))
            self.respond(success=False, message='Error al insertar'+ str(e)+'.' )
        self.db.close()

    def index(self):
            self.set_session()
            self.verif_privileges()
            result = self.manager(self.db).list_all()
            result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
            data = [];
            result.update(self.get_extra_data())
            self.render(self.html_index, **result)
            self.db.close()

    def  get_extra_data(self):
        aux = super().get_extra_data()
        aux['roles'] = RolManager(self.db).get_all()
        return aux

    def insert(self):
      self.set_session()
      try:
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user_id'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        if "archivo" in self.request.files:
          cliente = dropbox.Dropbox('v0XIGaIghHAAAAAAAAAD7T_jN4-pBkDTAT0jxzseAo2sHSt3RWsHD7a-SKfWi5ka')
          fileinfo = self.request.files["archivo"][0]
          fname = fileinfo.filename
          extn = os.path.splitext(fname)[1]
          cname = str(uuid.uuid4()) + extn
          # CORRECCION DROPBOX
          respuesta = cliente.files_upload(fileinfo.body, '/images/' + cname)
          link = cliente.sharing_create_shared_link('/images/' + cname)
          ruta = str(link.url).replace("dl=0", "raw=1")
          diccionary['foto'] = ruta
        else:
          link = ' '
          diccionary['portada'] = link
        objeto = self.manager(self.db).entity(**diccionary)
        UsuarioManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')
      except Exception as e:
        print(e)
        self.respond(success=False, message='Ocurrio un problema al insertar.')
      self.db.close()

    def update(self):
        self.set_session()
        try:
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user_id'] = self.get_user_id()
            ip = diccionary['ip']
            diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
            if "archivo" in self.request.files:
              cliente = dropbox.Dropbox('v0XIGaIghHAAAAAAAAAD7T_jN4-pBkDTAT0jxzseAo2sHSt3RWsHD7a-SKfWi5ka')
              fileinfo = self.request.files["archivo"][0]
              fname = fileinfo.filename
              extn = os.path.splitext(fname)[1]
              cname = str(uuid.uuid4()) + extn
              # CORRECCION DROPBOX
              respuesta = cliente.files_upload(fileinfo.body, '/images/' + cname)
              link = cliente.sharing_create_shared_link('/images/' + cname)
              ruta = str(link.url).replace("dl=0", "raw=1")
              diccionary['foto'] = ruta
            objeto = self.manager(self.db).entity(**diccionary)
            UsuarioManager(self.db).update(objeto)
            self.respond(success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(success=False, message='error'+str(e))
        self.db.close()

    def delete_user(self):
        self.set_session()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        ip = diccionary['ip']
        ip = self.manager(self.db).obtener_ip(ip)
        enable = UsuarioManager(self.db).sacar_estado(id)
        if enable==True:
            enable=False
        else:
            enable=True
        #id = json.loads(self.get_argument("id"))
        resp = UsuarioManager(self.db).delete_user(id, enable, self.get_user_id(), ip)

        if resp:
            if enable == True:
                msg = 'Usuario activado correctamente.'
            else:
                msg = 'Usuario eliminado correctamente.'
            self.respond(success=True, message=msg)
        else:
            msg = 'Rol asignado dado de baja, no es posible habilitar el usuario.'
            self.respond(success=False, message=msg)

    def activate_user(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        UsuarioManager(self.db).activate_users(id, self.get_user_id(), self.request.remote_ip)
        self.respond(success=True, message='Usuario activado correctamente.')

    def usuario_profile(self):
        user = self.get_user()
        self.set_session()
        usuario = UsuarioManager(self.db)
        result = usuario.get_userById(self.get_user_id())
        self.render("usuarios/views/usuario/profile.html", user=user, **result)
        self.db.close()

    def user_update_password(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        user = self.manager(self.db).get_by_password(self.get_user_id(), diccionary['old_password'])
        if user:
            if diccionary['new_password'] == diccionary['new_password_2']:
                user.password = diccionary['new_password']
                self.manager(self.db).update_password(user)
                self.respond(message="Contraseña cambiada correctamente ", success=True)
            else:
                self.respond(message="Datos incorrectos", success=False)
        else:
            self.respond(message="Datos incorrectos", success=False)
        self.db.close()

    def user_reset_password(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        user = self.manager(self.db).get_by_pass(self.get_user_id())
        if user:
            if diccionary['new_password'] == diccionary['new_password_2']:
                user.password = diccionary['new_password']
                self.manager(self.db).update_password(user)
                self.respond(message="Contraseña cambiada correctamente ", success=True)
            else:
                self.respond(message="Datos incorrectos", success=False)
        else:
            self.respond(message="Datos incorrectos", success=False)
        self.db.close()

    def user_update_profile(self):
        self.set_session()

        diccionary = json.loads(self.get_argument("object"))
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        user = self.manager(self.db).update_profile(objeto, diccionary['ip'])
        self.respond(message="Datos Correctos", success=True)
        self.db.close()

    def usuario_codigo_reset(self):
        self.set_session()
        id = json.loads(self.get_argument("id"))
        self.manager(self.db).update_codigo(id)
        self.respond(success=True, message='Modificado Correctamente!')

    def fecha_actual(self):
        return datetime.now(pytz.timezone('America/La_Paz'))


class RolController(CrudController):
    manager = RolManager
    html_index = "usuarios/views/rol/index.html"
    html_table = "usuarios/views/rol/table.html"
    routes = {
        '/rol': {'GET': 'index', 'POST': 'table'},
        '/rol_insert': {'POST': 'insert'},
        '/rol_update': {'PUT': 'edit', 'POST': 'update'},
        '/rol_delete': {'POST': 'delete_rol'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['modulos'] = ModuloManager(self.db).list_all()
        return aux

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        objeto = self.manager(self.db).entity(**diccionary)
        RolManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        objeto = self.manager(self.db).entity(**diccionary)
        RolManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')

    def delete_rol(self):
        self.set_session()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        id = diccionary['id']
        enable = diccionary['enabled']
        ip = diccionary['ip']
        diccionary['ip'] = self.manager(self.db).obtener_ip(ip)
        RolManager(self.db).delete_rol(id, enable, self.get_user_id(), diccionary['ip'] )
        if enable == True:
            msg = 'Rol activado correctamente.'
        else:
            msg = 'Rol inhabilitado correctamente.'
        self.respond(success=True, message=msg)


class LoginController(SuperController):
    @coroutine
    def get(self):
        """Renderiza el login"""
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')
        usuario = self.get_secure_cookie("user")
        if usuario:
            self.redirect("/")
        else:
            self.clear_cookie("user")
            self.render("usuarios/views/login/index.html", error=0)

    @coroutine
    def post(self):
        """Inicia sesión en la aplicación.

        Si se inicia sesión con éxito enctonces se guarda el
        usuario en la cookie caso contrario se vuelve al login.
        """
        self.check_xsrf_cookie()
        username = self.get_argument('username', default=None)
        password = self.get_argument('password', default=None)
        ip = self.get_argument('ip')
        ip = LoginManager().obtener_ip(ip)


        if username is not None and password is not None:
            user = LoginManager().login(username, password)
            if user:
                fecha = self.fecha_actual()
                b = Bitacora(fkusuario=user.id, ip=ip, accion="Inicio de sesión.", fecha=fecha)
                self.insertar_bitacora(b)
                self.set_user_id(user.id)
                self.redirect("/")
            else:
                userb = LoginManager().not_enabled(username, password)
                if userb:
                    self.render("usuarios/views/login/index.html", error=1)
                else:
                    self.render("usuarios/views/login/index.html", error=2)
        else:
            self.render("usuarios/views/login/index.html", error=2)

    def fecha_actual(self):
        return datetime.now(pytz.timezone('America/La_Paz'))

    def insertar_bitacora(self, bitacora):
        with transaction() as session:
            session.add(bitacora)
            session.commit()


class ManualController(SuperController):
    @coroutine
    def get(self):
        usuario = self.get_user()
        self.render("usuarios/views/usuario/manual.html", user=usuario)


class LogoutController(SuperController):
    @coroutine
    def get(self):
        try:
            ip = LoginManager().obtener_ips(self.get_argument("ip"))
            user_id = self.get_user_id()
            fecha = self.fecha_actual()
            print(ip)
            b = Bitacora(fkusuario=user_id, ip=ip, accion="Finalizó sesión.", fecha=fecha)
            self.insertar_bitacora(b)
            self.clear_cookie('user')
            self.redirect(self.get_argument("next", "/"))
        except Exception as e:
            self.clear_cookie('user')
            self.redirect(self.get_argument("next", "/"))

    def fecha_actual(self):
        return datetime.now(pytz.timezone('America/La_Paz'))

    def insertar_bitacora(self, bitacora):
        with transaction() as session:
            session.add(bitacora)
            session.commit()


class ApiLoginController(SuperController):
    @coroutine
    def post(self):
        """Devuelve el usuario que coincida con el username y password dados.

        Si ocurre algún error se retornará None en la respuesta json al
        cliente invocador.
        """
        try:
            username = self.get_argument('username')
            password = self.get_argument('password')

            usuario = LoginManager().login(username, password)
            self.respond(usuario.getDict())
        except:
            self.respond(success=False)


class ApiUserController(ApiController):
    routes = {
            '/api/v1/login_usuario_mobile': {'POST': 'login_usuario_mobile'},
        '/api/v1/update_token_usuario': {'POST': 'update_token_usuario'},
        '/api/v1/listar_usuarios_privilegios': {'POST': 'listar_usuarios_privilegios'},
        '/api/v1/update_movil_privilegio': {'POST': 'update_movil_privilegio'},
    }

    def check_xsrf_cookie(self):
        return
