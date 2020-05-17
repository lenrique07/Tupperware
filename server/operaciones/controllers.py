from tornado.gen import coroutine
from .managers import *
from ..usuarios.managers import *
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from ..common.controllers import CrudController, SuperController, ApiController
from xhtml2pdf import pisa
import os.path

class Report:
    def html_to_pdf(self, sourceHtml, nombre):
        outputFilename = 'server/common/resources/downloads/' + nombre

        resultFile = open(outputFilename, "w+b")
        pisaStatus = pisa.CreatePDF(
            sourceHtml,
            dest=resultFile)
        resultFile.close()

        return pisaStatus.err

global report
report = Report()
global image_report
image_report = "server/common/resources/images/pst.jpg"

class BitacoraController(CrudController):

    manager = BitacoraManager
    html_index = "operaciones/views/bitacora/index.html"
    html_table = "operaciones/views/bitacora/table.html"
    routes = {
        '/bitacora': {'GET': 'index', 'POST': 'table'}
    }