// Obtiene el precio de la licencia
var licensePrice = document.getElementById("licensePrice").value;
var school = document.getElementById("school").value;
// Formatea el precio para poder setearlo en Paypal
licensePrice = licensePrice.replace(',', '.') 

// Proceso de Paypal
paypal.Button.render({

    env: 'sandbox', // sandbox | production

    locale: 'es_ES',

    style: {
        size: 'responsive',
        color: 'gold',
        shape: 'rect',
        label: 'pay',
        tagline: false,
        fundingicons: true,
    },

    // PayPal Client IDs - replace with your own
    // Create a PayPal app: https://developer.paypal.com/developer/applications/create
    client: {
        sandbox: 'AZDxjDScFpQtjWTOUtWKbyN_bDt4OgqaF4eYXlewfBP4-8aqX3PiV8e1GWU6liB2CUXlkA59kJXE7M6R',
        production: '<insert production client id>'
    },

    // Show the buyer a 'Pay Now' button in the checkout flow
    commit: true,

    // payment() is called when the button is clicked
    payment: function (data, actions) {

        // Make a call to the REST api to create the payment
        return actions.payment.create({
            payment: {
                transactions: [
                    {
                        amount: { total: licensePrice, currency: 'EUR' }
                    }
                ]
            }
        });
    },

    // onAuthorize() is called when the buyer approves the payment
    onAuthorize: function (data, actions) {

        // Make a call to the REST api to execute the payment
        return actions.payment.execute().then(function () {
            //window.alert('Payment Complete!');

            // Activa el input del Formulario para controlar errores
            document.getElementById("payment").value = '1';

            // Env&#237;a el formulario
            document.forms.payForm.submit();
        });
    },

    // onCancel() is called when the buyer cancels the payment
    onCancel: function (data, actions) {
        //return window.alert('Payment Cancelled!');

        // Desactiva el input del Formulario para controlar errores
        document.getElementById("payment").value = '0';

        // Env&#237;a el formulario
        document.forms.payForm.submit();
    },

    // onError() is called when the an error occurs
    onError: function (data, actions) {
        //return window.alert('Payment Cancelled!');

        // Desactiva el input del Formulario para controlar errores
        document.getElementById("payment").value = '0';

        // Env&#237;a el formulario
        document.forms.payForm.submit();
    }

}, '#paypal-button-container');
