function checkCustomCheckbox(checkbox) {
  var radios = document.getElementsByName(checkbox.name);
  for(i=0; i<radios.length; i++) {
    var checkboxElement = radios[i].parentElement.parentElement;
    if(radios[i].checked) {
      checkboxElement.classList.add("selected");
    } else {
      checkboxElement.classList.remove("selected");
    }
  }
}


function CustomFillLicenseFields(checkbox, license) {

    myLicense = license;

    var unitPrice = (parseFloat(license.price) / license.users).toFixed(2);

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
        '</div>' +
        '<div class="col-xs-6 col-md-6 form-group">' +
        '<label for="numUsers" class="control-label">Usuarios de base</label>' +
        '<input required oninput="CalculatePriceField()" type="number" min="' + license.users + '" class="form-control" id="numUsers" name="numUsers" id="numUsers" value="'+ license.users +'" />' +
        '<span class="unit-price-user">* El coste unitario de cada usuario extra es de ' + unitPrice +' &euro;.</span>' +
        '</div>' +
        '</div>';

    $('#licensePersonalization').empty();
    $('#licensePersonalization').append(htmlLicenseFields);

}
