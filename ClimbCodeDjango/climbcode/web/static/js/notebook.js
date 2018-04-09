//Variables para generar ids unicos
var numBox = 0;
var numImg = 0;
var numParameter = 0;

function prueba(){
	alert(saludo);
}

function addNewTextBox(idNotebookContent,idNotebookBD){
	addTextBox(idNotebookContent,idNotebookBD,null,null,'');
}

function addTextBox(idNotebookContent,idNotebookBD,order,idBoxBD,content){
	numBox++;
	var idBox = "idBox"+numBox;
	var idBoxParameter = "'idBox"+numBox+"'";
	var idFormBox = "form_box_"+idBox;
	var idInputText = "input_text_box_"+idBox;
	var idHiddenIdNotebook = "input_hidden_id_notebook_"+idBox;
	var idHiddenOrder = "input_hidden_order_"+idBox;
	var idHiddenIdBox = "input_hidden_id_box_"+idBox;
	if(order==null){
		var order = numBox;
	}

	//HTML DE LA CAJA DE TEXTO
		var htmlTextBox = 	'<div class="col-md-10 custom-mt-1 offset-md-1" id="'+idBox+'">'+
								'<div class="row">'+
									'<div class="col-md-12 custom-mt-1" >'+
										'<div class="form-group" style="padding:12px;">'+
											'<form method="POST" id="'+idFormBox+'">'+
												'<input type="hidden" id="'+idHiddenIdNotebook+'" value="'+idNotebookBD+'">'+
												'<input type="hidden" id="'+idHiddenOrder+'" value="'+order+'">'+
												'<input type="hidden" id="'+idHiddenIdBox+'" value="'+idBoxBD+'">'+
				                            	'<textarea id="'+idInputText+'" onkeyup="auto_grow(this)" class="form-control text-box-textarea" placeholder="Escribe aquí">'+content+'</textarea>'+
				                         		'<button type="submit" class="btn btn-info pull-right" style="margin-top:10px" type="button">Save</button>'+
				                         		'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteElement('+idBoxParameter+')" type="button">Eliminar</button>'+
			                        		'</form>'+
			                        	'</div>'+
									'</div>'+
								'</div>'+
							'</div>';

    $('#'+idNotebookContent).append(htmlTextBox);

    // Comportamiento al pulsar SAVE -> Llamada Ajax

    $('#'+idFormBox).on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");
        //MANDAR COMO PARÁMETRO TODO INPUT QUE SEA NECESARIO RECUPERAR EN EL MÉTODO
        createTextBox(idHiddenIdNotebook,idHiddenOrder,idInputText);
    });


}

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}

function addNewCodeBox(idNotebookContent,idNotebookBD){
	return addCodeBox(idNotebookContent,idNotebookBD,null,null,'');
}

