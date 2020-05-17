validations ={//during, post, range of values
    'ci': [/^[0-9]{1,8}$/, /^[0-9]{6,8}$/, 'Solo se aceptan numeros entre 6 y 8 dígitos.'],
    'celular': [/^[0-9]{1,8}$/, /^[0-9]{8}$/, 'Solo se aceptan numeros de 8 dígitos.'],
    'telefono': [/^[0-9]{1,8}$/, /^[0-9]{7}$/, 'Solo se aceptan numeros de 7 dígitos.'],
    'username': [/^[a-zA-Z0-9_]{1,50}$/,/^[a-zA-Z0-9_]{1,50}$/, 'Solo se acepta texto alfanumerico entre 1 y 50 caracteres.'],
    'password': [/^.{1,25}$/, /^.{8,25}$/, 'La contraseña debe tener 8 caracteres como mínimo y 25 como máximo.'],
    'int32': [/[0-9]+$/, /[0-9]+$/, 'Solo se acepta un número entero positivo.', [0, 2147483647]],
    'int32_signed': [/^-$|-?[0-9]+$/, /-?[0-9]+$/, 'Solo se acepta un número entero.', [-2147483648, 2147483647]],
    'float': [/-$|^-?[0-9]+$|^-?[0-9]+\.[0-9]*$/, /-?[0-9]+$|-?[0-9]+(.[0-9]+)?$/, 'Solo se acepta un número real o entero.', [-2147483648, 2147483647]],
    'text': [/^[a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ@.,()/]{0,200}$/,/^[a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ@.,()/]{0,200}$/, 'Solo se aceptan texto menor a 200 caracteres.'],
    'mail': [/^[a-zA-Z0-9_@.-]{1,100}$/, /^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+$/, 'La dirección del correo no es válida'],
    'name': [/^[a-zA-Z ñÑáéíóúÁÉÍÓÚ]{1,50}$/,/^[a-zA-Z ñÑáéíóúÁÉÍÓÚ]{1,100}$/, 'Rellene este campo.'],
    'simple': [/^[a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ]{1,50}$/,/^[a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ]{1,50}$/, 'Solo se acepta texto alfanumerico entre 1 y 50 caracteres.'],
    'textosigno': [/^[a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ@.,()/[\]\-#]{0,200}$/,/^[a-zA-Z0-9 ñÑáéíóúÁÉÍÓÚ@.,()/]{0,200}$/, 'Solo se aceptan texto menor a 200 caracteres.']
}

function attach_validators() {
    for(j in validations){
        (function (j) {
            $('.'+j).unbind('keypress')
            $('.'+j).keypress(function (e) {
                if(e.charCode == 0) return true

                validator = validations[j]
                value = $(this).val() + String.fromCharCode(e.charCode)
                if(!validator[0].test(value)){
                    return false
                }
                if(validator.length > 3){
                    number = parseFloat(value)
                    if(!isNaN(value)){
                        return validator[3][0] <= number && number <= validator[3][1]
                    }
                }
                return true
            })
            $('.'+j).focusout(function (e) {
                field = $('#'+this.id)
                reg = validations[field.attr('data-regexp')]
                if (reg[1].test(field.val())){
                    $(this).parent().removeClass('error')
                    $(this).parent().next('label').text('')
                } else {
                    $(this).parent().addClass('error')
                    $(this).parent().next('label').text(reg[2])
                }
            })
            $('.'+j).attr('data-regexp', j)
            $('.'+j).parent().after('<label class="error"></label>')
        })(j)
    }
}

function validate_fields(ids) {
    for(i in ids){

        field = $('#' + ids[i])
        reg = validations[field.attr('data-regexp')]
        if(!reg[1].test(field.val())){
            return false
        }
    }
    return true
}

function validate_inputs_empty(values)
{
    data = values
    v = data.split(',')
    x=true
    i=0
    while (v.length > i)
    {
        if($("#"+v[i]+"").val() == '')
        {
            $("#"+v[i]+"DIV").addClass('focused')
            $("#"+v[i]+"DIV").addClass('error')
            x=false
        }

        i++
    }
    return x
}
function validarInspeccion() {
    control=true

    if(parseInt($('#fkgerencias').val()) == 0|| $('#fkgerencias').val()==null){
        $('#lbErrorGerencia').show()
        control=false
    }
    if(parseInt($('#fkciclo').val()) == 0|| $('#fkciclo').val()==''){
        $('#lbErrorCiclo').show()
        control=false
    }
    if(parseInt($('#fkgpr').val()) == 0|| $('#fkgpr').val()==''){
        $('#lbErrorGPR').show()
        control=false
    }
    if(parseInt($('#fkempresa').val()) == 0|| $('#fkempresa').val()==null){
        $('#lbErrorEmpresa').show()
        control=false
    }
    if(parseInt($('#fkresponsable').val()) == 0|| $('#fkresponsable').val()==''){
        $('#lbErrorResponsable').show()
        control=false
    }
    return control
}
function validarReciclaje() {
    control=true
    if(parseInt($('#fkgerencias').val()) == 0){
        $('#lbErrorGerencia').show()
        control=false
    }
    if($('#fkrelator').val() == ''){
        $('#lbErrorRelator').show()
        control=false
    }
    if(parseInt($('#fkgpr').val()) == 0){
        $('#lbErrorGpr').show()
        control=false
    }
    if($('#fkempresa').val() == null){
        $('#lbErrorEmpresa').show()
        control=false
    }
    return control
}

function validarReuniones() {
    control=true
    if(parseInt($('#fkgerencias').val()) == 0){
        $('#lbErrorGerencia').show()
        control=false
    }
    if($('#fkrelator').val() == ''){
        $('#lbErrorRelator').show()
        control=false
    }
    if(parseInt($('#fkgpr').val()) == 0){
        $('#lbErrorGpr').show()
        control=false
    }
    if(parseInt($('#fkempresa').val()) == 0){
        $('#lbErrorEmpresa').show()
        control=false
    }
    return control
}
function validarGPR() {
    control=true
    if($('#fkgerencias').val() == '' ||$('#fkgerencias').val()==null ){
        $('#lbErrorGerencia').show()
        control=false
    }
    if(parseInt($('#tipo').val()) == ''||$('#tipo').val()==null){
        $('#lbErrorGpr').show()
        control=false
    }
    if($('#fkempresa').val() == null || $('#fkempresa').val() == '' ){
        $('#lbErrorEmpresa').show()
        control=false
    }
    return control
}
function validarAnalisis() {
    control=true
    if(parseInt($('#fkgerencias').val()) == 0 ||$('#fkgerencias').val()==null ){
        $('#lbErrorGerencia').show()
        control=false
    }
    if($('#fkrelator').val() == null ||$('#fkrelator').val()==0){
        $('#lbErrorRelator').show()
        control=false
    }
    if(parseInt($('#fkgpr').val()) == 0||$('#fkgpr').val()==null){
        $('#lbErrorGpr').show()
        control=false
    }
    if($('#fkempresa').val() == null ||parseInt($('#fkempresa').val()) == 0){
        $('#lbErrorEmpresa').show()
        control=false
    }
    return control
}

function validarInspecciones() {
    control=true
    if(parseInt($('#fkgerencias').val()) == 0){
        control=false
    }
    if(parseInt($('#fkrelator').val()) == 0){
        control=false
    }
    if(parseInt($('#fkgpr').val()) == 0){
        control=false
    }
    if(parseInt($('#fkempresa').val()) == 0){
        control=false
    }
    return control
}
function clean_form() {
    $('div.focused').removeClass('focused')
    $('div.error').removeClass('error')
    $('label.error').text('')
}
function activarCheck() {
    $("#checkbox1").prop("disabled", false);
    $("#checkbox2").prop("disabled", false);
    $("#checkbox3").prop("disabled", false);
    $("#checkbox4").prop("disabled", false);
}

function desActivarCheck() {
    $("#checkbox1").prop("disabled", true);
    $("#checkbox2").prop("disabled", true);
    $("#checkbox3").prop("disabled", true);
    $("#checkbox4").prop("disabled", true);

    document.getElementById('checkbox1').checked=false;
    document.getElementById('checkbox2').checked=false;
    document.getElementById('checkbox3').checked=false;
    document.getElementById('checkbox4').checked=false;
}
function limpiarChekcbox() {
    document.getElementById('checkbox1').checked=false;
    document.getElementById('checkbox2').checked=false;
    document.getElementById('checkbox3').checked=false;
    document.getElementById('checkbox4').checked=false;
    document.getElementById('checkbox5').checked=false;
}




function limpiarIncidentes() {
    $('#fechaIncidente').val('');
    $('#potencialidad').val('');
    $('#potencialidad').selectpicker('render')
    $('#tipo').val('');
    $('#tipo').selectpicker('render')
    $('#resumen').val('');
    $('#descripcion').val('');
    $('#fechaSolucion').val('');
    $('#posibleSolucion').val('');
    $('#txtnombre').val('');
    $('#txtgerencia').val('');
    $('#cargo').val('');
    $('#edad').val('');
    $('#descripcionDaños').val('');
    $('#costo').val('');
    $('#patente').val('');
    $('#tipoVehiculo').val('');
    $('#tipoVehiculo').selectpicker('render')

    $('#fkcodigoposte').val('');
    $('#fkcodigoposte').selectpicker('render')
    $('#fksistema').val('');
    $('#fksistema').selectpicker('render')
    $('#fkpuesto').val('');
    $('#fkpuesto').selectpicker('render')
    $('#fkderivacion').val('');
    $('#fkderivacion').selectpicker('render')
    $('#fkprioridad').val('');
    $('#fkprioridad').selectpicker('render')
    $('#fkcodigomantenimiento').val('');
    $('#fkcodigomantenimiento').selectpicker('render')
    $('#hora').val('');


    document.getElementById('checkaccidente').checked=false;
    document.getElementById('checkcuasi').checked=false;
    document.getElementById('checkacto').checked=false;
    document.getElementById('checkcondicion').checked=false;
    document.getElementById('checkcondicionred').checked=false;
    document.getElementById('checkbox6').checked=false;
    document.getElementById('checkbox7').checked=false;
    document.getElementById('checkbox8').checked=false;
    document.getElementById('checkbox9').checked=false;
    document.getElementById('checkbox10').checked=false;
    document.getElementById('checkbox11').checked=false;
    document.getElementById('checkbox18').checked=false;
    document.getElementById('checkbox19').checked=false;
    document.getElementById('checkbox20').checked=false;

}

function validarObservaciones() {
    control=true
    if(parseInt($('#fkgerencias').val()) == 0|| $('#fkgerencias').val() == ''){

        control=false
    }
    if(parseInt($('#fkresponsable').val()) == 0|| $('#fkresponsable').val() == ''){

        control=false
    }
    if(parseInt($('#fktrabajador').val()) == 0 || $('#fktrabajador').val() == ''){

        control=false
    }
    if($('#fkempresa').val() == null || $('#fkempresa').val() == ''){

        control=false
    }
    if(parseInt($('#fkgpr').val()) == 0 || $('#fkgpr').val() == ''){

        control=false
    }
    return control
}
function borrarFotoObservaciones(a) {
    objeto=""
    if(a=="foto1"){
     objeto = JSON.stringify({
                'id': parseInt($('#id').val()),
                'fecha': $('#fecha').val(),
                'fechaobservacion': $('#fechao').val(),
                'foto1' : ''
    })
    }
    if(a=="foto2"){
     objeto = JSON.stringify({
                'id': parseInt($('#id').val()),
                'fecha': $('#fecha').val(),
                 'fechaobservacion': $('#fechao').val(),
                'foto2' : ""
    })}
    if(a=="foto3") {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'fecha': $('#fecha').val(),
            'fechaobservacion': $('#fechao').val(),
            'foto3': ""
        })
    }

    return objeto
}
function cargar_observaciones(self) {
     $('#id').val(self.id)
     $('#fecha').val(self.fecha)
     $('#fechao').val(self.fechaobservacion)
}
function cargar_id(self) {
     $('#id').val(self.id)
}
function cargar_inspecciones(self) {
     $('#id').val(self.id)
     $('#fecha').val(self.fecha)
}
function borrarFotoAuditorias(a) {
    objeto=""
    if(a=="foto1"){
     objeto = JSON.stringify({
                'id': parseInt($('#id').val()),
                'fecha': $('#fecha').val(),
                'foto1' : ""
    })
    }
    if(a=="foto2"){
     objeto = JSON.stringify({
                'id': parseInt($('#id').val()),
                'fecha': $('#fecha').val(),
                'foto2' : ""
    })}
    if(a=="foto3") {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'fecha': $('#fecha').val(),
            'foto3': ""
        })
    }

    return objeto
}

