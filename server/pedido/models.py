from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, BigInteger, Text, Time
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..mcatalogo.models import Producto
from ..usuarios.models import *

from ..database.models import Base
from ..database.serializable import Serializable
from sqlalchemy.ext.hybrid import hybrid_property
from ..usuarios.models import Usuario

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))

class Pedido(Serializable, Base):
    way = {'detallepedidos': {}}
    __tablename__ = 'cb_pedido'
    id = Column(Integer, primary_key=True)
    noventa =Column(Integer, nullable=False)
    fechavta = Column(Date, nullable=False)
    gestion = Column(Integer, nullable=False)
    semana = Column(Integer, nullable=False)
    unidad = Column(Integer, nullable=False)
    mtoneto = Column(Integer, nullable=False)
    mtoretail = Column(Float, nullable=False)
    cliente = Column(Integer, ForeignKey("cb_usuarios_usuario.cb_usuario_id"), nullable=False)
    usuario = Column(Integer, ForeignKey("cb_usuarios_usuario.cb_usuario_id"), nullable=False)
    codigorol = Column(Integer, nullable=False)

    enabled = Column(Boolean, default=True)
    detallepedidos = relationship("DetallePedido", cascade="save-update, merge, delete, delete-orphan")

class almacen(Serializable,Base):
    way = {'detallepedidos': {}}
    __tablename__ = 'cb_almacen'
    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=True)
    usuario = Column(Integer, ForeignKey("cb_usuarios_usuario.cb_usuario_id"), nullable=False)
    producto = Column(Integer, ForeignKey("cb_producto.id"), nullable=True)
    nombreproducto = Column(String(100) , nullable = True )
    enabled = Column(Boolean, default=True)

class DetallePedido(Serializable, Base):
    way = {'pedido': {}, "asignacionpedido": {}}
    __tablename__ = 'cb_detallepedido'
    id = Column(Integer, primary_key=True)
    codinterno = Column(Integer, nullable=False)
    codigovta = Column(String(50), nullable=False)
    fkpedido = Column(Integer, ForeignKey("cb_pedido.id"))
    fkproducto = Column(Integer, ForeignKey("cb_producto.id"), nullable=True)
    producto = Column(String(100), nullable=False)
    cantidad = Column(Integer, nullable=False)
    preciounitario = Column(Float, nullable=False)
    preciopromotora = Column(Float, nullable=False)
    importeneto = Column(Float, nullable=False)
    enabled = Column(Boolean, default=True)

    pedido = relationship('Pedido')
    asignacionpedido = relationship("AsignacionPedido")


class ClienteFinal(Serializable, Base):
    way = {'usuario': {}}
    __tablename__ = 'cb_clientefinal'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    telefono = Column(Integer, nullable=False)
    fkusuario = Column(Integer, ForeignKey("cb_usuarios_usuario.cb_usuario_id"), nullable=False)
    enabled = Column(Boolean, default=True)


class AsignacionPedido(Serializable, Base):
    way = {'detallepedido': {}, 'clientefinal': {}}
    __tablename__ = 'cb_asignacionpedido'
    id = Column(Integer, primary_key=True)
    fkdetallepedido = Column(Integer, ForeignKey("cb_detallepedido.id"), nullable=False)
    fkclientefinal = Column(Integer, ForeignKey("cb_clientefinal.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    monto = Column(Float, nullable=False)
    enabled = Column(Boolean, default=True)

    detallepedido = relationship('DetallePedido')
    clientefinal = relationship('ClienteFinal')


class Pedido_cliente(Serializable, Base):
        way = {'clientefinal': {}}
        __tablename__ = 'cb_pedido_cliente'
        id = Column(Integer, primary_key=True)
        fechavta = Column(Date, nullable=False)
        montopagar = Column(Float, nullable=False)
        montopagado = Column(Float, nullable=False)
        fkcliente = Column(Integer, ForeignKey("cb_clientefinal.id"), nullable=False)
        enabled = Column(Boolean, default=True)


class detall_pago(Serializable, Base):
    way = { }
    __tablename__ = 'cb_detallepago'
    id = Column(Integer, primary_key=True)
    fkpedido_cliente = Column(Integer, ForeignKey("cb_pedido_cliente.id"))
    fechavta = Column(Date, nullable=False)
    monto = Column(Float, nullable=False)
    enabled = Column(Boolean, default=True)
    pedido_cliente = relationship('Pedido_cliente')
