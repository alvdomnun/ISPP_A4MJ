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
			                            	'<textarea id="'+idInputText+'" onkeyup="auto_grow(this)" class="form-control text-box-textarea" placeholder="Escribe aquí" required>'+content+'</textarea>'+
			                         		'<button type="submit" class="btn btn-info pull-right" style="margin-top:10px" type="button">Guardar</button>'+
			                         		'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteTextBox(\''+idHiddenIdNotebook+'\',\''+idHiddenIdBox+'\',\''+idBox+'\')" type="button">Eliminar</button>'+
		                        		'</form>'+
		                        	'</div>'+
								'</div>'+
							'</div>'+
						'</div>';

    $('#'+idNotebookContent).append(htmlTextBox);

    // Comportamiento al pulsar GUARDAR -> Llamada Ajax

    $('#'+idFormBox).on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");
        //MANDAR COMO PARÁMETRO TODO INPUT QUE SEA NECESARIO RECUPERAR EN EL MÉTODO
        createUpdateTextBox(idHiddenIdNotebook,idHiddenOrder,idInputText,idHiddenIdBox);
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
												'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteCodeBox(\''+idHiddenIdNotebook+'\',\''+idHiddenIdBox+'\',\''+idBox+'\')" type="button">Eliminar</button>'+
											'</form>'+
	                                        
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

    // Comportamiento al pulsar GUARDAR -> Llamada Ajax
    $('#'+idFormBox).on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");
        //MANDAR COMO PARÁMETRO TODO INPUT QUE SEA NECESARIO RECUPERAR EN EL MÉTODO
        var form = $('#'+idFormBox);
        createUpdateCodeBox(idHiddenIdNotebook,idHiddenOrder,idHiddenIdBox,idEditor,idAddParamButton,idDivParam,idDivParamButton);
    });

    //Se devuelven los IDs de los divs necesarios para mostrar los parámetros
    var respuesta = [idDivParam,idDivParamButton];
    return respuesta;

}

function addNewImageBox(idNotebookContent,idNotebookBD){
	addImageBox(idNotebookContent,idNotebookBD,null,null,'');
}

function addImageBox(idNotebookContent,idNotebookBD,order,idBoxBD,url){
	numBox++;
	//Box id
	var idBox = "idBox"+numBox;

	//Img id
	var idImg = "idImg"+idBox;
	//Input URL id
	var idUrlInput = "input_url_img_"+idBox;

	var idFormBox = "form_box_"+idBox;
	var idHiddenIdBox = "input_hidden_id_box_"+idBox;
	var idHiddenIdNotebook = "input_hidden_id_notebook_"+idBox;
	var idHiddenOrder = "input_hidden_order_"+idBox;

	if(order==null){
		var order = numBox;
	}
    var urlImg = '/static/img/placeholder.png'
	if(url==null || url==""){
		url = '';
	}else{
	    urlImg = url;
	}

	//HTML DE LA CAJA DE IMAGEN
	var htmlImageBox = '<div class="col-md-12 custom-mt-1" id="'+idBox+'">'+
							'<div class="row">'+
								'<div class="col-md-12 custom-mt-1" >'+
									'<div class="form-group" style="padding:12px;">'+
		                            	'<img class="notebook-img" id="'+idImg+'" src="'+urlImg+'" height="256px" />'+
		                        	'</div>'+
		                        '</div>'+
		                        '<div class="form-group col-md-6 offset-md-3" style="padding:12px;">'+
									'<form method="POST" id="'+idFormBox+'">'+
										'<input type="hidden" id="'+idHiddenIdNotebook+'" value="'+idNotebookBD+'">'+
										'<input type="hidden" id="'+idHiddenIdBox+'" value="'+idBoxBD+'">'+
										'<input type="hidden" id="'+idHiddenOrder+'" value="'+order+'">'+
				                        '<input class="form-control col-md-5 offset-md-3" id="'+idUrlInput+'" type="text" placeholder="Establecer URL" required value="'+url+'">'+
										'<div class="col-md-12 offset-md-3" >'+
				                         		'<button type="submit" class="btn btn-info pull-right" style="margin-top:10px" type="button">Guardar</button>'+
				                         		'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteImageBox(\''+idHiddenIdNotebook+'\',\''+idHiddenIdBox+'\',\''+idBox+'\')" type="button">Eliminar</button>'+
										'</div>'+
									'</form>'+
								'</div>'+
							'</div>'+
						'</div>';

	$('#'+idNotebookContent).append(htmlImageBox);

	// Comportamiento al pulsar GUARDAR -> Llamada Ajax
    $('#'+idFormBox).on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");
        //MANDAR COMO PARÁMETRO TODO INPUT QUE SEA NECESARIO RECUPERAR EN EL MÉTODO
        //var form = $('#'+idFormBox);
        createUpdateImageBox(idHiddenIdNotebook,idHiddenOrder,idUrlInput,idHiddenIdBox,idImg);
    });
}

