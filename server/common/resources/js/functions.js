function ajax_call(url, data, render, callback) {
    $.ajax({
        method: "POST",
        url: url,
        data: data,
        async: false
    }).done(function (response) {
        if (render != null){
            $(render).html(response)
        } else {
            dictionary = JSON.parse(response)
            if ("message" in dictionary && dictionary.message != ''){
                if (dictionary.success) {
                    showMessage(dictionary.message, "success", "ok")
                } else {
                    showMessage(dictionary.message, "danger", "remove")
                }
            }
        }
        if(callback != null){
            callback(response)
        }
    })
}
function ajax_call_own(url, data, render, callback) {
    $.ajax({
        method: "POST",
        url: url,
        data: data,
        async: false/*,
        beforeSend: function () {
            console.log('before')
            $("#spn-ld").remove();
            $("<div id='spn-ld' style='text-align: center; margin:auto;width:100%; height:65px;'>"+
               "<div style='margin:auto;display:block; height:55px;'>"+
                   "<img src='resources/images/espiral.gif' style='height:100%; width:auto;'/>"+
               "</div>"+
            "</div>").insertAfter(".swal2-title");
        },
        success: function (data, textStatus) {
            console.log('success')
           $("#spn-ld").fadeOut(800);
        }*/
    }).done(function (response) {
        if (render != null){
            $(render).html(response)
        } else {
            dictionary = JSON.parse(response)
            if ("message" in dictionary && dictionary.message != ''){
                if (dictionary.success) {
                    showMessage(dictionary.message, "success", "ok")
                } else {
                    showMessage(dictionary.message, "danger", "remove")
                }
            }
        }
        if(callback != null){
            callback(response)
        }
    })
}
function ajax_call2(ruta, data, render, callback) {
        $.ajax({
            url: ruta,
            type: "post",
            data: data,
            contentType: false,
            processData: false,
            cache: false,
            async: false
        }).done(function (response) {
            response=JSON.parse(response);
            if (response.success){
                showMessage(response.message, "success", "ok");
                $('.modal-backdrop').remove();
                $('body').removeClass('modal-open');
                $('#form').modal('hide')
                query(main_route)
            }else{
                showMessage(response.message, "danger", "remove");
                $("#submit_imagen").waitMe("hide");
            }
        })
}
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
function ajax_call_get(url, data, callback) {
    $.ajax({
        method: "PUT",
        url: url,
        data: data,
        async: false
    }).done(function (response) {
        if(callback != null){
            dictionary = JSON.parse(response)
            callback(dictionary.response)
        }
    })
}
function ajax_call_post(url, data, callback) {
    $.ajax({
        method: "POST",
        url: url,
        data: data,
        async: false
    }).done(function (response) {
        if(callback != null){
            dictionary = JSON.parse(response)
            if (dictionary.success) {
                showMessage(dictionary.message, "success", "ok")
            } else {
                showMessage(dictionary.message, "danger", "remove")
            }
            callback(dictionary)
        }
    })
}

function remove_empty_columns() {
    if(!$.trim($('#table_content > tr > td:last-child').html()).length){
        $('#table_content > tr > td:last-child, .actions_header').remove()
    }
}

function query(url) {
    data = {
        data: JSON.stringify({
            page_nr: page_nr,
            max_entries: max_entries,
            like_search: like_search,
            order_by: order_by,
            ascendant: ascendant
        })
    }
    ajax_call(url, data, '#table_content', function () { remove_empty_columns() })
}

function verif_inputs() {
    $.each($('#form .form-line input'), function (index, value) {
        if(value.value.length > 0){
            $(value).parent().addClass('focused')
        }
    })
}

function verif_inputs2() {
    $.each($('#form2 .form-line input'), function (index, value) {
        if(value.value.length > 0){
            $(value).parent().addClass('focused')
        }
    })
}

function verif_inputs_catalogo() {
    $.each($('#form_catalogo .form-line input'), function (index, value) {
        if(value.value.length > 0){
            $(value).parent().addClass('focused')
        }
    })
}

function verif_inputs_paginas() {
    $.each($('#form_paginas .form-line input'), function (index, value) {
        if(value.value.length > 0){
            $(value).parent().addClass('focused')
        }
    })
}

function reload_form() {
    //Tooltip
//    $('[data-toggle="tooltip"]').tooltip({
//        container: 'body'
//    });
    $('.form-control').focus(function () {
        $(this).parent().addClass('focused');
    }).focusout(function () {
        var $this = $(this);
        if ($this.parents('.form-group').hasClass('form-float')) {
            if ($this.val() == '') { $this.parents('.form-line').removeClass('focused'); }
        }
        else {
            $this.parents('.form-line').removeClass('focused');
        }
    });

    $('body').on('click', '.form-float .form-line .form-label', function () {
        $(this).parent().find('input').focus();
    });
}

function confirmation_message(title, callback) {
    swal({
            //title: "¿Está seguro de que desea cancelar la operacion?",
            title: "¿Está seguro de que desea cancelar la operacion?",
            text: "Al cerrar esta ventana, no se guardará ningún cambio realizado",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Aceptar",
            cancelButtonText: "Cancelar",
            closeOnConfirm: true,
            closeOnCancel: true
        }, function (isConfirm) {
            if (isConfirm) {
                $('#form').modal('hide')
                //callback()
            }
        })
}
