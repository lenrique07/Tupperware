import hashlib
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import make_transient

from ..operaciones.managers import *

from ..database.connection import transaction
from server.common.managers import SuperManager, Error
from .models import *
from sqlalchemy.sql import func

import string
from random import *
import random



class UsuarioManager(SuperManager):
    def __init__(self, db):
        super().__init__(Usuario, db)

    def validar_usuario_servicio(self,objeto,rol):
        obj = []
        for usuario in objeto:
            user = ""
            password = hashlib.sha512( usuario['passwo'].encode()).hexdigest()
            user = self.db.query(self.entity).filter(self.entity.nombre == usuario['nombre']).filter(self.entity.password ==password)\
                .first()
            if user == None:
                bol = False
                for r in rol['objects']:
                    ro = r.id - 1
                    if ro == usuario['codrol']:
                        bol = True
                        break
                if bol:
                    obj.append(usuario)
                else:
                    obj = bol
                    break
        return obj

    def name_role(self, rol):
        role = self.db.query(Rol).filter_by(id=rol).first()
        nombre_rol = role.name
        return nombre_rol


    def get_random_string(self):
        random_list = []
        for i in range(8):
            random_list.append(random.choice(string.ascii_uppercase + string.digits))
        return ''.join(random_list)




    def insert(self, Usuario):
        if Usuario.fkrol > 0:
            Usuario.password = hashlib.sha512(Usuario.password.encode()).hexdigest()
            codigo = self.get_random_string()
            Usuario.codigo = codigo
            fecha = BitacoraManager(self.db).fecha_actual()
            b = Bitacora(fkusuario=Usuario.user_id, ip=Usuario.ip, accion="Se registró un usuario.", fecha=fecha)
            super().insert(b)
            u = super().insert(Usuario)
            return u
        return Error('unknown')

    def insertar_usuario(self,prod,user,ip):
        for diccionary in prod:
                    diccionary['user_id'] = user
                    diccionary['ip'] = ip
                    diccionary['username'] = diccionary['codigo']
                    diccionary['apellido'] = "."
                    diccionary['fkrol'] = diccionary['codrol']+1
                    diccionary['correo'] = str(diccionary['codigo']) +"@test.com"
                    diccionary['password'] = hashlib.sha512(diccionary['passwo'].encode()).hexdigest()
                    diccionary['enabled'] = 1
                    objeto = UsuarioManager(self.db).entity(**diccionary)
                    print(diccionary)
                    object = self.many_to_many(objeto)
                    self.db.add(object)
        self.db.commit()
        return object


    def update(self, Usuarioupd):
        fecha = BitacoraManager(self.db).fecha_actual()
        Usuarioupd.password = hashlib.sha512(Usuarioupd.password.encode()).hexdigest()
        b = Bitacora(fkusuario=Usuarioupd.user_id, ip=Usuarioupd.ip, accion="Se modificó un usuario.", fecha=fecha)
        super().insert(b)
        user = self.db.query(Usuario).filter(Usuario.id == Usuarioupd.id).one()
        return super().update(Usuarioupd)

    def servicio_usuario(self, data):
        user = self.db.query(Usuario).filter(Usuario.id == data['id']).one()
        if data['sobrenombre']!=None:
            user.sobrenombre=data['sobrenombre']
        if data['foto']!=None:
            user.foto=data['foto']
        if data['nombre']!=None:
            user.nombre=data['nombre']
        if data['apellido']!=None:
            user.apellido=data['apellido']
        if data['correo']!=None:
            user.correo=data['correo']
        if data['telefono']!=None:
            user.telefono=data['telefono']
        if data['password']!=None:
            user.password= hashlib.sha512(data['password'].encode()).hexdigest()
        if data['user']!=None:
            user.user=int(data['id'])
        if data['ip']!=None:
            user.ip=data['ip']
        return user

    def update_users(self, emailprev, emailnew, nameprev, namenew):
        u = self.db.query(Usuario).filter(Usuario.correo == emailprev).one()

        if u:
            ap_user = u.apellido
            result = nameprev.index(ap_user)
            print(result)
            u.correo = emailnew

    def delete_user(self, id, enable, Usuariocr, ip):
        x = self.db.query(Usuario).filter(Usuario.id == id).one()

        if enable == True:
            r = self.db.query(Rol).filter(Rol.id == x.fkrol).one()
            if r.enabled:
                x.enabled = enable
            else:
                return False
            message = "Se habilitó un usuario."
        else:
            x.enabled = enable
            message = "Se inhabilitó un usuario."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuariocr, ip=ip, accion=message, fecha=fecha)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return True

    def activate_Usuarios(self, id, Usuario, ip):
        x = self.db.query(Usuario).filter(Usuario.id == id).one()
        x.enabled = 1
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuario, ip=ip, accion="Se activó un usuario.", fecha=fecha)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

    def get_privileges(self, id, route):
        parent_module = self.db.query(Modulo).\
            join(Rol.modulos).join(Usuario).\
            filter(Modulo.route == route).\
            filter(Usuario.id == id).\
            filter(Usuario.enabled).\
            first()
        if not parent_module:
            return dict()
        modules = self.db.query(Modulo).\
            join(Rol.modulos).join(Usuario).\
            filter(Modulo.fkmodulo == parent_module.id).\
            filter(Usuario.id == id).\
            filter(Usuario.enabled)
        privileges = {parent_module.name: parent_module}
        for module in modules:
            privileges[module.name] = module
        return privileges

    def list_all(self):
        return dict(objects=self.db.query(Usuario).distinct())

    def listar_todo(self):
        return dict(objects=self.db.query(Rol).filter(Rol.id != 1 ).distinct())

    def listar_usuario_5(self,rol):
        a = dict(objects=self.db.query(Usuario).filter(Usuario.fkrol == rol).all())
        return a
    def has_access(self, id, route):
        aux = self.db.query(Usuario.id).\
            join(Rol).join(Acceso).join(Modulo).\
            filter(Usuario.id == id).\
            filter(Modulo.route == route).\
            filter(Usuario.enabled).\
            all()
        return len(aux) != 0

    def get_page(self, page_nr=1, max_entries=10, like_search=None, order_by=None, ascendant=True, query=None):
        query = self.db.query(Usuario).join(Rol).filter(Rol.id > 1)
        return super().get_page(page_nr, max_entries, like_search, order_by, ascendant, query)

    def login_Usuario(self, username, password):
        password = hashlib.sha512(password.encode()).hexdigest()
        return self.db.query(Usuario).filter(Usuario.username == username).filter(Usuario.password == password).filter(
            Usuario.enabled == 1)

    def login_Usuario_servicio(self, username, password):
      try:
          password = hashlib.sha512(password.encode()).hexdigest()
          a = self.db.query(Usuario).filter(Usuario.username == username).filter(Usuario.password == password).filter(Usuario.enabled == 1)
          return dict(objects =a)
      except Exception as e:
          return dict(objects="hay usuario repetido")
    def get_userById(self, id):
        return dict(profile=self.db.query(Usuario).filter(Usuario.id == id).first())

    def update_password(self, Usuario):
        Usuario.password = hashlib.sha512(Usuario.password.encode()).hexdigest()
        return super().update(Usuario)

    def get_by_password(self, Usuario_id, password):
        a = str(password).encode()
        a = hashlib.sha256(a)
        nuevo = a.hexdigest()
        a = self.db.query(Usuario).filter(Usuario.id == Usuario_id). \
            filter(Usuario.password == hashlib.sha512(str(password).encode()).hexdigest()).first()
        return a
    def get_by_pass(self, Usuario_id):
        return self.db.query(Usuario).filter(Usuario.id == Usuario_id).first()

    def update_profile(self, Usuarioprf, ip):
        usuario = self.db.query(Usuario).filter_by(id=Usuarioprf.id).first()
        usuario.nombre = Usuarioprf.nombre
        usuario.apellido = Usuarioprf.apellido
        usuario.correo = Usuarioprf.correo
        self.db.merge(usuario)
        b = Bitacora(fkusuario=usuario.id, ip=ip, accion="Se actualizó perfil de usuario.", fecha=fecha_zona, tabla='cb_usuarios_usuario', identificador=usuario.id)
        super().insert(b)
        self.db.commit()
        return usuario

    def validar_usuario(self, username, password):
        password = hashlib.sha512(password.encode()).hexdigest()
        return self.db.query(func.count(Usuario.id)).filter(Usuario.username == username).filter(
            Usuario.enabled == True).filter(Usuario.password == password).scalar()

    def validar_usuario_sesion(self, codigo, usuario):
        return self.db.query(func.count(Usuario.id)).filter(Usuario.codigo == codigo).filter(
            Usuario.enabled == True).filter(Usuario.id == usuario).scalar()

    def activate_Usuario(self, usuario):
        usuario = self.db.query(Usuario).filter_by(id=usuario).first()
        usuario.activo = 1
        self.db.merge(usuario)
        self.db.commit()

    def update_codigo(self, usuario):
        x = self.db.query(Usuario).filter(Usuario.id == usuario).one()
        x.activo = 0
        x.codigo = self.get_random_string()
        x.token = "Sin Token"
        self.db.commit()
        self.db.close()
        return x

   # def listar_todo(self, id):
    #    return self.db.query(Usuario).filter(Usuario.enabled == True).filter(Usuario.id == id)


    def listar_todo(self ):
        return self.db.query(Usuario).filter(Usuario.enabled == True).all()

    def sacar_id(self,codigo):
        usuario= self.db.query(Usuario).filter(Usuario.enabled == True).filter(Usuario.username == codigo).first()
        return usuario.id

    def sacar_codigo(self,id):
        usuario= self.db.query(Usuario).filter(Usuario.enabled == True).filter(Usuario.id == id ).first()
        return usuario.username

    def sacar_estado(self,id):
        usuario= self.db.query(Usuario).filter(Usuario.id == id ).first()
        return usuario.enabled