function addCodeBox(idNotebookContent,idNotebookBD,order,idBoxBD,content){
	numBox++;
	var idBox = "idBox"+numBox;
	var idBoxParameter = "'idBox"+numBox+"'";

	//Editor id
	var idEditor = "idEditor"+numBox;
	var idEditorParameter = "'idEditor"+numBox+"'";
	//Div Parameter id
	var idDivParam = "id_div_parameter_"+numBox;
	var idDivParamParameter = "'id_div_parameter_"+numBox+"'";
	//Div Parameter Button id
	var idDivParamButton = "id_div_parameter_button_"+numBox;
	var idDivParamButtonParameter = "'id_div_parameter_button_"+numBox+"'";
	//Add Parameter Button id
	var idAddParamButton = "id_add_parameter_button_"+numBox;
	var idAddParamButtonParameter = "'id_add_parameter_button_"+numBox+"'";	
	//Div Row Principal del contenido para concatenar la gráfica
	var idRowPrincipal = "id_code_box_row_"+idBox;
	var idRowPrincipalParameter = "'id_code_box_row_"+idBox+"'";
	//Div Col Add Delete Button Chart
	var idColChartButtons = "id_col_chart_buttons_"+idBox;
	var idColChartButtonsParameter = "'id_col_chart_buttons_"+idBox+"'";

	/* IDS FORM */
	var idFormBox = "form_box_"+idBox;
	var idHiddenIdNotebook = "input_hidden_id_notebook_"+idBox;
	var idHiddenOrder = "input_hidden_order_"+idBox;
	var idHiddenIdBox = "input_hidden_id_box_"+idBox;
	if(order==null){
		var order = numBox;
	}
	

	//HTML DE LA CAJA DE CÓDIGO

	var htmlCodeBox = 	'<div class="col-md-12 custom-mt-1" >'+
							'<div class="row" id="'+idBox+'">'+
	                            '<div class="col-md-10 custom-mt-1 offset-md-1" >'+
	                                '<h2 style="text-align: center">CUADRO DE CÓDIGO</h2>'+
	                                '<div style="background-color: #ebebeb;margin-left: 30px; margin-right: 30px;width: auto;height: auto">'+
	                                    '<div class="row" id="'+idRowPrincipal+'">'+
	                                    	/* INICIO ACE EDITOR */
	                                        '<div class="col-md-12">'+
	                                            '<div id="'+idEditor+'">'+content+
	                                            '</div>'+
	                                        '</div>'+

	                                        /* FIN ACE EDITOR */
	                                        '<div class="col-md-12" style="margin-top: 20px;">'+
	                                        '<form method="POST" id="'+idFormBox+'">'+
												'<input type="hidden" id="'+idHiddenIdNotebook+'" value="'+idNotebookBD+'">'+
												'<input type="hidden" id="'+idHiddenOrder+'" value="'+order+'">'+
												'<input type="hidden" id="'+idHiddenIdBox+'" value="'+idBoxBD+'">'+
												'<button type="submit" class="btn btn-info pull-right" style="margin-top:10px" type="button">Guardar</button>'+
											'</form>'+
	                                        '<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteElement('+idBoxParameter+')" type="button">Eliminar</button>'+
	                                                '<div class="row" style="padding: 15px;">'+                                                	
	                                                    '<div class="col-md-12 div-notebook-parameter" style="margin-top: 20px;background-color: white">'+
	                                                    '<h3 style="text-align:center">Parámetros</h3>'+
	                                                        '<div class="row" id="'+idDivParam+'">'+                                                          
	                                                            '<div id="'+idDivParamButton+'" class="col-md-2" style="margin-top: 20px;">'+
	                                                            	'<p>Añadir Parámetro</p>'+
	                                                                '<button id="'+idAddParamButton+'" type="submit" class="btn btn-primary" onclick="alert(\'Para añadir parámetros, guarde la caja de código.\')" >'+
	                                                                   'Añadir'+
	                                                                '</button>'+                                                                
	                                                            '</div>'+
	                                                        '</div>'+
	                                                    '</div>'+
	                                                '</div>'+
	                                        '</div>'+
	                                        '<div id="'+idColChartButtons+'" class="col-md-4" style="margin-top: 20px;">'+
	                                            '<button type="submit" class="btn btn-primary" onclick="evalUserCodeAce('+idEditorParameter+');">'+
	                                               'Ejecutar >>'+
	                                            '</button>'+
	                                            '<br><br>'+
	                                            '<h4>Resultado del código</h4>'+
	                                            '<input name="resultado_'+idEditor+'" class="form-control resultado_code_editor"  id="resultado_'+idEditor+'" type="text" disabled="disabled">'+
	                                            '<br><br>'+
	                                            '<button class="btn btn-primary" onclick="addChart('+idRowPrincipalParameter+','+idBoxParameter+','+idColChartButtonsParameter+');">'+
	                                               'Añadir Gráfica'+
	                                            '</button>'+
	                                        '</div>'+

	                                    '</div>'+
	                                '</div>'+
	                            '</div>'+
	                        '</div>'+
                        '</div>';

	$('#'+idNotebookContent).append(htmlCodeBox);

	var editor = ace.edit(idEditor);
    editor.getSession().setMode("ace/mode/javascript");
    editor.getSession().setTabSize(4);
    editor.getSession().setUseWrapMode(true);
    editor.setFontSize(16);
    editor.setShowPrintMargin(false);
    var heightUpdateFunction = function() {                    
        $('#'+idEditor).height("250px");
        $('#editor-section').height("250px");
        // This call is required for the editor to fix all of
        // its inner structure for adapting to a change in size
        editor.resize();
        };
    // Set initial size to match initial content
    heightUpdateFunction();
    // Whenever a change happens inside the ACE editor, update
    // the size again
    editor.getSession().on('change', heightUpdateFunction);

    // Comportamiento al pulsar SAVE -> Llamada Ajax
    $('#'+idFormBox).on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");
        //MANDAR COMO PARÁMETRO TODO INPUT QUE SEA NECESARIO RECUPERAR EN EL MÉTODO
        var form = $('#'+idFormBox);
        createCodeBox(idHiddenIdNotebook,idHiddenOrder,idEditor,idAddParamButton,idDivParam,idDivParamButton);
    });

    //Se devuelven los IDs de los divs necesarios para mostrar los parámetros
    var respuesta = [idDivParam,idDivParamButton];
    return respuesta;

}

