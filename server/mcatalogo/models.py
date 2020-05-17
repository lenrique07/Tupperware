from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, BigInteger, Text, Time
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime


from ..database.models import Base
from ..database.serializable import Serializable
from sqlalchemy.ext.hybrid import hybrid_property

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class Producto(Serializable, Base):
    way = {}

    __tablename__ = 'cb_producto'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=True)
    codigo = Column(Integer, nullable=False)
    codvta = Column(String(10), nullable=False)
    precio = Column(Float, nullable=False)
    prepro = Column(Float, nullable=False)
    retail = Column(Integer, nullable=False)
    bonifi = Column(Float, nullable=False)
    impini = Column(Float, nullable=True)
    impfin = Column(Float, nullable=True)
    gesini = Column(Integer, nullable=True)
    gesfin = Column(Integer, nullable=True)
    semini = Column(Integer, nullable=True)
    semfin = Column(Integer, nullable=True)
    TipoProducto = Column(Integer, nullable=True)
    foto = Column(MEDIUMTEXT, nullable=True, default=" ")
    gestion = Column(Integer, nullable=True)
    catalogo = Column(Integer,ForeignKey("cb_catalogo.id"),nullable=True)
    pagina = Column(Integer, ForeignKey('cb_pagina.id'))
    orden = Column(Integer, nullable=True)
    remplazo = Column(Integer, ForeignKey("cb_producto.id"),nullable=True)
    enabled = Column(Boolean, default=True)


class Catalogo(Serializable, Base):
    way = {'paginas': {}}
    __tablename__ = 'cb_catalogo'
    id = Column(Integer, primary_key=True)
    Gestion = Column(Integer, nullable=True)
    FechaInicio = Column(Date, nullable=False)
    FechaFinal = Column(Date, nullable=False)
    Numerocatalogo = Column(String(50), nullable=False)
    NumeroPaginas = Column(Integer, nullable=False)
    Estado = Column(Boolean, nullable=False)
    portada = Column(MEDIUMTEXT, nullable=True, default=" ")
    enabled = Column(Boolean, default=True)

    paginas = relationship('Pagina', cascade="save-update, merge, delete, delete-orphan")

class Pagina(Serializable, Base):
    way = {'catalogo': {},'producto':{}}

    __tablename__ = 'cb_pagina'
    id = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False)
    portada = Column(MEDIUMTEXT, nullable=True, default=" ")
    enabled = Column(Boolean, default=True)
    fkcatalogo = Column(Integer, ForeignKey("cb_catalogo.id"),nullable= True)

    catalogo = relationship('Catalogo')
    producto = relationship('Producto')
