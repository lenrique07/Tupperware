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
from ..pedido.models import Pedido
from sqlalchemy import desc

from ..usuarios.managers import *

global image_report
image_report = 'server/common/resources/images/sabsa-xls.png'


class ConfiguracionManager(SuperManager):
    def __init__(self, db):
        super().__init__(Configuracion, db)


    def get_configuracion(self, ids):
        prod = self.db.query(self.entity).filter(self.entity.pagina == ids).first()
        return prod

    def get_configuracion_by_id(self, ids):
        prod = self.db.query(self.entity).filter(self.entity.id == ids).first()
        return prod

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def obtener_x_id(self, id):
        return self.db.query(self.entity).filter(self.entity.id == id).first()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro configuracion.", fecha=fecha, tabla="cb_configuracion",
                     identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico configuracion.", fecha=fecha, tabla="cb_configuracion",
                     identificador=a.id)
        super().insert(b)
        return a

    def delete_update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico configuracion.", fecha=fecha, tabla="cb_configuracion",
                     identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip, estado):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó configuracion.", fecha=fecha, tabla="cb_configuracion",
                     identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

class FinancieroManager(SuperManager):
    def __init__(self, db):
        super().__init__(Financiero, db)

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        a= dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))
        return a
    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro financiero.", fecha=fecha, tabla="cb_financiero",
                     identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico financiero.", fecha=fecha, tabla="cb_financiero",
                     identificador=a.id)
        super().insert(b)
        return a

    def delete_update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico financiero.", fecha=fecha, tabla="cb_financiero",
                     identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip, estado):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó configuracion.", fecha=fecha, tabla="cb_configuracion",
                     identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