function addImageBox(idNotebookContent){
	numBox++;
	//Box id
	var idBox = "idBox"+numBox;
	var idBoxParameter = "'idBox"+numBox+"'";

	//Img id
	numImg++;
	var idImg = "idImg"+numImg;
	var idImgParameter = "'idImg"+numImg+"'";
	//Input URL id
	var idUrlInput = "idUrlInput"+numImg;
	var idUrlInputParameter = "'idUrlInput"+numImg+"'";


	//HTML DE LA CAJA DE IMAGEN
	var htmlImageBox = '<div class="col-md-12 custom-mt-1" id="'+idBox+'">'+
							'<div class="row">'+
								'<div class="col-md-12 custom-mt-1" >'+
									'<div class="form-group" style="padding:12px;">'+
		                            	'<img class="notebook-img" id="'+idImg+'" src="" height="256px" width="256px" />'+		                         		
		                        	'</div>'+
		                        '</div>'+
		                        '<div class="col-md-6 offset-md-3" >'+
		                        		'<input class="form-control" id="'+idUrlInput+'" type="text" placeholder="Establecer URL">'+
								'</div>'+
								'<div class="col-md-12 offset-md-3" >'+
		                         		'<button class="btn btn-info pull-right" style="margin-top:10px" onclick="updateImg('+idImgParameter+','+idUrlInputParameter+')" type="button">Actualizar URL</button>'+
		                         		'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteElement('+idBoxParameter+')" type="button">Eliminar</button>'+
								'</div>'+
							'</div>'+
						'</div>';

	$('#'+idNotebookContent).append(htmlImageBox);
}

function deleteElement(idElement){
	console.log('hola');
	$('#'+idElement).remove();
}

function updateImg(idImgParameter,idUrlInputParameter){
	urlInputVal = document.getElementById(idUrlInputParameter).value;
	$("#"+idImgParameter).attr("src",urlInputVal);
}


function evalUserCodeAce(idEditor){
    var editor = ace.edit(idEditor);
    var s = editor.getValue();
    var resultado = eval(s);
    document.getElementById("resultado_"+idEditor).value = String(resultado);
}

function addNewParameter(idParameterDiv,idButtonParameter,idBox){
	addParameter(idParameterDiv,idButtonParameter,idBox,null,'',null);
}

