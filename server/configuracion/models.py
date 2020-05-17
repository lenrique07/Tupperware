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


class Configuracion(Serializable, Base):
    way = {}

    __tablename__ = 'cb_configuracion'
    id = Column(Integer, primary_key=True)
    video = Column(MEDIUMTEXT, nullable=True)
    facebook =  Column(MEDIUMTEXT, nullable=True)
    pagina = Column(MEDIUMTEXT, nullable=False)
    twitter = Column(MEDIUMTEXT, nullable=False)
    otro = Column(MEDIUMTEXT, nullable=False)
    enabled = Column(Boolean, default=True)

class Financiero(Serializable, Base):
    way = {}

    __tablename__ = 'cb_financiero'
    id = Column(Integer, primary_key=True)
    nombre = Column(MEDIUMTEXT, nullable=True)
    imagen = Column(MEDIUMTEXT, nullable=True, default=" ")
    enabled = Column(Boolean, default=True)
