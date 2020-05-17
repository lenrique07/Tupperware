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
from ..pedido.models import Pedido
from sqlalchemy import desc

from ..usuarios.managers import *

global image_report
image_report = 'server/common/resources/images/sabsa-xls.png'


class ProductoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Producto, db)

    def validarProducto(self,objeto):
      obj = []
      for producto in objeto:
        prod =""
        prod = self.db.query(self.entity).\
            filter(self.entity.nombre == producto['nombre']).\
            filter(self.entity.codigo == producto['codigo']).\
            filter(self.entity.catalogo == producto["catalogo"]).\
            filter(self.entity.gestion == producto["gestion"]).all()
        if prod == []:
          obj.append(producto)
      return obj

    def validarniveles(self, objeto, tipo):
      obj = []
      for producto in objeto:
        prod =""
        prod = self.db.query(self.entity).\
            filter(self.entity.nombre == producto['nombre']).\
            filter(self.entity.codigo == producto['codigo']).\
            filter(self.entity.semini == producto["semini"]).\
            filter(self.entity.semfin == producto["semfin"]).\
            filter(self.entity.gesini == producto["gesini"]).\
            filter(self.entity.gesfin == producto["gesfin"]).\
            filter(self.entity.TipoProducto == tipo).first()
        if prod == None:
          obj.append(producto)
      return obj

    def lista_vacio(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.TipoProducto == 10))

    def get_producto(self,ids):
        prod = self.db.query(self.entity).filter(self.entity.pagina == ids).first()
        return prod

    def get_producto_by_id(self, ids):
        prod = self.db.query(self.entity).filter(self.entity.id == ids).first()
        return prod

    def get_by_gestion(self, gestion):
        return self.db.query(self.entity).filter(self.entity.Gestion == gestion).filter(self.entity.enabled == True).all()

    def get_by_cat(self, catalogo):
        return self.db.query(self.entity).filter(self.entity.catalogo == catalogo).filter(self.entity.enabled == True).all()

    def get_tipoProd_by_semana(self, semini, tipoproducto):
        return self.db.query(self.entity).filter(self.entity.semini == semini).filter(self.entity.TipoProducto == tipoproducto).filter(self.entity.enabled == True).all()

    # Devuelve los productos por la gestion, el id de catalogo y el tipo de producto
    def get_producto_by_catalogo(self, gestion, catalogo, tipoproducto):
        a = self.db.query(self.entity).filter(self.entity.catalogo == catalogo).\
            filter(self.entity.gestion == gestion).\
            filter(self.entity.TipoProducto == tipoproducto).\
            filter(self.entity.enabled == True).all()
        return a


    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def obtener_x_id(self, id):
        return self.db.query(self.entity).filter(self.entity.id == id).first()


    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.TipoProducto == 1).all()

    def list_producto(self):
      return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
        self.entity.TipoProducto == 1))

    def list_producto_catalogo(self,gestion , catalogo):

        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.TipoProducto == 1).filter(self.entity.gestion == gestion)
	.filter(self.entity.catalogo == catalogo).all())


    def get_all_productos_by_idPagina(self, id):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.pagina == id).all())

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.TipoProducto == 1))
    def lista_vacio(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.TipoProducto == 0))

    
    def list_all_productos_index(self, gestion, cat_id, tipo_producto):
        a = self.db.query(self.entity).filter(self.entity.enabled == True).\
            filter(self.entity.TipoProducto == tipo_producto).\
            filter(self.entity.gestion == gestion).\
            filter(self.entity.catalogo == cat_id).all()
        return dict(objects=a)

    def list_all_niveles(self,gestion , catalogo):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.TipoProducto == 2).filter(self.entity.gestion == gestion)
                    .filter(self.entity.catalogo == catalogo).all())

    def listar_tipo(self,tipo):
        a =  dict(objects=self.db.query(self.entity).filter(
            self.entity.TipoProducto == tipo).all())
        return a

    def list_all_promocion(self,gestion , catalogo):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.TipoProducto == 3).filter(self.entity.gestion == gestion)
                    .filter(self.entity.catalogo == catalogo).all())

    def list_all_oferta(self,gestion , catalogo):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.TipoProducto == 4).filter(self.entity.gestion == gestion)
                    .filter(self.entity.catalogo == catalogo).all())

    def list_all_ofertaweb(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True).filter(
            self.entity.TipoProducto == 6).all())


    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Producto.", fecha=fecha,tabla="cb_producto", entificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Producto.", fecha=fecha,tabla="cb_producto", identificador=a.id)
        super().insert(b)
        return a

    def delete_update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Producto.", fecha=fecha, tabla="cb_producto",
                     identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip, estado):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Producto.", fecha=fecha,tabla="cb_producto", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