function addParameter(idParameterDiv,idButtonParameter,idBox,idParam,paramValue,idNameValue){

	numParameter++;

	/* IDS FORM */
	var idFormParam = "form_param_"+numParameter;
	var idHiddenIdBox = "input_hidden_parameter_id_box_"+numParameter;
	var idHiddenIdPkParam = "input_hidden_parameter_id_pk_param_"+numParameter;
	var idHiddenIdNameParam = "input_hidden_parameter_id_name_param_"+numParameter;
	var idValueParam = "input_parameter_value_"+numParameter;

	/* FIN IDS FORM */

	var idParameterDivParameter = "'"+idParameterDiv+"'";
	var idButtonParameterParameter = "'"+idButtonParameter+"'";

	var idUrlInputParameter = "'idUrlInput"+numImg+"'";

    $('#'+idButtonParameter).remove();
    //Campo usado por el programador, y del que recoger el valor para persistir
    var idNameParameter = '';
    if(idNameValue==null){
    	var idNameParameter = 'param'+numParameter;
	}
	else{
		idNameParameter = idNameValue;
	}

    var htmlParameter 	= 	'<div class="col-md-2" style="margin-top: 20px;">'+
	    						'<form method="POST" id="'+idFormParam+'">'+
									'<input type="hidden" id="'+idHiddenIdBox+'" value="'+idBox+'">'+
									'<input type="hidden" id="'+idHiddenIdPkParam+'" value="'+idParam+'">'+
									'<input type="hidden" id="'+idHiddenIdNameParam+'" value="'+idNameParameter+'">'+
    							'<p>id: '+idNameParameter+'</p>'+
    							'<input value="'+paramValue+'" name="'+idNameParameter+'" class="form-control" id="'+idNameParameter+'" type="text">'+
    							'<button type="submit" class="btn btn-info pull-right" style="margin-top:10px" type="button">Guardar</button>'+
    							'</form>'+
    						'</div>'

    $('#'+idParameterDiv).append(htmlParameter);

    var htmlButton		=	'<div id="'+idButtonParameter+'" class="col-md-2" style="margin-top: 20px;">'+
    							'<p>Añadir Parámetro</p>'+
    							'<button type="submit" class="btn btn-primary" onclick="addNewParameter('+idParameterDivParameter+','+idButtonParameterParameter+',\''+idBox+'\');"> Añadir </button>'+
							'</div>'


    $('#'+idParameterDiv).append(htmlButton);

    // Comportamiento al pulsar SAVE -> Llamada Ajax
    $('#'+idFormParam).on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");
        //MANDAR COMO PARÁMETRO TODO INPUT QUE SEA NECESARIO RECUPERAR EN EL MÉTODO
        var form = $('#'+idFormParam);
        createCodeParam(idHiddenIdBox,idNameParameter,idHiddenIdPkParam,idHiddenIdNameParam);
    });
}

function addChart(idRowPrincipalParameter,idBoxParameter,idColChartButtons){

	var idChart = "myChart_"+idBoxParameter;

	var idChartRow = idChart+'_row';

	var element = $('#'+idChartRow);
	if(element != null){
		$('#'+idChartRow).remove();
	}

	var htmlChart = '<div class="col-md-12" id="'+idChartRow+'" style="height="300">'+
						'<div class="row">'+
							'<div class="col-md-12">'+
								'<b><p style="text-align:center">chart id: '+idChart+'</p></b>'+
							'</div>'+	                    
		                    '<div class="col-md-12">'+
		                        '<canvas class="notebook-chart" id="'+idChart+'" width="auto" height="300"></canvas>'+
		                    '</div>'+
		                '</div>'+
	                '</div>';

	$('#'+idRowPrincipalParameter).append(htmlChart);

	//Botón eliminar gráfica

	//Quitamos previamente el botón de aceptar

	$('#'+idColChartButtons+' button:last-child').remove();


	var htmlDeleteChartButton = '<button type="submit" class="btn btn-primary" onclick="deleteChart(\''+idChartRow+'\',\''+idRowPrincipalParameter+'\',\''+idBoxParameter+'\',\''+idColChartButtons+'\');">'+
                                   'Eliminar Gráfica'+
                                '</button>';

    $('#'+idColChartButtons).append(htmlDeleteChartButton);

	//Mostrar la gráfica con valores por defecto

	var ctx = document.getElementById(idChart);
	var myChart = new Chart(ctx, {
	    type: 'line',
	    data: {
	        labels: [],
	        datasets: [{
	            label: 'Nombre Gráfica',
	            data: [],
	            backgroundColor: [
	                'rgba(255, 99, 132, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(255, 206, 86, 0.2)',
	                'rgba(75, 192, 192, 0.2)',
	                'rgba(153, 102, 255, 0.2)',
	                'rgba(255, 159, 64, 0.2)'
	            ],
	            borderColor: [
	                'rgba(255,99,132,1)',
	                'rgba(54, 162, 235, 1)',
	                'rgba(255, 206, 86, 1)',
	                'rgba(75, 192, 192, 1)',
	                'rgba(153, 102, 255, 1)',
	                'rgba(255, 159, 64, 1)'
	            ],
	            borderWidth: 1
	        }]
	    },
	    options: {
	    	chartArea: {
		        backgroundColor: 'rgba(251, 255, 255, 0.4)',
		    },
	        maintainAspectRatio: false,
	        scales: {
	            yAxes: [{
	                ticks: {
	                    beginAtZero:true
	                }
	            }]
	        }
	    }
	});

}