function borrarFotoInspecciones(a) {
    objeto=""
    if(a=="foto1"){
     objeto = JSON.stringify({
                'id': parseInt($('#id').val()),
                'fecha': $('#fecha').val(),
                'foto1' : ""
    })
    }
    if(a=="foto2"){
     objeto = JSON.stringify({
                'id': parseInt($('#id').val()),
                'fecha': $('#fecha').val(),
                'foto2' : ""
    })}
    if(a=="foto3") {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'fecha': $('#fecha').val(),
            'foto3': ""
        })
    }

    return objeto
}

function borrarFotoAuditorias(a) {
    objeto=""
    if(a=="foto1"){
     objeto = JSON.stringify({
                'id': parseInt($('#id').val()),
                'fecha': $('#fecha').val(),
                'foto1' : ""
    })
    }
    if(a=="foto2"){
     objeto = JSON.stringify({
                'id': parseInt($('#id').val()),
                'fecha': $('#fecha').val(),
                'foto2' : ""
    })}
    if(a=="foto3") {
        objeto = JSON.stringify({
            'id': parseInt($('#id').val()),
            'fecha': $('#fecha').val(),
            'foto3': ""
        })
    }

    return objeto
}
function cargar_auditorias(self) {
    $('#id').val(self.id)
    $('#fecha').val(self.fecha)
}


