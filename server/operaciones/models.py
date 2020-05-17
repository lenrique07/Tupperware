from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, BigInteger, Text
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database.models import Base
from ..database.serializable import Serializable
import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class Bitacora(Serializable, Base):
    way = {'usuario': {}}

    __tablename__ = 'cb_operaciones_bitacora'

    id = Column('cb_bitacora_id', BigInteger, primary_key=True)
    fkusuario = Column('cb_bitacora_fkusuario', Integer, ForeignKey('cb_usuarios_usuario.cb_usuario_id'), nullable=True)
    ip = Column('cb_bitacora_ip', String(100), nullable=True)
    accion = Column('cb_bitacora_accion', String(200), nullable=True)
    fecha = Column('cb_bitacora_fecha', DateTime, nullable=False, default=fecha_zona)
    tabla = Column('cb_bitacora_tabla', String(200), nullable=True)
    identificador = Column('cb_bitacora_identificador', Integer, nullable=True)

    usuario = relationship('Usuario')
