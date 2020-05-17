from tornado.web import authenticated
from tornado.gen import coroutine

from server.common.utils import decorators
from ..common.controllers import SuperController
from ..usuarios.managers import *

from ..common.controllers import CrudController, SuperController, ApiController
from ..common import globals


class Index(SuperController):
    @decorators(authenticated, coroutine)
    def get(self):
        try:
            usuario = self.get_user()
            if usuario:
                self.render("main/index.html", user=usuario)
            else:
                self.redirect('/logout')
        except Exception as e:
            print(e)
            self.redirect('/logout')