function validarAuditorias() {
    control = true
    if (parseInt($('#fkgpr').val()) == 0 ||$('#fkgpr').val() == '' ) {
        $('#lbErrorGpr').show()
        control = false
    }
    if (parseInt($('#fkgerencias').val()) == 0||$('#fkgerencia').val() == '') {
        $('#lbErrorGerencia').show()
        control = false
    }
    if (parseInt($('#fkempresa').val()) == 0||$('#fkempresa').val() == null ) {
        $('#lbErrorEmpresa').show()
        control = false
    }
    if (parseInt($('#fkjefe').val()) === 0||$('#fkjefe').val() == '') {
        $('#lbErrorJefe').show()
        control = false
    }
    if (parseInt($('#fksupervisor').val()) == 0||$('#fksupervisor').val() == '') {
       $('#lbErrorSupervisor').show()
        control = false
    }
    if (parseInt($('#fkresponsable').val()) == 0||$('#fkresponsable').val() == '') {
        $('#lbErrorResponsable').show()
        control = false
    }
    if (parseInt($('#fkcargo').val()) == 0||$('#fkcargo').val() == null) {
        $('#lbErrorCargo').show()
        control = false
    }
    return control
}

function golpeadoPor() {
    document.getElementById('checkbox6').checked=false;
   document.getElementById('checkbox8').checked=false;
   document.getElementById('checkbox9').checked=false;
   document.getElementById('checkbox10').checked=false;
   document.getElementById('checkbox11').checked=false;
}
function golpeadoContra() {
    document.getElementById('checkbox7').checked=false;
   document.getElementById('checkbox8').checked=false;
   document.getElementById('checkbox9').checked=false;
   document.getElementById('checkbox10').checked=false;
   document.getElementById('checkbox11').checked=false;
}
function atrapadoEntre() {
    document.getElementById('checkbox6').checked=false;
   document.getElementById('checkbox8').checked=false;
   document.getElementById('checkbox7').checked=false;
   document.getElementById('checkbox10').checked=false;
   document.getElementById('checkbox11').checked=false;
}
function caidaNivel() {
    document.getElementById('checkbox6').checked=false;
   document.getElementById('checkbox8').checked=false;
   document.getElementById('checkbox9').checked=false;
   document.getElementById('checkbox7').checked=false;
   document.getElementById('checkbox11').checked=false;
}
function sobreEsfuerzo() {
    document.getElementById('checkbox6').checked=false;
   document.getElementById('checkbox8').checked=false;
   document.getElementById('checkbox9').checked=false;
   document.getElementById('checkbox10').checked=false;
   document.getElementById('checkbox7').checked=false;
}
function atrapadoPor() {
    document.getElementById('checkbox6').checked=false;
   document.getElementById('checkbox7').checked=false;
   document.getElementById('checkbox9').checked=false;
   document.getElementById('checkbox10').checked=false;
   document.getElementById('checkbox11').checked=false;
}

