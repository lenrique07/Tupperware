from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, BigInteger, Text, Time
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime


from ..database.models import Base
from ..database.serializable import Serializable
from sqlalchemy.ext.hybrid import hybrid_property

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class AyudaVentas(Serializable, Base):
    way = {}

    __tablename__ = 'cb_ayudaventas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=True)
    codigo = Column(Integer,  unique=True, nullable=False)
    codvta = Column(String(10), nullable=False)
    precio = Column(Float, nullable=False)
    prepro = Column(Float, nullable=False)
    retail = Column(Integer, nullable=False)
    bonifi = Column(Float, nullable=False)
    gestion = Column(Integer, nullable=True)
    catalogo = Column(Integer, ForeignKey("cb_catalogo.id"))
    foto = Column(Text, nullable=True, default=" ")
    enabled = Column(Boolean, default=True)
