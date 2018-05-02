
//$('#selectedLicense').click(function () {
//    console.log($('#selectedLicense').value)
//});

// Variable global para la licencia tipo
var licenseType;

$(document).ready(function() {
  var radios = document.getElementsByName("licenseSelect");
  for(i=0; i<radios.length; i++) {
    var checkboxElement = radios[i].parentElement.parentElement;
    if(radios[i].checked) {
      checkboxElement.classList.add("selected");
    } else {
      checkboxElement.classList.remove("selected");
    }
  }
});

function FillLicenseFields(license) {

    myLicense = license;

    // Calcula precio unitario si no es licencia grauita
    if (myLicense.name !== "GRATUITA") {
        var unitPrice = (parseFloat(license.price) / license.users).toFixed(2);
    }    

    var htmlLicenseFields =
        '<input type="hidden" name="licenseType" value="' + parseInt(license.id) + '">' +
        '<hr />' +
        '<div class="row">' +
        '<div class="col-xs-12 col-md-12 form-group">' +
        '<h4 style="text-align: center; color: #1fb4e0;">&#161; Has elegido una licencia de tipo ' + license.name + ' !</h4>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '<div class="row">' +
        '<div class="col-xs-6 col-md-6 form-group">' +
        '<label for="numExercises" class="control-label">Ejercicios gratuitos</label>' +
        '<input readonly class="form-control" type="text" placeholder="Esta licencia incluye ' + license.exercises + ' ejercicios gratuitos." />' +
        '</div>';

    // Si es licencia GRATUITA
    if (myLicense.name === "GRATUITA") {
        htmlLicenseFields = htmlLicenseFields +
            '<div class="col-xs-6 col-md-6 form-group">' +
            '<label for="numUsers" class="control-label">Usuarios de base</label>' +
            '<input readonly type="number" min="' + license.users + '" class="form-control" id="numUsers" name="numUsers" value="' + license.users + '" />' +
            '</div>' +
            '</div>';

    // Si es alguna DE PAGO
    } else {
        htmlLicenseFields = htmlLicenseFields +
            '<div class="col-xs-6 col-md-6 form-group">' +
            '<label for="numUsers" class="control-label">Usuarios de base</label>' +
            '<input required oninput="CalculatePriceField()" type="number" min="' + license.users + '" class="form-control" id="numUsers" name="numUsers" value="' + license.users + '" />' +
            '<span class="unit-price-user">* El coste unitario de cada usuario extra es de ' + unitPrice + ' &euro;.</span>' +
            '</div>' +
            '</div>';
    }

    $('#licensePersonalization').empty();
    $('#licensePersonalization').append(htmlLicenseFields);

}

function CalculatePriceField() {

    var numUsers = document.getElementById("numUsers").value;

    var unitPrice = (parseFloat(myLicense.price) / myLicense.users).toFixed(2);
    var finalPrice = parseFloat(myLicense.price) + ((numUsers - myLicense.users) * unitPrice);
    finalPrice = finalPrice.toFixed(2);

    var htmlPriceField =
        '<div id="finalPrice" class="row">' +
        '<div class="col-xs-12 col-md-12 form-group">' +
        '<label for="finalPrice" class="control-label">Informaci&#243;n sobre el precio</label>' +
        '<input disabled type="text" class="form-control" name="finalPrice" id="finalPrice" value="El coste final de la licencia para el n&#250;mero de usuarios seleccionado es de ' + finalPrice + ' &euro;/a&#241;o." />' +
        '</div>' +
        '</div>';

    $('#finalPrice').remove();
    $('#licensePersonalization').append(htmlPriceField);

}