function deleteElement(idElement){
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
	addParameter(idParameterDiv,idButtonParameter,idBox,null,'',null,null);
}

function addParameter(idParameterDiv,idButtonParameter,idBox,idParam,paramValue,idNameValue,nameParam){

	numParameter++;

	/* IDS FORM */
	var idFormParam = "form_param_"+numParameter;
	var idDivParam = "div_param_"+numParameter;
	var idHiddenIdBox = "input_hidden_parameter_id_box_"+numParameter;
	var idHiddenIdPkParam = "input_hidden_parameter_id_pk_param_"+numParameter;
	//El nombre del id para obtenerse por código
	var idHiddenIdNameParam = "input_hidden_parameter_id_name_param_"+numParameter;
	//El nombre del parámetro establecido por el usuario
	var idNameParam = "input__name_param_"+numParameter;
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

	if(nameParam==null){
		nameParam = '';
	}

    var htmlParameter 	= 	'<div id="'+idDivParam+'" class="col-xs-4 col-md-4" style="margin-top: 20px;">'+
	    						'<form method="POST" id="'+idFormParam+'">'+
									'<input type="hidden" id="'+idHiddenIdBox+'" value="'+idBox+'">'+
									'<input type="hidden" id="'+idHiddenIdPkParam+'" value="'+idParam+'">'+
									'<input type="hidden" id="'+idHiddenIdNameParam+'" value="'+idNameParameter+'">'+
								'<label class="control-label">ID</label>'+
    							'<input value="'+idNameParameter+'" class="form-control" type="text" disabled="disabled">'+
    							'<label for="'+idNameParam+'" class="control-label">Nombre</label>'+
    							'<input value="'+nameParam+'" name="'+idNameParam+'" class="form-control" id="'+idNameParam+'" type="text" required>'+
    							'<label for="'+idNameParameter+'" class="control-label">Valor</label>'+
    							'<input value="'+paramValue+'" name="'+idNameParameter+'" class="form-control" id="'+idNameParameter+'" type="text" required>'+
    							'<button type="submit" class="btn btn-primary pull-right" style="margin-top:10px" type="button">Guardar</button>'+
    							'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteParam(\''+idDivParam+'\',\''+idHiddenIdPkParam+'\')" type="button">Eliminar</button>'+
    							'</form>'+
    						'</div>'




    $('#'+idParameterDiv).append(htmlParameter);

    var htmlButton		=	'<div id="'+idButtonParameter+'" class="col-md-2" style="margin-top: 20px;">'+
    							'<p>Añadir Parámetro</p>'+
    							'<button type="submit" class="btn btn-primary" onclick="addNewParameter('+idParameterDivParameter+','+idButtonParameterParameter+',\''+idBox+'\');"> Añadir </button>'+
							'</div>'


    $('#'+idParameterDiv).append(htmlButton);

    // Comportamiento al pulsar GUARDAR -> Llamada Ajax
    $('#'+idFormParam).on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");
        //MANDAR COMO PARÁMETRO TODO INPUT QUE SEA NECESARIO RECUPERAR EN EL MÉTODO
        var form = $('#'+idFormParam);
        createUpdateCodeParam(idHiddenIdBox,idNameParameter,idHiddenIdPkParam,idHiddenIdNameParam,idNameParam);
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
    var level = $('#level').val();
    var category = $('#category').val();
    var idNotebook = $('#idNotebook').val();
    //TODO MBC VALIDAR CAMPOS
    //alert("Mandando por Ajax el título: "+ title+" y descripción: "+description);
    $.ajax({
        url : "/web/editNotebookAjax", // the endpoint
        type : "POST", // http method
        data : { 
        'title': title,
        'description': description,
        'level': level,
        'category': category,
        'idNotebook': idNotebook

        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //alert("Notebook editado correctamente");
            //Actualización de los campos
            var newTitle = json['editedExerciseTitle'];
            $('#title').val(newTitle);
            $('#title_disabled').val(newTitle);
            var newDescription = json['editedExerciseDescription'];
            $('#description').val(newDescription);
            $('#description_disabled').val(newDescription);
            var newLevel = json['editedExerciseLevel'];
            $('#level').val(newLevel);
            $('#level_disabled').val(newLevel);
            var newCategory = json['editedExerciseCategory'];
            var newCategoryId = json['editedExerciseCategoryId'];

            $('#category').val(newCategoryId);
            $('#category_disabled').val(newCategory);
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

function createUpdateCodeBox(idHiddenIdNotebook, idHiddenOrder, idHiddenIdBox, idEditor, idAddParamButton, idDivParam, idDivParamButton){
	console.log("Retrieving code box fields"); // sanity check
	var idNotebook = $('#'+idHiddenIdNotebook).val();
	var boxOrder = $('#'+idHiddenOrder).val();
	var idBox = $('#'+idHiddenIdBox).val();

	//Recuperando el código del editor como String
	var editor = ace.edit(idEditor);
    var contentCode = editor.getValue();

	console.log("Recuperado idNotebook: "+idNotebook);
	console.log("Recuperado boxOrder: "+boxOrder);
	console.log("Recuperado código: "+contentCode);
	console.log("Recuperado idBox: "+idBox);

	$.ajax({
        url : "/web/createUpdateCodeBoxAjax", // the endpoint
        type : "POST", // http method
        data : {
        'idNotebook': idNotebook,
        'boxOrder': boxOrder,
        'contentCode': contentCode,
        'idBox': idBox,
        }, // data sent with the post request
        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //alert("Notebook editado correctamente");
            //Actualización de los campos
            console.log("success"); // another sanity check
            //$("#getCodeModal").modal('show');
            
			//Se comprueba si el box ha sido creado o actua
            var updateBox = json['updateBox'];
            if(updateBox){
            	$('#notification-text').text('Box editada correctamente');
            }else{
            	$('#notification-text').text('Box creada correctamente');
            }

            $('#notificaciones-holder').slideDown();
            setTimeout(
              function() 
              {
                $('#notificaciones-holder').slideUp();
              }, 2000);

            //Activar el botón de añadir parámetros para esa caja de código
            //Recuperar id box
            var idBox = json['savedBoxId'];
            //Actualizar el campo idbox, por si se está creando
            $('#'+idHiddenIdBox).val(idBox);

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

function createUpdateCodeParam(idHiddenIdBox,idValueParameter,idHiddenIdPkParam,idHiddenIdNameParam,idNameParam){
	console.log("Retrieving code param fields"); // sanity check
	var idBox = $('#'+idHiddenIdBox).val();
	var paramValue = $('#'+idValueParameter).val();
	//PK del parámetro
	var idPkParam = $('#'+idHiddenIdPkParam).val();
	//Id del input del parámetro
	var nameIdParam = $('#'+idNameParam).val();
	//Nombre del parámetro, establecido por el usuario
	var nameParam = $('#'+idNameParam).val();
	

	console.log("Recuperado idBox: "+idBox);
	console.log("Recuperado paramValue: "+paramValue);
	console.log("Recuperado idPkParam: "+idPkParam);
	console.log("Recuperado nameIdParam: "+nameIdParam);
	console.log("Recuperado nameParam: "+nameParam);

	$.ajax({
        url : "/web/createUpdateCodeParamAjax", // the endpoint
        type : "POST", // http method
        data : { 
        'idBox': idBox,
        'paramValue': paramValue,
        'idPkParam': idPkParam,
        'nameIdParam': nameIdParam,
        'nameParam': nameParam,
        }, // data sent with the post request
        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //alert("Notebook editado correctamente");
            //Actualización de los campos
            console.log("success"); // another sanity check
            //$("#getCodeModal").modal('show');
            //Se comprueba si el box ha sido creado o actua
            var updateParam = json['updateParam'];
            if(updateParam){
            	$('#notification-text').text('Parámetro editado correctamente');
            }else{
            	$('#notification-text').text('Parámetro creado correctamente');
            }

            $('#notificaciones-holder').slideDown();
            
            setTimeout(
              function() 
              {
                $('#notificaciones-holder').slideUp();
              }, 2000);

            //Recuperar id param
            var idPkParam = json['savedParamId'];
            //Actualizar el campo idbox, por si se está creando
            $('#'+idHiddenIdPkParam).val(idPkParam);



            //$('#'+idAddParamButton).attr("onclick","addNewParameter(\'"+idDivParam+"\',\'"+idDivParamButton+"\',\'"+idBox+"\')");

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
function createUpdateImageBox(idHiddenIdNotebook, idHiddenOrder, idUrlInput, idHiddenIdBox, idImg){
	console.log("Retrieving text box fields"); // sanity check
	var idNotebook = $('#'+idHiddenIdNotebook).val();
	var boxOrder = $('#'+idHiddenOrder).val();
	var url = $('#'+idUrlInput).val();
	var idBox = $('#'+idHiddenIdBox).val();

	console.log("Recuperado idNotebook: "+idNotebook);
	console.log("Recuperado boxOrder: "+boxOrder);
	console.log("Recuperado url: "+url);
	console.log("Recuperado idBox: "+idBox);

	$.ajax({
        url : "/web/createUpdateImageBoxAjax", // the endpoint
        type : "POST", // http method
        data : { 
        'idNotebook': idNotebook,
        'boxOrder': boxOrder,
        'url': url,
        'idBox': idBox
        
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //alert("Notebook editado correctamente");
            //Actualización de los campos
            console.log("success"); // another sanity check
            //$("#getCodeModal").modal('show');

            //Se comprueba si el box ha sido creado o actua
            var updateBox = json['updateBox'];
            if(updateBox){
            	$('#notification-text').text('Caja de ilustración editada correctamente');
            }else{
            	$('#notification-text').text('Caja de ilustración creada correctamente');
            }
            
            $('#notificaciones-holder').slideDown();
            
            setTimeout(
              function() 
              {
                $('#notificaciones-holder').slideUp();
              }, 2000);

            //Activar el botón de añadir parámetros para esa caja de texto
            //Recuperar id box
            var idBox = json['savedBoxId'];
            //Actualizar el campo idbox, por si se está creando
            $('#'+idHiddenIdBox).val(idBox);

            //Mostrar la imagen en el img
            $("#"+idImg).attr("src",url);

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
function createUpdateTextBox(idHiddenIdNotebook, idHiddenOrder, idInputText, idHiddenIdBox){
	console.log("Retrieving text box fields"); // sanity check
	var idNotebook = $('#'+idHiddenIdNotebook).val();
	var boxOrder = $('#'+idHiddenOrder).val();
	var text = $('#'+idInputText).val();
	var idBox = $('#'+idHiddenIdBox).val();

	console.log("Recuperado idNotebook: "+idNotebook);
	console.log("Recuperado boxOrder: "+boxOrder);
	console.log("Recuperado text: "+text);
	console.log("Recuperado idBox: "+idBox);

	$.ajax({
        url : "/web/createUpdateTextBoxAjax", // the endpoint
        type : "POST", // http method
        data : { 
        'idNotebook': idNotebook,
        'boxOrder': boxOrder,
        'text': text,
        'idBox': idBox
        
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            //alert("Notebook editado correctamente");
            //Actualización de los campos
            console.log("success"); // another sanity check
            //$("#getCodeModal").modal('show');

            //Se comprueba si el box ha sido creado o actua
            var updateBox = json['updateBox'];
            if(updateBox){
            	$('#notification-text').text('Box editada correctamente');
            }else{
            	$('#notification-text').text('Box creada correctamente');
            }
            
            $('#notificaciones-holder').slideDown();
            
            setTimeout(
              function() 
              {
                $('#notificaciones-holder').slideUp();
              }, 2000);

            //Activar el botón de añadir parámetros para esa caja de texto
            //Recuperar id box
            var idBox = json['savedBoxId'];
            //Actualizar el campo idbox, por si se está creando
            $('#'+idHiddenIdBox).val(idBox);
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

//AJAX para eliminar code box
function deleteCodeBox(idHiddenIdNotebook,idHiddenIdBox,idBoxParameter){
	console.log("Retrieving ids text box fields"); // sanity check
	var idNotebook = $('#'+idHiddenIdNotebook).val();
	var idBox = $('#'+idHiddenIdBox).val();

	console.log("Recuperado idNotebook: "+idNotebook);
	console.log("Recuperado idBox: "+idBox);

	mensajeConfirmacion = '¿Seguro que quiere eliminar esta caja de código? Se eliminarán los parámetros y gráfica asociados. Esta acción no se puede deshacer';

	var confirmacion = confirm(mensajeConfirmacion);
	if (confirmacion) {
		//Si idBox no es vacío, la caja ya ha sido persistida y debe eliminarse de BD, antes de eliminar el código HTML correspondiente
		if(idBox!=null && idBox!='null'){
			$.ajax({
	        url : "/web/deleteCodeBoxAjax", // the endpoint
	        type : "POST", // http method
	        data : { 
	        'idNotebook': idNotebook,
	        'idBox': idBox
	        }, // data sent with the post request

	        // handle a successful response
	        success : function(json) {
	            console.log(json); // log the returned json to the console
	            //alert("Notebook editado correctamente");
	            //Actualización de los campos
	            console.log("success"); // another sanity check
	            //$("#getCodeModal").modal('show');

	            //Se comprueba si el box ha sido creado o actua
	        	$('#notification-text').text('Caja de código borrada correctamente');

	            $('#notificaciones-holder').slideDown();
	            
	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').slideUp();
	              }, 2000);

	            deleteElement(idBoxParameter);

	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {
	            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
	            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	            //TODO MBC SI FALLA REINICIAR LOS INPUTS A LOS VALORES QUE ESTABAN PERSISTIDOS
	            $('#notification-text').text('Error al eliminar');
	            $('#notificaciones-holder').show();

	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').hide();
	              }, 2000);
	        }
		});
		}else{
			deleteElement(idBoxParameter);
		}
	}
	
}


//AJAX para eliminar text box
function deleteTextBox(idHiddenIdNotebook,idHiddenIdBox,idBoxParameter){
	console.log("Retrieving ids text box fields"); // sanity check
	var idNotebook = $('#'+idHiddenIdNotebook).val();
	var idBox = $('#'+idHiddenIdBox).val();

	console.log("Recuperado idNotebook: "+idNotebook);
	console.log("Recuperado idBox: "+idBox);

	mensajeConfirmacion = '¿Seguro que quiere eliminar esta caja de texto?';

	var confirmacion = confirm(mensajeConfirmacion);
	if (confirmacion) {
		//Si idBox no es vacío, la caja ya ha sido persistida y debe eliminarse de BD, antes de eliminar el código HTML correspondiente
		if(idBox!=null && idBox!='null'){
			$.ajax({
	        url : "/web/deleteTextBoxAjax", // the endpoint
	        type : "POST", // http method
	        data : { 
	        'idNotebook': idNotebook,
	        'idBox': idBox
	        
	        }, // data sent with the post request

	        // handle a successful response
	        success : function(json) {
	            console.log(json); // log the returned json to the console
	            //alert("Notebook editado correctamente");
	            //Actualización de los campos
	            console.log("success"); // another sanity check
	            //$("#getCodeModal").modal('show');

	            //Se comprueba si el box ha sido creado o actua
	        	$('#notification-text').text('Box borrada correctamente');

	            $('#notificaciones-holder').slideDown();
	            
	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').slideUp();
	              }, 2000);

	            deleteElement(idBoxParameter);

	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {
	            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
	            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	            //TODO MBC SI FALLA REINICIAR LOS INPUTS A LOS VALORES QUE ESTABAN PERSISTIDOS
	            $('#notification-text').text('Error al eliminar');
	            $('#notificaciones-holder').show();

	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').hide();
	              }, 2000);
	        }
		});
		}else{
			deleteElement(idBoxParameter);
		}
	}
	
}

//AJAX para eliminar parametro
function deleteParam(idDivParam,idPkParam){
	console.log("Retrieving ids text box fields"); // sanity check

	var idParam = $('#'+idPkParam).val();

	mensajeConfirmacion = '¿Seguro que quiere eliminar este parámetro?';

	var confirmacion = confirm(mensajeConfirmacion);
	if (confirmacion) {
		//Si idBox no es vacío, la caja ya ha sido persistida y debe eliminarse de BD, antes de eliminar el código HTML correspondiente
		if(idParam!=null && idParam!='null'){
			$.ajax({
	        url : "/web/deleteParamAjax", // the endpoint
	        type : "POST", // http method
	        data : { 
	        'idParam': idParam	        
	        }, // data sent with the post request

	        // handle a successful response
	        success : function(json) {
	            console.log(json); // log the returned json to the console
	            //alert("Notebook editado correctamente");
	            //Actualización de los campos
	            console.log("success"); // another sanity check
	            //$("#getCodeModal").modal('show');

	            //Se comprueba si el box ha sido creado o actua
	        	$('#notification-text').text('Parámetro borrado correctamente');

	            $('#notificaciones-holder').slideDown();
	            
	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').slideUp();
	              }, 2000);

	            deleteElement(idDivParam);

	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {
	            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
	            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	            //TODO MBC SI FALLA REINICIAR LOS INPUTS A LOS VALORES QUE ESTABAN PERSISTIDOS
	            $('#notification-text').text('Error al eliminar');
	            $('#notificaciones-holder').show();

	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').hide();
	              }, 2000);
	        }
		});
		}else{
			deleteElement(idDivParam);
		}
	}
	
}

//AJAX para eliminar text box
function deleteImageBox(idHiddenIdNotebook,idHiddenIdBox,idBoxParameter){
	console.log("Retrieving ids text box fields"); // sanity check
	var idNotebook = $('#'+idHiddenIdNotebook).val();
	var idBox = $('#'+idHiddenIdBox).val();

	console.log("Recuperado idNotebook: "+idNotebook);
	console.log("Recuperado idBox: "+idBox);

	mensajeConfirmacion = '¿Seguro que quiere eliminar esta caja de ilustración?';

	var confirmacion = confirm(mensajeConfirmacion);
	if (confirmacion) {
		//Si idBox no es vacío, la caja ya ha sido persistida y debe eliminarse de BD, antes de eliminar el código HTML correspondiente
		if(idBox!=null && idBox!='null'){
			$.ajax({
	        url : "/web/deleteImageBoxAjax", // the endpoint
	        type : "POST", // http method
	        data : { 
	        'idNotebook': idNotebook,
	        'idBox': idBox
	        
	        }, // data sent with the post request

	        // handle a successful response
	        success : function(json) {
	            console.log(json); // log the returned json to the console
	            //alert("Notebook editado correctamente");
	            //Actualización de los campos
	            console.log("success"); // another sanity check
	            //$("#getCodeModal").modal('show');

	            //Se comprueba si el box ha sido creado o actua
	        	$('#notification-text').text('Box borrada correctamente');

	            $('#notificaciones-holder').slideDown();
	            
	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').slideUp();
	              }, 2000);

	            deleteElement(idBoxParameter);

	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {
	            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
	            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	            //TODO MBC SI FALLA REINICIAR LOS INPUTS A LOS VALORES QUE ESTABAN PERSISTIDOS
	            $('#notification-text').text('Error al eliminar');
	            $('#notificaciones-holder').show();

	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').hide();
	              }, 2000);
	        }
		});
		}else{
			deleteElement(idBoxParameter);
		}
	}
	
}