class RolManager(SuperManager):
    def __init__(self, db):
        super().__init__(Rol, db)

    def validar_roles(self, objeto):
        bandera = 0
        try:
            for rol in objeto:
                codrol = rol['codrol']+1
                roles = self.db.query(self.entity).filter(self.entity.id == codrol).first()
        except Exception as e:
            print(e)
            bandera = 1
        return bandera



    def get_page(self, page_nr=1, max_entries=10, like_search=None, order_by=None, ascendant=True, query=None):
        query = self.db.query(self.entity).filter(Rol.id > 1)
        return super().get_page(page_nr, max_entries, like_search, order_by, ascendant, query)

    def insert(self, rol):
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=rol.user, ip=rol.ip, accion="Se registró un rol.", fecha=fecha)
        super().insert(b)
        a = super().insert(rol)
        return a

    def update(self, rol):
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=rol.user, ip=rol.ip, accion="Se modificó un rol.", fecha=fecha)
        super().insert(b)
        a = super().update(rol)
        return a

    def list_all(self):
        return dict(objects=self.db.query(Rol).filter(Rol.id != 1 ).distinct())

    def get_all(self):
        return self.db.query(Rol).filter(Rol.enabled == True).filter(Rol.id != 1)

    def delete_rol(self, id, enable, Usuariocr, ip):
        x = self.db.query(Rol).filter(Rol.id == id).one()
        x.enabled = enable

        if enable == True:
            message = "Se habilitó un rol."
        else:
            users = self.db.query(Usuario).filter(Usuario.enabled == True).filter(Usuario.fkrol == id).all()
            for u in users:
                u.enabled = False

            message = "Se inhabilitó un rol y usuarios relacionados."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=Usuariocr, ip=ip, accion=message, fecha=fecha)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()