class NivelManager(SuperManager):
    def __init__(self, db):
        super().__init__(Producto, db)

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def get_by_cat(self, semini):
        return self.db.query(self.entity).filter(self.entity.semini == semini).filter(self.entity.enabled == True).all()

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Nivel.", fecha=fecha,tabla="cb_producto", entificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico un Nivel.", fecha=fecha,tabla="cb_producto", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip, estado):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Nivel.", fecha=fecha,tabla="cb_producto", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()


class CatalogoManager(SuperManager):
    def __init__(self, db):
        super().__init__(Catalogo, db)

    def obtener_x_nombre(self, nombre):
        return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()


    def validarPagina(self, objecto):
      ant = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.id == objecto.id).first()
      ant = ant.NumeroPaginas
      nuevo = int(objecto.NumeroPaginas)
      if nuevo > ant:
        pagina = nuevo-ant
        return dict(paginas = pagina,numero = ant)
      else:
          if  nuevo != ant:
            pagina = nuevo - ant
            return dict(paginas = pagina ,numero = 0)
          else:
              return dict(paginas=0, numero=0)

    def catalogo(self, gestion,catalogo):
      catalogo = str(catalogo)
      catalogos = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.Numerocatalogo == catalogo).filter(self.entity.Gestion == gestion).first()
      cat = catalogos.id
      return cat

    def Numerocatalogo(self, gestion,catalogo):
      catalogo = str(catalogo)
      catalogos = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.Numerocatalogo == catalogo).filter(self.entity.Gestion == gestion).first()
      cat = catalogos.Numerocatalogo
      return cat

    # Devuelve una lista de los catalogos haciendo un distinct por la gestión
    def get_all_distinct(self):
        cat = self.db.query(Catalogo.Gestion).filter(Catalogo.enabled == True).distinct()
        return list(cat)


    def listar_catalogo(self, gestion,catalogo):
        return dict(objects=self.db.query(self.entity).filter(self.entity.Numerocatalogo == catalogo).filter(self.entity.Gestion == gestion).filter(self.entity.enabled == True))

    def validar(self, objeto,mess):
      catalogo = objeto['catalogo']
      gestion = objeto['gestion']
      catalogo = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.Numerocatalogo == mess).filter(self.entity.Gestion == gestion).first()
      objeto['catalogo'] = catalogo.id
      return objeto

    def obtener_registro(self):
        return  self.db.query(self.entity).filter(self.entity.enabled==True).order_by(self.entity.id)

    def get_by_id(self, id):
        cat = self.db.query(self.entity).filter(self.entity.id == id).first()
        return cat

    # Obtener los catalogos de una determinada gestión
    def get_all_cat_by_gestion(self, gestion):
        a = self.db.query(self.entity).filter(self.entity.Gestion == gestion).filter(self.entity.enabled == True).all()
        return a

    # Devuelve el catálogo actual por la fecha actual
    def get_cat_by_fecha_actual(self, FECHA_HOY):
        a = self.db.query(self.entity).filter(self.entity.FechaInicio <= FECHA_HOY).filter(
            self.entity.FechaFinal >= FECHA_HOY).first()
        return a

    def Mostrar_catalogo_actual(self, FECHA_HOY):
        a = dict(objects=self.db.query(self.entity).filter(self.entity.FechaInicio <= FECHA_HOY).filter(
            self.entity.FechaFinal >= FECHA_HOY))
        return a

    def listar_vacio(self):
        a = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.id == 0)
        return dict(objects=a)

    # Obtener el ID de un Catálogo por la gestión y el nro de catálogo
    def get_cat_id(self, gestion, nrocatalogo):
        a = self.db.query(self.entity).filter(self.entity.Gestion == gestion).filter(self.entity.Numerocatalogo >= nrocatalogo).filter(self.entity.enabled == True).first()
        return a

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_por_fecha(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        i_date = datetime.strptime(objeto.FechaInicio, '%d/%m/%Y').date()
        f_date = datetime.strptime(objeto.FechaFinal, '%d/%m/%Y').date()

        objeto.FechaInicio = i_date
        objeto.FechaFinal = f_date
        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Catalogo.", fecha=fecha,
                     tabla="cb_catalogo", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Catalogo.", fecha=fecha,
                     tabla="cb_catalogo", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip, estado):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó Catalogo.", fecha=fecha,
                     tabla="cb_catalogo", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()


