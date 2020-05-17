import base64
from tornado.gen import coroutine
from .managers import *
from ..usuarios.managers import *
from ..operaciones.managers import *
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


image_report = "../server/common/resources/images/sabsa.jpg"


class PedidoController(CrudController):

    manager = PedidoManager
    html_index = "pedido/views/pedido/index.html"
    html_table = "pedido/views/pedido/table.html"
    routes = {
        '/pedido': {'GET': 'index', 'POST': 'table'},
        '/pedido_insert': {'POST': 'insert'},
        '/pedido_update': {'PUT': 'edit', 'POST': 'update'},
        '/pedido_delete': {'POST': 'delete'},
    }


    def get_extra_data(self):
        # try:
            aux = super().get_extra_data()
            aux['pedido'] = PedidoManager(self.db).get_all()
            return aux
        # except:
        #     print("Something went wrong")
        # finally:
        #     print("Finalizado")

    def index(self):
        self.set_session()
        self.verif_privileges()
        result = self.manager(self.db).list_all()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PedidoManager(self.db).insert(objeto)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        objeto = self.manager(self.db).entity(**diccionary)
        PedidoManager(self.db).update(objeto)
        self.respond(success=True, message='Modificado correctamente.')