class ModuloManager:
    def __init__(self, db):
        self.db = db

    def list_all(self):
        return self.db.query(Modulo).filter(Modulo.fkmodulo==None)


class LoginManager:

    def login(self, username, password):
        """Retorna un usuario que coincida con el username y password dados.

        parameters
        ----------
        Usuarioname : str
        password : str
            El password deberá estar sin encriptar.

        returns
        -------
        Usuario
        None
            Retornará None si no encuentra nada.
        """
        password = hashlib.sha512(password.encode()).hexdigest()
        with transaction() as session:
            usuario = session.query(Usuario).\
                options(joinedload('rol').
                        joinedload('modulos').
                        joinedload('children')).\
                filter(Usuario.username == username).\
                filter(Usuario.password == password).\
                filter(Usuario.enabled).\
                first()
            if not usuario:
                return None
            session.expunge(usuario)
            make_transient(usuario)
        usuario.rol.modulos = self.order_modules(usuario.rol.modulos)
        return usuario

    def obtener_ip(self,ip):
        ips=ip
        i = ip.find("ip")
        f = ip.find("ts")
        ip = ip[i + 3:f - 1]
        return ip

    def obtener_ips(self,ip):
        ips=ip
        i = ip.find("ip")
        f = ip.find("ts")
        ip = ip[i + 3:f]
        return ip


    def not_enabled(self, username, password):
        """Retorna un usuario que coincida con el username y password dados.

        parameters
        ----------
        Usuarioname : str
        password : str
            El password deberá estar sin encriptar.

        returns
        -------
        Usuario
        None
            Retornará None si no encuentra nada.
        """
        password = hashlib.sha512(password.encode()).hexdigest()
        with transaction() as session:
            usuario = session.query(Usuario).\
                options(joinedload('rol').
                        joinedload('modulos').
                        joinedload('children')).\
                filter(Usuario.username == username).\
                filter(Usuario.password == password).\
                filter(Usuario.enabled == False).\
                first()
            if not usuario:
                return None
            session.expunge(usuario)
            make_transient(usuario)
        usuario.rol.modulos = self.order_modules(usuario.rol.modulos)
        return usuario

    def get(self, key):
        with transaction() as session:
            usuario = session.query(Usuario).\
                options(joinedload('rol').
                        joinedload('modulos').
                        joinedload('children')).\
                filter(Usuario.id == key).\
                filter(Usuario.enabled).\
                first()
            if not usuario:
                return None
            session.expunge(usuario)
            make_transient(usuario)
        usuario.rol.modulos = self.order_modules(usuario.rol.modulos)
        return usuario

    def order_modules(self, modules):
        modules.sort(key=lambda x: x.id)
        mods_parents = []
        mods = {}
        while len(modules) > 0:
            module = modules.pop(0)
            module.children = []
            mods[module.id] = module
            parent_module = mods.get(module.fkmodulo, None)
            if parent_module:
                parent_module.children.append(module)
            else:
                mods_parents.append(module)
        return mods_parents
