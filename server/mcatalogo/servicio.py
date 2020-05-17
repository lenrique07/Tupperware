import base64
from tornado.gen import coroutine

from server.mcatalogo.models import Catalogo
from .managers import *
from ..usuarios.managers import *
from ..operaciones.managers import *
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from ..common.controllers import CrudController, SuperController, ApiController
from ..usuarios.managers import *
from ..pedido.managers import *
from server.configuracion.managers import *
from server.mcatalogo.managers import PaginaManager
import json
import requests
api_reporte ="http://181.115.203.250:4040/api/Reportes/"
api= "http://181.115.203.250:4040/api/"

class ApiProductoController(ApiController):
    manager = ProductoManager

    routes = {
        '/api/v1/listar_niveles': {'POST': 'listar_niveles'},
        '/api/v1/listar_promociones': {'POST': 'listar_promociones'},
        '/api/v1/listar_oferta': {'POST': 'listar_oferta'},
        '/api/v1/listar_producto': {'POST': 'listar_producto'},
        '/api/v1/iniciar_sesion': {'POST': 'iniciar_session'},
        '/api/v1/editar_perfil': {'POST': 'editar_perfil'},
        '/api/v1/listar_catalogo': {'POST': 'listar_catalogo'},
        '/api/v1/listar_pagina': {'POST': 'listar_pagina'},
        '/api/v1/insertar_pedido': {'POST': 'insertar_pedido'},
        '/api/v1/listar_pedido': {'POST': 'listar_pedido'},
        '/api/v1/listar_detallepedido': {'POST': 'listar_detallepedido'},
        '/api/v1/listar_asignacion': {'GET': 'listar_asignacion'},
        '/api/v1/listar_cliente': {'POST': 'listar_cliente'},
        '/api/v1/insertar_cliente': {'POST': 'insertar_cliente'},
        '/api/v1/listar_usuarios': {'POST': 'listar_usuarios'},
        '/api/v1/insertar_asignarpedido': {'POST': 'insertar_asignarpedido'},
        '/api/v1/insertar_detallepago': {'POST': 'insertar_detallepago'},
        '/api/v1/redes': {'POST': 'redes'},
        '/api/v1/listar_redes': {'GET': 'listar_redes'},
        '/api/v1/listar_deuda': {'POST': 'listar_deuda'},
        '/api/v1/reporte': {'POST': 'listar_reporte'},
        '/api/v1/listar_financiero': {'GET': 'listar_financiero'},
        '/api/v1/api': {'POST': 'api_servicio'},
        '/api/v1/listar_cantidad': {'POST': 'listar_cantidad'},
    }

    def listar_reporte(self):
        try:
            response = []
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            ruta = data['ruta']
            datos = data['body']
            self.set_session()
            url = api_reporte + ruta
            headers = {'Content-Type': 'application/json'}
            string = dict()
            cadena = json.dumps(string)
            body = cadena
            data = json.dumps(datos)
            resp = requests.put(url, data=data, headers=headers, verify=False)
            texto = resp.text
            response = json.dumps(texto)
            self.respond(response=response, success=True, message="lista de producto recuperados correctamente.")
        except Exception as e:
            print(e)
            response = e
            self.respond(response=response, success=True, message="error:" + str(e))
        self.db.close()


    def api_servicio(self):
        try:
            response = []
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            ruta = data['ruta']
            datos = data['body']
            self.set_session()
            url = api + ruta
            headers = {'Content-Type': 'application/json'}
            string = dict()
            cadena = json.dumps(string)
            body = cadena
            data = json.dumps(datos)
            resp = requests.put(url, data=data, headers=headers, verify=False)
            response = resp
            self.respond(response=response, success=True, message="lista de producto recuperados correctamente.")
        except Exception as e:
            print(e)
            response = e
            self.respond(response=response, success=True, message="error:" + str(e))
        self.db.close()
    def check_xsrf_cookie(self):
        return
    def listar_usuarios(self):
        usuarios = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            usuario = UsuarioManager(self.db).listar_usuario_5(data['rol']+1)
            for response in usuario['objects']:
                diccionary = dict(
                    id=response.id,
                    sobrenombre=response.sobrenombre,
                    foto=response.foto,
                    nombre=response.nombre,
                    apellido=response.apellido,
                    correo=response.correo,
                    username=response.username,
                    password=response.password,
                    telefono=response.telefono,
                    unidad=response.unidad,
                    distrito=response.distrito,
                    fkrol=response.fkrol-1,
                )
                usuarios.append(diccionary)
            longitud = len(usuarios)
            self.respond(response=usuarios, success=True, message='la lista de usuario son '+str(longitud)+'.')
        except Exception as e:
            print(e)
            self.respond(response=0, success=True, message="error:" + str(e))
        self.db.close()
    def iniciar_session(self):
        response = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            username = data['username']
            password = data['password']
            result = UsuarioManager(self.db).login_Usuario_servicio(username, password)
            usuario = result['objects']
            for user in result['objects']:
                dic = dict(id=user.id,
                           sobrenombre=user.sobrenombre,
                           nombre=user.nombre,
                           apellido=user.apellido,
                           correo=user.correo,
                           username=user.username,
                           telefono=user.telefono,
                           unidad=user.unidad,
                           distrito=user.distrito,
                           fkrol=user.fkrol,
                           enabled=user.enabled,
                           foto=user.foto,
                           rol=user.rol.id
                           )
                response.append(dic)

            if len(response) != 0:
                self.respond(response=response, success=True, message='Inicio session correctamente.')
            else:
                self.respond(response=0, success=False, message="No se encontro el usuario")
        except Exception as e:
            print(e)
            self.respond(response=response, success=False, message="error:"+str(e))
        self.db.close()
    def editar_perfil(self):
        usuarios = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            usuario = UsuarioManager(self.db).servicio_usuario(data)
            response = UsuarioManager(self.db).update(usuario)
            diccionary = dict(
                id=response.id,
                sobrenombre = response.sobrenombre,
                foto = response.foto,
                nombre=response.nombre,
                apellido=response.apellido,
                correo=response.correo,
                username=response.username,
                password=response.password,
                telefono=response.telefono,
                unidad=response.unidad,
                distrito=response.distrito,
                fkrol=response.fkrol,
                user=response.user, # Cambiar, esta por defecto administrador
                ip=response.ip,
            )
            usuarios.append(diccionary)
            if response != None:
                self.respond(response=usuarios, success=True, message='Se edito el usuario correctamente.')
            else:
                self.respond(response=0, success=False, message="No se pudo editar el usuario")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:" + str(e))
        self.db.close()
    def listar_producto(self):
        response = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            Gestion = data['gestion']
            catalogos = data['catalogo']
            self.set_session()
            catalogo = CatalogoManager(self.db).catalogo(Gestion,catalogos)
            result = self.manager(self.db).list_producto_catalogo(Gestion,catalogo)
            for producto in result['objects']:
                dic = dict(id=producto.id,
                           nombre=producto.nombre,
                           codigo=producto.codigo,
                           codvta=producto.codvta,
                           precio=producto.precio,
                           prepro=producto.prepro,
                           bonifi=producto.bonifi,
                           retail=producto.retail,
                           impini=producto.impini,
                           impfin=producto.impfin,
                           gesini=producto.gesini,
                           gesfin=producto.gesfin,
                           semini=producto.semini,
                           semfin=producto.semfin,
                           TipoProducto=producto.TipoProducto,
                           foto=producto.foto,
                           catalogo=catalogos,
                           pagina=producto.pagina
                           )
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="lista de producto recuperados correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    def listar_niveles(self):
        response = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            Gestion = data['gestion']
            catalogos = data['catalogo']
            self.set_session()
            catalogo = CatalogoManager(self.db).catalogo(Gestion, catalogos)
            result = self.manager(self.db).list_all_niveles(Gestion, catalogo)
            for producto in result['objects']:
                dic = dict(id=producto.id,
                           nombre=producto.nombre,
                           codigo=producto.codigo,
                           codvta=producto.codvta,
                           precio=producto.precio,
                           prepro=producto.prepro,
                           bonifi=producto.bonifi,
                           retail=producto.retail,
                           impini=producto.impini,
                           impfin=producto.impfin,
                           gesini=producto.gesini,
                           gesfin=producto.gesfin,
                           semini=producto.semini,
                           semfin=producto.semfin,
                           TipoProducto=producto.TipoProducto,
                           foto=producto.foto)
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="lista de niveles recuperados correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    def listar_promociones(self):
        response = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            Gestion = data['gestion']
            catalogos = data['catalogo']
            self.set_session()
            catalogo = CatalogoManager(self.db).catalogo(Gestion, catalogos)
            result = self.manager(self.db).list_all_promocion(Gestion,catalogo)
            for producto in result['objects']:
                dic = dict(id=producto.id,
                           nombre=producto.nombre,
                           codigo=producto.codigo,
                           codvta=producto.codvta,
                           precio=producto.precio,
                           prepro=producto.prepro,
                           bonifi=producto.bonifi,
                           retail=producto.retail,
                           gesini=producto.gesini,
                           gesfin=producto.gesfin,
                           semini=producto.semini,
                           semfin=producto.semfin,
                           TipoProducto=producto.TipoProducto,
                           foto=producto.foto)
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="lista de promociones recuperados correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    def listar_oferta(self):
        response = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            Gestion = data['gestion']
            catalogos = data['catalogo']
            self.set_session()
            catalogo = CatalogoManager(self.db).catalogo(Gestion, catalogos)
            result = self.manager(self.db).list_all_oferta(Gestion,catalogo)
            for producto in result['objects']:
                dic = dict(id=producto.id,
                           nombre=producto.nombre,
                           codigo=producto.codigo,
                           codvta=producto.codvta,
                           precio=producto.precio,
                           prepro=producto.prepro,
                           bonifi=producto.bonifi,
                           retail=producto.retail,
                           impini=producto.impini,
                           impfin=producto.impfin,
                           gesini=producto.gesini,
                           gesfin=producto.gesfin,
                           semini=producto.semini,
                           semfin=producto.semfin,
                           TipoProducto=producto.TipoProducto,
                           foto=producto.foto)
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="lista de ofertas recuperados correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    def listar_catalogo(self):
        response = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            Gestion = data['gestion']
            catalogos = data['catalogo']
            self.set_session()
            result = CatalogoManager(self.db).listar_catalogo(Gestion, catalogos)
            for lista in result['objects']:
                dic = dict(
                id=lista.id,
                Gestion=lista.Gestion,
                FechaInicio=str(lista.FechaInicio),
                FechaFinal=str(lista.FechaFinal),
                Numerocatalogo=lista.Numerocatalogo,
                NumeroPaginas=lista.NumeroPaginas,
                Estado=lista.Estado,
                portada=lista.portada,
                enabled=lista.enabled,)
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="Catalogo  recuperadas correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    def listar_pagina(self):
        response = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            Gestion = data['gestion']
            catalogos = data['catalogo']
            self.set_session()
            catalogo = CatalogoManager(self.db).catalogo(Gestion, catalogos)
            result = PaginaManager(self.db).listar_paginas(catalogo)
            for lista in result['objects']:
                dic = dict(id=lista.id,
                           numero=lista.numero,
                           portada=lista.portada,
                           fkcatalogo=lista.fkcatalogo,
                           enabled=lista.enabled
                           )
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="lista de paginas recuperadas correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    # Inserta un pedido
    def insertar_pedido(self):
        response = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            listapedidos = list()
            pedidoDict = data['Venta']
            usuario = pedidoDict['usuario']
            cliente = pedidoDict['cliente']
            usuario= UsuarioManager(self.db).sacar_id(usuario)
            cliente = UsuarioManager(self.db).sacar_id(cliente)
            diccionaryPedido = dict(usuario=usuario,
                                    codigorol=pedidoDict['codigorol'],
                                    noventa=pedidoDict['noventa'],
                                    fechavta=pedidoDict['fechavta'],
                                    gestion=pedidoDict['gestion'],
                                    semana=pedidoDict['semana'],
                                    unidad=pedidoDict['unidad'],
                                    cliente=cliente,
                                    mtoneto=pedidoDict['mtoneto'],
                                    mtoretail=pedidoDict['mtoretail'],
                                    user=usuario,  # Cambiar, esta por defecto administrador
                                    ip=pedidoDict['ip']
                                    )
            for dv in data['DetalleVenta']:
                listapedidos.append(dict(
                    codinterno=dv['codinterno'],
                    codigovta=dv['codigovta'],
                    producto=dv['producto'],
                    preciounitario=float(dv['preciounitario']),
                    preciopromotora=dv['preciopromotora'],
                    importeneto=dv['importeneto'],
                    cantidad=dv['cantidad']
                ))
                AlmacenManager(self.db).validar(usuario,dv['producto'],pedidoDict['ip'],dv['cantidad'])
            diccionaryPedido['detallepedidos'] = listapedidos
            objeto = PedidoManager(self.db).entity(**diccionaryPedido)
            PedidoManager(self.db).insert(objeto)
            #response.append(PedidoManager(self.db).list_all())
            response = objeto.get_dict()
            if len(response) != 0:
                self.respond(response=response, success=True, message='Pedido insertado correctamente.')
            else:
                self.respond(response=0, success=False, message="No se encontro el pedido")
        except Exception as e:
            print(e)
            self.respond(response=0, success=False, message="error:"+str(e))
        self.db.close()
    # Lista todos los pedidos
    def listar_pedido(self):
        response = []
        listapedidos = list()
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            noventa = data['noventa']
            self.set_session()
            pedido = PedidoManager(self.db).listar_pedido(noventa)
            usuario = UsuarioManager(self.db).sacar_codigo(pedido.usuario)
            cliente = UsuarioManager(self.db).sacar_codigo(pedido.cliente)
            dic = dict(
                id=pedido.id,
                codigorol=pedido.codigorol,
                fechavta=str(pedido.fechavta),
                gestion=pedido.gestion,
                semana=pedido.semana,
                unidad=pedido.unidad,
                cliente=cliente,
                mtoneto=pedido.mtoneto,
                mtoretail=pedido.mtoretail,
                fkusuario=usuario,
                noventa=noventa
            )
            response.append(dic)
            for detalle in pedido.detallepedidos:
                listapedidos.append(dict(
                    id=detalle.id,
                    codinterno=detalle.codinterno,
                    codigovta=detalle.codigovta,
                    fkpedido=detalle.fkpedido,
                    preciounitario=detalle.preciounitario,
                    preciopromotora=detalle.preciopromotora,
                    importeneto=detalle.importeneto,
                    cantidad=detalle.cantidad,
                    producto=detalle.producto
                ))

                dic['detallepedidos'] = listapedidos
            self.db.close()
            self.respond(response=dic, success=True, message="Lista de pedidos recuperados correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    # listar detalle del pedido
    def listar_detallepedido(self):
        response = []
        listapedidos = list()
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            noventa = data['noventa']
            self.set_session()
            pedido = PedidoManager(self.db).listar_pedido(noventa)
            fkpedido = pedido.id
            detalles = DetallePedidoManager(self.db).listar_detalle(fkpedido)
            dic = dict()
            for detalle in detalles:
                listapedidos.append(dict(
                    id=detalle.id,
                    codinterno=detalle.codinterno,
                    codigovta=detalle.codigovta,
                    fkpedido=detalle.fkpedido,
                    preciounitario=detalle.preciounitario,
                    preciopromotora=detalle.preciopromotora,
                    importeneto=detalle.importeneto,
                    cantidad=detalle.cantidad,
                    producto=detalle.producto
                ))

                dic['detallepedidos'] = listapedidos
            self.db.close()
            self.respond(response=dic, success=True, message="Lista de pedidos recuperados correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    # Lista todas las asignaciones
    def listar_asignacion(self):
        response = []
        self.set_session()
        try:
            result = AsignacionPedidoManager(self.db).list_all()
            for asignacion in result['objects']:
                dic = dict(
                    id=asignacion.id,
                    fkdetallepedido=asignacion.fkdetallepedido,
                    fkclientefinal=asignacion.fkclientefinal,
                )
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="Lista de asignaciones recuperados correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=0, success=False, message="error:" + e)
        self.db.close()
    # Lista todas los clientes
    def listar_cliente(self):
        response = []
        data = json.loads(self.request.body.decode('utf-8'))
        promotora = data['promotora']
        self.set_session()
        try:
            result = ClienteFinalManager(self.db).get_all_by_promotora(promotora)
            for clientefinal in result:
                dic = dict(
                    id=clientefinal.id,
                    nombre=clientefinal.nombre,
                    apellido=clientefinal.apellido,
                    email=clientefinal.email,
                    telefono=clientefinal.telefono,
                    fkusuario=clientefinal.fkusuario

                )
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="Lista de cliente finales recuperados correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    def listar_deuda(self):
        response = []
        data = json.loads(self.request.body.decode('utf-8'))
        try:
            cliente = data['fkcliente']
            self.set_session()
            pedido = Pedido_clienteManager(self.db).listar_cliente(cliente)
            montoapagar =pedido.montopagar
            montopagado = pedido.montopagado
            dic = dict(
                id=pedido.id,
                fkcliente=pedido.fkcliente,
                montoapagar=montoapagar,
                montopagado=montopagado,
                deuda = montoapagar - montopagado
            )
            response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="Lista de cliente finales recuperados correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    # Inserta cliente final
    def insertar_cliente(self):
        response = []
        print(self.request.body)
        data = json.loads(self.request.body.decode('utf-8'))
        self.set_session()
        try:
            data = json.loads(self.request.body.decode('utf-8'))

            response = []
            self.set_session()
            dic = dict(
                nombre=data['nombre'],
                apellido=data['apellido'],
                email=data['email'],
                telefono=data['telefono'],
                fkusuario=data['promotora'],
                usuario=data['promotora'],
                enabled=1,
                user=data['promotora'],
                ip=data['ip'],
            )
            response.append(dic)
            objeto = ClienteFinalManager(self.db).entity(**dic)
            respuesta = self.manager(self.db).insert(objeto)
            cliente = respuesta.id
            Pedido_clienteManager(self.db).insertar_duda(cliente)
            if respuesta is not None:
                self.respond(response=dic, success=True, message='Cliente insertado correctamente.')
            else:
                self.respond(response=0, success=False, message="Error al encontrar el usuario")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    # Inserta una AsignacionPedido
    def insertar_asignarpedido(self):
        response = []
        data = json.loads(self.request.body.decode('utf-8'))
        self.set_session()
        try:
            detalle= data['idDetallePedido']
            preciounidad = DetallePedidoManager(self.db).listar_unidad(detalle)
            clientefianl= data['idClienteFinal']
            diccionary = dict(
                fkdetallepedido=data['idDetallePedido'],
                fkclientefinal=clientefianl,
                cantidad=data['cantidad'],
                user=data['user'],  # Cambiar, esta por defecto administrador
                ip=data['ip'],
                monto = data['cantidad'] *preciounidad.preciounitario
            )
            pedido = preciounidad.pedido
            AlmacenManager(self.db).validarAsignacion(diccionary,preciounidad.fkpedido,preciounidad.producto,pedido.usuario)
            monto =  data['cantidad'] *preciounidad.preciounitario
            response.append(diccionary)
            objeto = AsignacionPedidoManager(self.db).entity(**diccionary)
            resp = AsignacionPedidoManager(self.db).insert(objeto)
            pedido=Pedido_clienteManager(self.db).listar_cliente(clientefianl)
            pedido.montopagar = pedido.montopagar+monto
            Pedido_clienteManager(self.db).actualizar_deuda(pedido)
            # response = objeto.get_dict()
            if resp != None:
                self.respond(response=response, success=True, message='AsignacionPedido insertado correctamente.')
            else:
                self.respond(response=0, success=False, message="No se encontro el pedido")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    def insertar_detallepago(self):
        response = []
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            cliente = data['cliente']
            fkpedido_cliente = Pedido_clienteManager(self.db).listar_cliente(cliente)
            fechavta = fecha_zona
            diccionary = dict(
                fkpedido_cliente=fkpedido_cliente.id,
                fechavta=fechavta,
                monto=data['monto'],
                user=data['user'],  # Cambiar, esta por defecto administrador
                ip=data['ip'],
            )
            monto=data['monto']
            response.append(diccionary)
            objeto = detall_pagoManager(self.db).entity(**diccionary)
            resp = detall_pagoManager(self.db).insert(objeto)
            fkpedido_cliente.montopagado = fkpedido_cliente.montopagado + monto
            Pedido_clienteManager(self.db).actualizar_deuda(fkpedido_cliente)
            diccionary = dict(
                fkpedido_cliente=fkpedido_cliente.id,
                fechavta=fechavta,
                monto=str(data['monto']),
                user=data['user'],  # Cambiar, esta por defecto administrador
                ip=data['ip'],
            )
            response.append(diccionary)
            # response = objeto.get_dict()
            if response != None:
                self.respond(response=response, success=True, message='AsignacionPedido insertado correctamente.')
            else:
                self.respond(response=0, success=False, message="No se encontro el pedido")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    def listar_redes(self):
        response = []
        try:
            self.set_session()
            redes = ConfiguracionManager(self.db).get_all()
            for lista in redes:
                dic = dict(id=lista.id,
                       video=lista.video,
                       facebook=lista.facebook,
                       pagina=lista.pagina,
                       twitter = lista.twitter,
                       otro=lista.otro,
                       enabled=lista.enabled,
                           )
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="lista recuperadas correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()
    def listar_financiero(self):
        response = []
        try:
            self.set_session()
            redes = FinancieroManager(self.db).get_all()
            for lista in redes:
                dic = dict(id=lista.id,
                       nombre=lista.nombre,
                       imagen = lista.imagen,
                       enabled=lista.enabled,
                           )
                response.append(dic)
            self.db.close()
            self.respond(response=response, success=True, message="lista recuperadas correctamente.")
        except Exception as e:
            print(e)
            self.respond(response=response, success=True, message="error:"+str(e))
        self.db.close()

    def listar_cantidad(self):
        try:
            response = []
            data = json.loads(self.request.body.decode('utf-8'))
            self.set_session()
            usuario = data['usuario']
            usuario = UsuarioManager(self.db).sacar_id(usuario)
            respon = AlmacenManager(self.db).listar_usuario(usuario)
            for r in respon:
                dic = dict(id=r.id,
                           cantidad=r.cantidad,
                           nombreproducto=r.nombreproducto,
                           usuario=r.usuario,
                           producto=r.producto,
                           enabled=r.enabled,
                           )
                response.append(dic)
            self.respond(response=response, success=True, message="lista de producto recuperados correctamente.")
        except Exception as e:
            print(e)
            response = e
            self.respond(response=response, success=False, message="error:" + str(e))
        self.db.close()
