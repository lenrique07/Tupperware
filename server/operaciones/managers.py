import hashlib
import string
from random import *
import json
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import make_transient
import random
from ..database.connection import transaction
from ..usuarios.models import *
from server.common.managers import SuperManager
from .models import *
from sqlalchemy.sql import func, extract, cast, text
from sqlalchemy import Date
from datetime import datetime, date, time, timedelta
from pyfcm import FCMNotification
import pytz

import uuid
from server.common.managers import Error
from server.database.connection import transaction
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class BitacoraManager(SuperManager):
    def __init__(self, db):
        super().__init__(Bitacora, db)

    def list_all(self):
        return dict(objects=self.db.query(Bitacora).order_by(Bitacora.id.asc()))

    def fecha_actual(self):
        return datetime.now(pytz.timezone('America/La_Paz'))

    def fecha(self):
        return fecha_zona.strftime('%Y/%d/%m')