function validationInputSelects(id) {
    var flag = false
    var elementsInput = document.querySelectorAll('#'+id+' input[type=text]:enabled')
    var elementsSelect = document.querySelectorAll('#'+id+' select')
    var elementsNumber = document.querySelectorAll('#'+id+' input[type=number]:enabled')
    for (var i = 0; i < elementsInput.length; i++) {
        if (elementsInput[i].id != '')
            if (!elementsInput[i].checkValidity()) {
                printError(elementsInput[i] , elementsInput[i].validationMessage)
                flag = true
            }else{
                eraseError(elementsInput[i])
            }
    }
    for (var i = 0; i < elementsNumber.length; i++) {
        if (elementsNumber[i].id != '')
            if (!elementsNumber[i].checkValidity()) {

                printError(elementsNumber[i] , elementsNumber[i].validationMessage)
                flag = true
            }else{
                eraseError(elementsNumber[i])
            }
    }
    for (var i = 0; i < elementsSelect.length; i++) {

        if (!elementsSelect[i].checkValidity()) {

            printError(elementsSelect[i], elementsSelect[i].validationMessage)
            flag = true
        }else {
                eraseError(elementsSelect[i])
        }

    }
    return flag
}


function disabledInputSelects(id) {
    var flag = false
    var elementsInput = document.querySelectorAll('#'+id+' input[type=text]')
    var elementsSelect = document.querySelectorAll('#'+id+' select')
    var elementsButton = document.querySelectorAll('#'+id+' button')
    var elementsCheck = document.querySelectorAll('#'+id+' input[type=checkbox]')
    var elementsFile = document.querySelectorAll('#'+id+' input[type=file]')
    for (var i = 0; i < elementsInput.length; i++) {

        elementsInput[i].disabled=true

    }
    for (var i = 0; i < elementsSelect.length; i++) {

        elementsSelect[i].disabled=true
    }
    for (var i = 0; i < elementsButton.length; i++) {


        elementsButton[i].disabled=true
    }
    for (var i = 0; i < elementsCheck.length; i++) {

        elementsCheck[i].disabled=true
    }
    for (var i = 0; i < elementsFile.length; i++) {
        elementsFile[i].disabled=true

    }

    return flag
}

function enabledInputSelects(id) {
    var flag = false
    var elementsInput = document.querySelectorAll('#'+id+' input[type=text]')
    var elementsSelect = document.querySelectorAll('#'+id+' select')
    var elementsButton = document.querySelectorAll('#'+id+' button')
    var elementsCheck = document.querySelectorAll('#'+id+' input[type=checkbox]')
    var elementsFile = document.querySelectorAll('#'+id+' input[type=file]')
    for (var i = 0; i < elementsInput.length; i++) {

        elementsInput[i].disabled=false

    }
    for (var i = 0; i < elementsSelect.length; i++) {

        elementsSelect[i].disabled=false
    }
    for (var i = 0; i < elementsButton.length; i++) {

        elementsButton[i].disabled=false
    }
    for (var i = 0; i < elementsCheck.length; i++) {

        elementsCheck[i].disabled=false
    }
    for (var i = 0; i < elementsFile.length; i++) {
        elementsFile[i].disabled=false

    }

    return flag
}


function printError(element, validMessage){
        element.parentElement.classList.add("error")
        if(!document.getElementById('errorMsg_'+element.id)) {
            labelError = document.createElement("label");
            // labelError.appendChild(labelErrorText);
            labelError.setAttribute('id',"errorMsg_"+element.id)
            labelError.classList.add("error");
            labelError.classList.add("text-danger");
            labelError.innerHTML = validMessage;
            element.parentElement.insertAdjacentElement("afterend", labelError);
        }
}
function validationKeyup(id){
    var elementsInput = document.querySelectorAll('#'+id+' input[type=text]')
    var elementsNumber = document.querySelectorAll('#'+id+' input[type=number]:enabled')
     for (var i = 0; i < elementsInput.length; i++) {

        if (elementsInput[i].id != '')
            elementsInput[i].oninput = function () {
                if (!this.checkValidity()){
                    printError(this,this.validationMessage)
                } else{
                    eraseError(this)
                }
            }
    }
    for (var i = 0; i < elementsNumber.length; i++) {

        if (elementsNumber[i].id != '')
            elementsNumber[i].oninput = function () {
                if (!this.checkValidity()){
                    printError(this,this.validationMessage)
                } else{
                    eraseError(this)
                }
            }
    }
}
function validationSelectChange(id) {
    var elementsSelect = document.querySelectorAll('#'+id+' select')
    for (var i = 0; i < elementsSelect.length; i++) {

        elementsSelect[i].addEventListener('change',function () {
            if(this.value != 0)
                eraseError(this)
        })
        if (!elementsSelect[i].checkValidity()) {

                printError(elementsSelect[i],elementsSelect[i].validationMessage)
            }
    }
}

function eraseError(element){
    if(document.getElementById('errorMsg_'+element.id)){
        eleChild = document.getElementById('errorMsg_'+element.id)
        element.parentElement.classList.remove('error');
        eleChild.parentElement.removeChild(eleChild)
    }

}



