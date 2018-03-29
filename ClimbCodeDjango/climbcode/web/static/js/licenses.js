
//$('#selectedLicense').click(function () {
//    console.log($('#selectedLicense').value)
//});

// Variable global para la licencia tipo
var licenseType;

function FillLicenseFields(license) {

    myLicense = license;

    var unitPrice = (parseFloat(license.price) / license.users).toFixed(2);

    var htmlLicenseFields =
        '<input type="hidden" name="licenseType" value="' + parseInt(license.id) + '">' +
        '<hr />' +
        '<div class="row">' +
        '<div class="col-xs-12 col-md-12 form-group">' +
        '<label for="numUsers" class="control-label">&#191;Necesitas m&#225;s usuarios?</label>' +
        '<input required oninput="CalculatePriceField()" type="number" min="' + license.users + '" class="form-control" id="numUsers" name="numUsers" id="numUsers" placeholder="Esta licencia incluye ' + license.users + ' usuarios de base" />' +
        '<span class="unit-price-user">* El coste unitario de cada usuario extra es de ' + unitPrice +' &euro;.</span>' +
        '</div>' +
        '</div>';

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