function validarCondicionSubEstandar() {
    control=true;
     values="fechaIncidente0,potencialidad0,resumen0,descripcion0,fechaSolucion0,posibleSolucion0"
    control = validate_inputs_empty(values)
    return control;
}
function validarSubEstandarRed() {
    control=true;
     values="fechaIncidente1,potencialidad1,resumen1,descripcion1,fechaSolucion1,posibleSolucion1,puesto,derivacion,prioridad,sistema,codigoMantenimiento   "
    control = validate_inputs_empty(values)
    return control;
}
function validarActoSubestandar() {
    control=true;
    values="fechaIncidente2,potencialidad2,tipo2,resumen2,descripcion2,fechaSolucion2,posibleSolucion2"
    control = validate_inputs_empty(values)
    return control;
}
function validarCuasiAccidente() {
    control=true;
    values="fechaIncidente3,potencialidad3,resumen3,descripcion3,fechaSolucion3,posibleSolucion3"
    control = validate_inputs_empty(values)
    return control;
}
function validarAccidente() {
    control=true
    values="gpr0,gerencia0,empresa0,fechaIncidente,potencialidad,tipo,resumen,descripcion,txtnombre,txtgerencia,cargo,edad,descripcionDaños,costo,patente"
    control=validate_inputs_empty(values)
    return control;
}
function validarIncidente(tipo) {
    values =""
      if(tipo=='Accidente'){
          values="fechaIncidente,potencialidad,tipo,resumen,posibleSolucion,descripcion,txtnombre,txtgerencia,cargo,edad,descripcionDaños,costo,patente"
      }
      if(tipo=='Cuasi Accidente'){
          values="fechaIncidente,potencialidad,resumen,descripcion,fechaSolucion,posibleSolucion"
      }
      if(tipo=='Acto Subestandar'){
          values="fechaIncidente,potencialidad,tipo,resumen,descripcion,fechaSolucion,posibleSolucion"
      }
      if(tipo=='Condicion Subestandar'){
          values="fechaIncidente,potencialidad,resumen,descripcion,fechaSolucion,posibleSolucion"
      }
      if(tipo =='Condicion Subestandar de Red'){
          values='fechaIncidente,potencialidad,resumen,descripcion,fechaSolucion,posibleSolucion,puesto,derivacion,prioridad,sistema,codigoMantenimiento'
      }
      return values
}
function validarLugar() {
    control=true;
    if ($('#gpr0').val() == '') {
        control = false;
    }
    if ($('#gerencia0').val() == ''){
        control = false;
    }
    if ($('#empresa0').val() == '') {
        control = false;
    }
   return control;
}