function deleteChart(idChartRow,idRowPrincipalParameter,idBoxParameter,idColChartButtons){

	var element = $('#'+idChartRow);
	if(element != null){
		$('#'+idChartRow).remove();
	}

	$('#'+idColChartButtons+' button:last-child').remove();


	var htmlAddChartButton = 	'<button type="submit" class="btn btn-primary" onclick="addChart(\''+idRowPrincipalParameter+'\',\''+idBoxParameter+'\',\''+idColChartButtons+'\');">'+
                            		'Añadir Gráfica'+
                            	'</button>';

    $('#'+idColChartButtons).append(htmlAddChartButton);

}



/*GESTION DE FORMULARIOS*/


// AJAX for posting
function create_notebook() {
    console.log("create notebook is working!") // sanity check
    console.log($('#post-text').val())
};

// AJAX para actualizar el notebook

function editExerciseInfo(){
    console.log("send title is working!"); // sanity check
    var title = $('#title').val();
    var description = $('#description').val();
    var idNotebook = $('#idNotebook').val();
    //TODO MBC VALIDAR CAMPOS
    //alert("Mandando por Ajax el título: "+ title+" y descripción: "+description);
    $.ajax({
        url : "/web/editNotebookAjax", // the endpoint
        type : "POST", // http method
        data : { 
        'title': title,
        'description': description,
        'idNotebook': idNotebook
        
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //alert("Notebook editado correctamente");
            //Actualización de los campos
            var newTitle = json['editedExerciseTitle'];
            $('#title').val(newTitle);
            var newDescription = json['editedExerciseDescription'];
            $('#description').val(newDescription);
            console.log("success"); // another sanity check
            
            $('#notification-text').text('Editado correctamente');
            $('#notificaciones-holder').slideDown();
            
            setTimeout(
              function() 
              {
                $('#notificaciones-holder').slideUp();
              }, 2000);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //TODO MBC SI FALLA REINICIAR LOS INPUTS A LOS VALORES QUE ESTABAN PERSISTIDOS
            $('#notification-text').text('Error al editar');
            $('#notificaciones-holder').show();

            setTimeout(
              function() 
              {
                $('#notificaciones-holder').hide();
              }, 2000);
        }
	});
}

//AJAX para crear code box

function createCodeBox(idHiddenIdNotebook, idHiddenOrder, idEditor, idAddParamButton, idDivParam, idDivParamButton){
	console.log("Retrieving code box fields"); // sanity check
	var idNotebook = $('#'+idHiddenIdNotebook).val();
	var boxOrder = $('#'+idHiddenOrder).val();

	//Recuperando el código del editor como String
	var editor = ace.edit(idEditor);
    var contentCode = editor.getValue();

	console.log("Recuperado idNotebook: "+idNotebook);
	console.log("Recuperado boxOrder: "+boxOrder);
	console.log("Recuperado código: "+contentCode);

	$.ajax({
        url : "/web/createCodeBoxAjax", // the endpoint
        type : "POST", // http method
        data : { 
        'idNotebook': idNotebook,
        'boxOrder': boxOrder,
        'contentCode': contentCode
        }, // data sent with the post request
        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //alert("Notebook editado correctamente");
            //Actualización de los campos
            console.log("success"); // another sanity check
            //$("#getCodeModal").modal('show');
            $('#notification-text').text('Code Box creada correctamente');
            $('#notificaciones-holder').slideDown();
            setTimeout(
              function() 
              {
                $('#notificaciones-holder').slideUp();
              }, 2000);

            //Activar el botón de añadir parámetros para esa caja de código
            //Recuperar id box
            var idBox = json['createdBoxId'];

            $('#'+idAddParamButton).attr("onclick","addNewParameter(\'"+idDivParam+"\',\'"+idDivParamButton+"\',\'"+idBox+"\')");

            //onclick="addParameter('+idDivParamParameter+','+idDivParamButtonParameter+');"

            //NECESITAMOS ID DEL BOTÓN, '+idDivParamParameter+','+idDivParamButtonParameter+'
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //TODO MBC SI FALLA REINICIAR LOS INPUTS A LOS VALORES QUE ESTABAN PERSISTIDOS
            $('#notification-text').text('Error al editar');
            $('#notificaciones-holder').show();

            setTimeout(
              function() 
              {
                $('#notificaciones-holder').hide();
              }, 2000);
        }
	});

}

