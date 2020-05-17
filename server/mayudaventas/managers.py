import hashlib
import string
from _ast import In, GeneratorExp
from random import *
from ..operaciones.models import *
from datetime import datetime, timedelta, time, date
from ..operaciones.managers import *
from .models import *
import json
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import make_transient, sessionmaker
import random
from ..database.connection import transaction
from ..usuarios.models import *
from server.common.managers import SuperManager
from .models import *

from ..usuarios.managers import *

global image_report
image_report = 'server/common/resources/images/sabsa-xls.png'


class AyudaVentasManager(SuperManager):
    def __init__(self, db):
        super().__init__(AyudaVentas, db)

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def get_id(self, ids):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.id==ids)

    def get_codigo(self, codigo):
        return self.db.query(self.entity).filter(self.entity.codigo==codigo).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    # Devuelve los productos por la gestion, el id de catalogo
    def get_ayudaventas_by_catalogo(self, gestion, catalogo):
        a = self.db.query(self.entity).filter(self.entity.catalogo == catalogo).filter(self.entity.gestion == gestion).filter(self.entity.enabled == True).all()
        return a

    # Devuelve una lista de ayudaventas no-repetidos
    def validar_productos(self, objeto, numerocatalogo):
        obj = []
        try:
            for producto in objeto:
                prod = ""
                prod = self.db.query(self.entity).\
                    filter(self.entity.nombre == producto['nombre']).\
                    filter(self.entity.codigo == producto['codigo']).\
                    filter(self.entity.gestion == producto["gestion"]).\
                    filter(numerocatalogo == producto["catalogo"]).first()
                if prod is None:
                    obj.append(producto)
            return obj
        except Exception as e:
            print("Error: " + str(e))

    # Devuelve una lista de todos las ayudaventas de una gestion y un id catalogo determinado
    def list_all_ayudaventas_index(self, gestion, cat_id):
        a = self.db.query(self.entity).filter(self.entity.enabled == True).\
            filter(self.entity.gestion == gestion).\
            filter(self.entity.catalogo == cat_id).all()
        return dict(objects=a)

    # Devuelve lista vacía
    def lista_vacio(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.catalogo == -1))

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro AyudaVentas.", fecha=fecha,tabla="cb_ayudaventas", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico AyudaVentas.", fecha=fecha, tabla="cb_ayudaventas", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip, estado):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó AyudaVentas.", fecha=fecha, tabla="cb_ayudaventas", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