function mostrarIncidente(self) {

    if(self.tipologia==="Golpeado por"){
        document.getElementById('checkbox7').checked=true
    }
    if(self.tipologia==="Golpeado contra"){
        document.getElementById('checkbox6').checked=true
    }
    if(self.tipologia==="Atrapado por"){
        document.getElementById('checkbox8').checked=true
    }
    if(self.tipologia==="Atrapado entre"){
        document.getElementById('checkbox9').checked=true
    }
    if(self.tipologia==="Caida a un mismo nivel"){
        document.getElementById('checkbox10').checked=true
    }
    if(self.tipologia==="Sobre esfuerzo"){
        document.getElementById('checkbox11').checked=true
    }



    if(self.tipo==="Accidente"){
        document.getElementById('checkaccidente').checked=true
    }
    if(self.tipo==="Cuasi Accidente"){
        document.getElementById('checkcuasi').checked=true
    }
    if(self.tipo==="Acto Subestandar"){
        document.getElementById('checkacto').checked=true
    }
    if(self.tipo==="Condicion Subestandar"){
        document.getElementById('checkcondicion').checked=true
    }
    if(self.tipo==="Condicion Sub Estandar de Red"){

        document.getElementById('checkcondicionred').checked=true
    }
                cargarGerenciaIncidente()
                cargar_gpr_incidente(self.fkgerencia)
                cargar_persona_incidente(self.fkgpr)

                cargarGerenciaIncidenteLugar()
                cargar_gpr_incidenteLugar(self.gerencial)


                $('#fkempresa').val(self.fkempresa),
                $('#fkgerencia').val(self.fkgerencia),
                $('#fkgpr').val(self.fkgpr),

                $('#fkempresa').selectpicker('render')
                $('#fkgerencia').selectpicker('refresh')
                $('#fkgpr').selectpicker('refresh')

                $('#nombre').val(self.fkpersona)
                $('#nombre').selectpicker('refresh')
                $('#empresa0').val(self.empresal)
                $('#empresa0').selectpicker('render')
                $('#gerencia0').val(self.gerencial)
                $('#gerencia0').selectpicker('render')

                $('#tipoVehiculo').val(self.tipoVehiculo)
                $('#tipoVehiculo').selectpicker('render')
                $('#fechaIncidente').val(self.fechaIncidente),
                $('#gpr0').val(self.gprl)
                $('#gpr0').selectpicker('refresh')
                $('#txtnombre').val(self.nombrea),
                $('#txtgerencia').val(self.gerenciaa),
                $('#cargo').val(self.cargo),
                $('#resumen').val(self.resumen),
                $('#descripcionDaños').val(self.descripcionDaños),
                $('#descripcion').val(self.descripcion),
                $('#edad').val(self.edad),
                $('#patente').val(self.patente),
                $('#costo').val(self.costos),
                $('#potencialidad').val(self.potencialidad),
                $('#potencialidad').selectpicker('render'),
                $('#tipoEmpresa').val(self.tipoEmpresa),
                $('#id').val(self.id),
                $('#tipoEmpresa').selectpicker('render')
                $('#fechaSolucion').val(self.fechaSolucion)
                $('#hora').val(self.hora)

                $('#fkcodigoposte').val(self.fkcodigoposte)
                $('#fkcodigoposte').selectpicker('refresh')
                $('#fkpuesto').val(self.fkpuesto)
                $('#fkpuesto').selectpicker('refresh')
                $('#fkderivacion').val(self.fkderivacion)
                $('#fkderivacion').selectpicker('refresh')
                $('#fkprioridad').val(self.fkprioridad)
                $('#fkprioridad').selectpicker('refresh')
                $('#fksistema').val(self.fksistema)
                $('#fksistema').selectpicker('refresh')
                $('#fkcodigomantenimiento').val(self.fkcodigomantenimiento)
                $('#fkcodigomantenimiento').selectpicker('refresh')

                $('#posibleSolucion').val(self.posibleSolucion)

                document.getElementById('checkbox18').checked=self.responsabilidad,
                document.getElementById('checkbox19').checked=self.accidente,
                document.getElementById('checkbox20').checked=self.muerte

}
function mostrarIncidenteCierre(self) {

    if(self['response'][0]['incidentes']['tipologia']==="Golpeado por"){
        document.getElementById('checkbox7').checked=true
    }
    if(self['response'][0]['incidentes']['tipologia']==="Golpeado contra"){
        document.getElementById('checkbox6').checked=true
    }
    if(self['response'][0]['incidentes']['tipologia']==="Atrapado por"){
        document.getElementById('checkbox8').checked=true
    }
    if(self['response'][0]['incidentes']['tipologia']==="Atrapado entre"){
        document.getElementById('checkbox9').checked=true
    }
    if(self['response'][0]['incidentes']['tipologia']==="Caida a un mismo nivel"){
        document.getElementById('checkbox10').checked=true
    }
    if(self['response'][0]['incidentes']['tipologia']==="Sobre esfuerzo"){
        document.getElementById('checkbox11').checked=true
    }


    if(self['response'][0]['incidentes']['tipo']==="Accidente"){
        document.getElementById('checkaccidente').checked=true
    }
    if(self['response'][0]['incidentes']['tipo']==="Cuasi Accidente"){
        document.getElementById('checkcuasi').checked=true
    }
    if(self['response'][0]['incidentes']['tipo']==="Acto Subestandar"){
        document.getElementById('checkacto').checked=true
    }
    if(self['response'][0]['incidentes']['tipo']==="Condicion Subestandar"){
        document.getElementById('checkcondicion').checked=true
    }
    if(self['response'][0]['incidentes']['tipo']==="Condicion Sub Estandar de Red"){
        document.getElementById('checkcondicionred').checked=true
    }
                cargarGerenciaIncidente()
                cargar_gpr_incidente(self['response'][0]['incidentes']['fkgerencia'])
                cargar_persona_incidente(self['response'][0]['incidentes']['fkgpr'])

                cargarGerenciaIncidenteLugar()
                cargar_gpr_incidenteLugar(self['response'][0]['incidentes']['gerencial'])

                $('#fkempresa').val(self['response'][0]['incidentes']['fkempresa']),
                $('#fkgerencia').val(self['response'][0]['incidentes']['fkgerencia']),
                $('#fkgpr').val(self['response'][0]['incidentes']['fkgpr']),

                $('#fkempresa').selectpicker('render'),
                $('#fkgerencia').selectpicker('refresh'),
                $('#fkgpr').selectpicker('refresh'),

                $('#nombre').val(self['response'][0]['incidentes']['fkpersona']),
                $('#nombre').selectpicker('refresh'),
                $('#empresa0').val(self['response'][0]['incidentes']['empresal'])
                $('#empresa0').selectpicker('render')
                $('#gerencia0').val(self['response'][0]['incidentes']['gerencial'])
                $('#gerencia0').selectpicker('render')

                $('#tipoVehiculo').val(self['response'][0]['incidentes']['tipoVehiculo']),
                $('#tipoVehiculo').selectpicker('render')
                $('#fechaIncidente').val(self['response'][0]['incidentes']['fechaIncidente']),
                $('#gpr0').val(self['response'][0]['incidentes']['gprl']),
                $('#gpr0').selectpicker('refresh')
                $('#txtnombre').val(self['response'][0]['incidentes']['nombrea']),
                $('#txtgerencia').val(self['response'][0]['incidentes']['gerenciaa']),
                $('#cargo').val(self['response'][0]['incidentes']['cargo']),
                $('#resumen').val(self['response'][0]['incidentes']['resumen']),
                $('#descripcionDaños').val(self['response'][0]['incidentes']['descripcionDaños']),
                $('#descripcion').val(self['response'][0]['incidentes']['descripcion']),
                $('#edad').val(self['response'][0]['incidentes']['edad']),
                $('#patente').val(self['response'][0]['incidentes']['patente']),
                $('#costo').val(self['response'][0]['incidentes']['costos']),
                $('#potencialidad').val(self['response'][0]['incidentes']['potencialidad']),
                $('#potencialidad').selectpicker('render'),
                $('#tipoEmpresa').val(self['response'][0]['incidentes']['tipoEmpresa']),
                $('#id').val(self['response'][0]['incidentes']['id']),
                $('#tipoEmpresa').selectpicker('render'),
                $('#fechaSolucion').val(self['response'][0]['incidentes']['fechaSolucion']),

                $('#fkcodigoposte').val(self['response'][0]['incidentes']['fkcodigoposte']),
                $('#fkcodigoposte').selectpicker('refresh')
                $('#fkpuesto').val(self['response'][0]['incidentes']['fkpuesto']),
                $('#fkpuesto').selectpicker('refresh')
                $('#fkderivacion').val(self['response'][0]['incidentes']['fkderivacion']),
                $('#fkderivacion').selectpicker('refresh')
                $('#fkprioridad').val(self['response'][0]['incidentes']['fkprioridad']),
                $('#fkprioridad').selectpicker('refresh')
                $('#fksistema').val(self['response'][0]['incidentes']['fksistema']),
                $('#fksistema').selectpicker('refresh')
                $('#fkcodigomantenimiento').val(self['response'][0]['incidentes']['fkcodigomantenimiento']),
                $('#fkcodigomantenimiento').selectpicker('refresh')
                $('#posibleSolucion').val(self['response'][0]['incidentes']['posibleSolucion']),

                document.getElementById('checkbox18').checked=self['response'][0]['incidentes']['responsabilidad'],
                document.getElementById('checkbox19').checked=self['response'][0]['incidentes']['accidente'],
                document.getElementById('checkbox20').checked=self['response'][0]['incidentes']['muerte']


                if(self['response'][0]['fecha'] == "None"){
                     $('#fechaSolucionIncidete').val('')
                     $('#fechaSolucionIncidete').selectpicker('refresh')

                }else{

                    $('#fechaSolucionIncidete').val(self['response'][0]['fecha'])
                     $('#fechaSolucionIncidete').selectpicker('refresh')
                }


                if(self['response'][0]['solucion'] == "None"){
                        $('#txtSolucion').val('')

                }else{

                        $('#txtSolucion').val(self['response'][0]['solucion'])
                }

                $('#responsableCierre').val(self['response'][0]['fkpersona']),
                $('#responsableCierre').selectpicker('refresh')



}

function validarSeguridadPersona() {
    control=true
   if(parseInt($('#fkgerencias').val()) == 0){
        $('#lbErrorGerencia').show()
        control=false
    }
    if(parseInt($('#fkgpr').val()) == 0){
        $('#lbErrorGpr').show()
        control=false
    }
    if(parseInt($('#fkempresa').val()) == 0){
        $('#lbErrorEmpresa').show()
        control=false
    }

    return control
}
function validate_auditorias_empty(values)
{
    data = values
    v = data.split(',')
    x=true
    i=0
    while (v.length > i)
    {
        if($("#"+v[i]+"").val() == '')
        {
            $("#"+v[i]+"LB").show()
            x=false
        }

        i++
    }
    return x
}