//AJAX para crear code param

function createCodeParam(idHiddenIdBox,idValueParameter,idHiddenIdPkParam,idHiddenIdNameParam){
	console.log("Retrieving code param fields"); // sanity check
	var idBox = $('#'+idHiddenIdBox).val();
	var paramValue = $('#'+idValueParameter).val();
	//PK del parámetro
	var idPkParam = $('#'+idHiddenIdPkParam).val();
	//Id del input del parámetro
	var nameIdParam = $('#'+idHiddenIdNameParam).val();

	console.log("Recuperado idBox: "+idBox);
	console.log("Recuperado paramValue: "+paramValue);
	console.log("Recuperado idPkParam: "+idPkParam);
	console.log("Recuperado nameIdParam: "+nameIdParam);

	$.ajax({
        url : "/web/createCodeParamAjax", // the endpoint
        type : "POST", // http method
        data : { 
        'idBox': idBox,
        'paramValue': paramValue,
        'idPkParam': idPkParam,
        'nameIdParam': nameIdParam
        }, // data sent with the post request
        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //alert("Notebook editado correctamente");
            //Actualización de los campos
            console.log("success"); // another sanity check
            //$("#getCodeModal").modal('show');
            $('#notification-text').text('Code Param creado correctamente');
            $('#notificaciones-holder').slideDown();
            setTimeout(
              function() 
              {
                $('#notificaciones-holder').slideUp();
              }, 2000);

            //Activar el botón de añadir parámetros para esa caja de código
            //Recuperar id box
            var idBox = json['createdBoxId'];

            $('#'+idAddParamButton).attr("onclick","addNewParameter(\'"+idDivParam+"\',\'"+idDivParamButton+"\',\'"+idBox+"\')");

            //onclick="addParameter('+idDivParamParameter+','+idDivParamButtonParameter+');"

            //NECESITAMOS ID DEL BOTÓN, '+idDivParamParameter+','+idDivParamButtonParameter+'
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //TODO MBC SI FALLA REINICIAR LOS INPUTS A LOS VALORES QUE ESTABAN PERSISTIDOS
            $('#notification-text').text('Error al editar');
            $('#notificaciones-holder').show();

            setTimeout(
              function() 
              {
                $('#notificaciones-holder').hide();
              }, 2000);
        }
	});

}

//AJAX para crear text box

function createTextBox(idHiddenIdNotebook, idHiddenOrder, idInputText){
	console.log("Retrieving text box fields"); // sanity check
	var idNotebook = $('#'+idHiddenIdNotebook).val();
	var boxOrder = $('#'+idHiddenOrder).val();
	var text = $('#'+idInputText).val();
	console.log("Recuperado idNotebook: "+idNotebook);
	console.log("Recuperado boxOrder: "+boxOrder);
	console.log("Recuperado text: "+text);

	$.ajax({
        url : "/web/createTextBoxAjax", // the endpoint
        type : "POST", // http method
        data : { 
        'idNotebook': idNotebook,
        'boxOrder': boxOrder,
        'text': text
        
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //alert("Notebook editado correctamente");
            //Actualización de los campos
            console.log("success"); // another sanity check
            //$("#getCodeModal").modal('show');
            $('#notification-text').text('Box creada correctamente');
            $('#notificaciones-holder').slideDown();
            
            setTimeout(
              function() 
              {
                $('#notificaciones-holder').slideUp();
              }, 2000);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //TODO MBC SI FALLA REINICIAR LOS INPUTS A LOS VALORES QUE ESTABAN PERSISTIDOS
            $('#notification-text').text('Error al editar');
            $('#notificaciones-holder').show();

            setTimeout(
              function() 
              {
                $('#notificaciones-holder').hide();
              }, 2000);
        }
	});

}