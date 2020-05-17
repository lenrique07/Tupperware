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
from ..mcatalogo.managers import *
from ..usuarios.managers import *

global image_report
image_report = 'server/common/resources/images/sabsa-xls.png'


class PedidoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Pedido, db)

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_pedido(self,noventa):
        a= self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.noventa == noventa).first()
        return a
    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        try:
            a = super().insert(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Pedido.", fecha=fecha,tabla="cb_pedido", identificador=a.id)
            super().insert(b)
            return a
        except Exception as e:
            print(e)
            return None



    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Pais.", fecha=fecha,tabla="rrhh_pais", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Pais.", fecha=fecha,tabla="rrhh_pais", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()


class AsignacionPedidoManager(SuperManager):
    def __init__(self, db):
        super().__init__(AsignacionPedido, db)

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()


    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        try:
            a = super().insert(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Pedido.", fecha=fecha,tabla="cb_pedido", identificador=a.id)
            super().insert(b)
            return a
        except Exception as e:
            print(e)
            e=None
            return e



    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Pais.", fecha=fecha,tabla="rrhh_pais", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Pais.", fecha=fecha,tabla="rrhh_pais", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

class ClienteFinalManager(SuperManager):
    def __init__(self, db):
        super().__init__(ClienteFinal, db)

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def get_all_by_promotora(self, promotora):
        promotora = self.db.query(self.entity).filter(self.entity.fkusuario == promotora).all()
        return promotora

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        try:
            a = super().insert(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Pedido.", fecha=fecha,tabla="cb_pedido", identificador=a.id)
            super().insert(b)
            return a
        except Exception as e:
            print(e)
            return e

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Pais.", fecha=fecha,tabla="rrhh_pais", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Pais.", fecha=fecha,tabla="rrhh_pais", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

class DetallePedidoManager(SuperManager):
    def __init__(self, db):
        super().__init__(DetallePedido, db)
    def listar_detalle(self, fkpedido):
        a = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkpedido == fkpedido).all()
        return a
    def listar_unidad(self, detalle):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.id == detalle).first()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        try:
            a = super().insert(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Pedido.", fecha=fecha,
                         tabla="cb_pedido", identificador=a.id)
            super().insert(b)
            return a
        except Exception as e:
            return e

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Pais.", fecha=fecha,tabla="rrhh_pais", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Pais.", fecha=fecha,tabla="rrhh_pais", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

class Pedido_clienteManager(SuperManager):
    def __init__(self, db):
        super().__init__(Pedido_cliente, db)

    def listar_unidad(self, detalle):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.id == detalle).first()

    def listar_cliente(self, cliente):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.fkcliente == cliente).first()



    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insertar_duda(self,cliente):
        try:
            fecha = BitacoraManager(self.db).fecha_actual()
            b = Pedido_cliente(montopagar= 0, montopagado=0, fkcliente=cliente, fechavta=fecha)
            super().insert(b)
        except Exception as e:
            print(e)
    def actualizar_deuda(self,objeto):
        a = super().update(objeto)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        try:
            a = super().insert(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Pedido.", fecha=fecha,
                         tabla="cb_pedido", identificador=a.id)
            super().insert(b)
            return a
        except Exception as e:
            return e

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Pais.", fecha=fecha, tabla="rrhh_pais",
                     identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Pais.", fecha=fecha, tabla="rrhh_pais",
                     identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

class detall_pagoManager(SuperManager):
    def __init__(self, db):
        super().__init__(detall_pago, db)

    def listar_cliente(self, cliente):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.fkcliente == cliente).first()

    def insertar_pagos(self,objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        try:
            a = super().insert(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro detalle_pago.", fecha=fecha,
                         tabla="cb_detall_pago", identificador=a.id)
            super().insert(b)
            return a
        except Exception as e:
            return e

    def actualizar_deuda(self,objeto):
        a = super().update(objeto)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        try:
            a = super().insert(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Pedido.", fecha=fecha,
                         tabla="cb_pedido", identificador=a.id)
            super().insert(b)
            return a
        except Exception as e:
            return e

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Pais.", fecha=fecha, tabla="rrhh_pais",
                     identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Pais.", fecha=fecha, tabla="rrhh_pais",
                     identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

class AlmacenManager(SuperManager):
    def __init__(self, db):
        super().__init__(almacen, db)

    def list_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).first()

    def listar_usuario(self, usuario):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.usuario == usuario).all()


    def validarAsignacion(self, validarAsignacion,pedido,producto,usuario):
        try:
            print(validarAsignacion)
            a = self.db.query(self.entity).filter(self.entity.enabled == True).filter(
                self.entity.usuario == usuario).filter(self.entity.nombreproducto == producto).first()
            cantidad = a.cantidad - validarAsignacion['cantidad']
            b = almacen(id=a.id, cantidad=cantidad, usuario=usuario, nombreproducto=producto, user=usuario,
                        ip=validarAsignacion['ip'])
            AlmacenManager(self.db).update(b)
        except Exception as e:
            print(e)

    def validar(self, usuario,producto,ip,cantidad):
        try:
            a = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.usuario == usuario).filter(self.entity.nombreproducto == producto).first()

            id = ProductoManager(self.db).obtener_x_nombre(producto)
            id = id.id
            if a == None :
                b = almacen(cantidad=cantidad,usuario=usuario,nombreproducto=producto, producto= id,user=usuario,ip=ip)
                AlmacenManager(self.db).insert(b)
            else:
                print(a)
                cantidad = a.cantidad + cantidad
                b= almacen(id=a.id,cantidad=cantidad,usuario=usuario,nombreproducto=producto, producto= id,user=usuario,ip=ip,enabled=True)
                AlmacenManager(self.db).update(b)
        except Exception as e:
            print(e)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        try:
            a = super().insert(objeto)
            b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro de almacen.", fecha=fecha,
                         tabla="cb_almacen", identificador=a.id)
            super().insert(b)
            return a
        except Exception as e:
            return e

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico almacen.", fecha=fecha, tabla="cb_almacen",
                     identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Pais.", fecha=fecha, tabla="rrhh_pais",
                     identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