class PaginaManager(SuperManager):
    def __init__(self, db):
        super().__init__(Pagina, db)


    def listar_paginas(self,catalogo):
      return dict(objects=self.db.query(self.entity).filter(self.entity.fkcatalogo == catalogo).filter(self.entity.enabled == True))

    def get_numero(self,id):
      try:
        a = self.db.query(self.entity).filter(self.entity.id == id).first()
        return  a.numero
      except Exception as ex:
        return "No hay"

    def get_pagina_by_nroPagina(self, nroPagina, idcatalogo):
        a = self.db.query(self.entity).filter(self.entity.fkcatalogo == idcatalogo).filter(self.entity.numero == nroPagina).first()
        return a

    def obtener_x_nombre(self, nombre):
        try:
            return self.db.query(self.entity).filter(self.entity.nombre == nombre).first()
        except Exception as ex:
            return "No hay"

    def obtener_pagina(self, id):
        list_productos = {}
        c = 0

        pag = self.db.query(self.entity).filter(self.entity.id == id).first()

        productos = self.db.query(Producto).filter(Producto.pagina == id).all()

        for pro in  productos:
            list_productos[c] = dict(nombre=pro.nombre)

            c = c + 1

        pagina = dict(id=pag.id,numero=pag.numero,fkcatalogo=pag.fkcatalogo,nombrecatalogo=pag.catalogo.Mes,productos=list_productos,portada=pag.portada)

        return pagina

    def get_all_productos_by_idPagina(self, id):
      return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))
#     return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.pagina == id).all()

    def get_all_by_id(self, id):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkcatalogo == id).all()

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def get_by_id(self, id):
        pag = self.db.query(self.entity).filter(self.entity.id == id).first()
        return pag

    def productopagina(self,objeto):
      a = self.db.query(self.entity).\
          filter(self.entity.numero == objeto.pagina).\
          filter(self.entity.fkcatalogo == objeto.catalogo).first()
      return a

    def listar_vacio(self):
        a = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkcatalogo == 0)
        return dict(objects=a)

    def list_all_pagina_index(self, id_catalogo):
        a = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkcatalogo == id_catalogo)
        return dict(objects=a)

    def listar_vacio(self):
        a = self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.fkcatalogo == 0)
        return dict(objects=a)

    # Devuelve las páginas de un catálogo determinado
    def get_all_paginas_by_catalogo(self, catalogo):
        a = self.db.query(self.entity).filter(self.entity.fkcatalogo == catalogo).\
            filter(self.entity.enabled == True).all()
        return a


    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.fkcatalogo != None ))

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True)

    def listar_x_departamento(self,iddepartamento):
        return self.db.query(self.entity).filter(self.entity.fkdepartamento == iddepartamento).filter(self.entity.enabled == True)

    def insertar_pagina(self, objeto, i ,numero):
        while i <= numero:
            objeto['numero'] = i
            objet = PaginaManager(self.db).entity(**objeto)
            object = self.many_to_many(objet)
            self.db.add(object)
            i += 1
        self.db.commit()

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=objeto['user'], ip=objeto['ip'], accion="Registro Pagina.", fecha=fecha,
                     tabla="cb_pagina", identificador=objeto['fkcatalogo'])
        super().insert(b)
        print("Programa terminado")
        return objet

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registro Pagina.", fecha=fecha,
                     tabla="cb_pagina", identificador=a.id)
        super().insert(b)
        return a

    def editar_paginas(self, objeto):
        a = super().update(objeto)

    def validar(self, objeto):
        a = self.db.query(self.entity).filter(self.entity.id == objeto['id']).one()
        return a.fkcatalogo

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modifico Pagina.", fecha=fecha,
                     tabla="cb_pagina", identificador=a.id)
        super().insert(b)
        return a

    def delete(self, id, user, ip, estado):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = estado
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó una pagina.", fecha=fecha, tabla="cb_pagina", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()



