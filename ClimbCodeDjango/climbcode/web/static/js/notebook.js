//Variables para generar ids unicos
var numBox = 0;
var numImg = 0;
var maxOrder = 0;
//Variable global seteada
var numParam = 0;

/*Variables para la gestión del guardado como borrador y publicación*/
//Array con los IDS de los formularios de las cajas
var boxFormsButtons = [];
var boxForms = [];
var savingDraft = false;
//Si ha ocurrido un problema guardando las cajas, se notifica con la siguiente variable 
var errorBatchSave = false;

//Constante para recuperar parámetro para el Iframe
var ID_HIDDEN_NAME_PARAM = "input_hidden_parameter_id_name_param_";

function prueba(){
	alert(saludo);
}

function addNewTextBox(idNotebookContent,idNotebookBD){
	addTextBox(idNotebookContent,idNotebookBD,null,null,'');
}

function addTextBox(idNotebookContent,idNotebookBD,order,idBoxBD,content){

	var vistaEdicion = true;

	numBox++;
	var idBox = "idBox"+numBox;
	var idBoxParameter = "'idBox"+numBox+"'";
	var idFormBox = "form_box_"+idBox;
	var idFormBoxSubmitButton = "form_box_submit_button_"+idBox;
	var idInputText = "input_text_box_"+idBox;
	var idHiddenIdNotebook = "input_hidden_id_notebook_"+idBox;
	var idHiddenOrder = "input_hidden_order_"+idBox;
	var idHiddenIdBox = "input_hidden_id_box_"+idBox;
	if(order==null){
		maxOrder++;
		var order = maxOrder;
	}

	//Contar número de saltos de línea en content
	var numSaltos = content.split(/\r\n|\r|\n/).length;

	//HTML DE LA CAJA DE TEXTO
	var htmlTextBox = 	'<div class="col-md-10 custom-mt-1 offset-md-1" id="'+idBox+'">'+
							'<div class="row">'+
								'<div class="col-md-12 custom-mt-1" >'+
									'<div class="form-group" style="padding:12px;">';
					if(vistaEdicion){
						htmlTextBox+=   '<form method="POST" id="'+idFormBox+'">'+
											'<input type="hidden" id="'+idHiddenIdNotebook+'" value="'+idNotebookBD+'">'+
											'<input type="hidden" id="'+idHiddenOrder+'" value="'+order+'">'+
											'<input type="hidden" id="'+idHiddenIdBox+'" value="'+idBoxBD+'">';
					}
		                htmlTextBox+=		'<textarea id="'+idInputText+'" onkeyup="auto_grow(this)" class="form-control text-box-textarea" placeholder="Escribe aquí" required>'+content+'</textarea>';
		            if(vistaEdicion){
		                htmlTextBox+=   	'<button id="'+idFormBoxSubmitButton+'" type="submit" class="btn btn-info pull-right" style="margin-top:10px" type="button">Guardar</button>'+
		                         			'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteTextBox(\''+idHiddenIdNotebook+'\',\''+idHiddenIdBox+'\',\''+idBox+'\',\''+idFormBoxSubmitButton+'\',\''+idFormBox+'\')" type="button">Eliminar</button>'+
                        				'</form>';
	                }
           			htmlTextBox+= '</div>'+
								'</div>'+
							'</div>'+
						'</div>';

    $('#'+idNotebookContent).append(htmlTextBox);

    for(i=0;i<numSaltos;i++){
    	var element = $('#'+idInputText);
    	auto_grow(element[0]);
    }

    // Comportamiento al pulsar GUARDAR -> Llamada Ajax

    $('#'+idFormBox).on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");
        //MANDAR COMO PARÁMETRO TODO INPUT QUE SEA NECESARIO RECUPERAR EN EL MÉTODO
        createUpdateTextBox(idHiddenIdNotebook,idHiddenOrder,idInputText,idHiddenIdBox);
    });

    //Añadimos el id del formulario al array de formularios para guardado borrador y publicar
    addBoxFormButton(idFormBoxSubmitButton);
    addBoxForm(idFormBox);

}

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}

function addNewCodeBox(idNotebookContent,idNotebookBD){
	return addCodeBox(idNotebookContent,idNotebookBD,null,null,'',null);
}

function addCodeBox(idNotebookContent,idNotebookBD,order,idBoxBD,content,idChart){

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
	var idAddGraphicButton = "id_add_graphic_button_"+numBox;
	var idRowPrincipal = "id_code_box_row_"+idBox;
	var idRowPrincipalParameter = "'id_code_box_row_"+idBox+"'";
	//Div Col Add Delete Button Chart
	var idColChartButtons = "id_col_chart_buttons_"+idBox;
	var idColChartButtonsParameter = "'id_col_chart_buttons_"+idBox+"'";

	//ID IFRAME
	var idIframe = "id_iframe_code_box_"+numBox;

	//ID INPUT RESULTADO CODIGO
	var idInputResultado = 'resultado_'+idEditor;

	/* IDS FORM */
	var idFormBox = "form_box_"+idBox;
	var idFormBoxSubmitButton = "form_box_submit_button_"+idBox;
	var idHiddenIdNotebook = "input_hidden_id_notebook_"+idBox;
	var idHiddenOrder = "input_hidden_order_"+idBox;
	var idHiddenIdBox = "input_hidden_id_box_"+idBox;
	if(order==null){
		maxOrder++;
		var order = maxOrder;
	}

	if(content==''||content==null){
		content='//Escribe tu ejercicio con JavaScript\n'+
		'function saludo(){\n'+
		'	return "Hola Mundo";\n'+
		'}\n'+
		'\n'+
		'saludo();\n';
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
												'<button id="'+idFormBoxSubmitButton+'" type="submit" class="btn btn-info pull-right" style="margin-top:10px" type="button">Guardar</button>'+
												'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteCodeBox(\''+idHiddenIdNotebook+'\',\''+idHiddenIdBox+'\',\''+idBox+'\',\''+idFormBoxSubmitButton+'\',\''+idFormBox+'\')" type="button">Eliminar</button>'+
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
	                                            /*'<button type="submit" class="btn btn-primary" onclick="evalUserCodeAce('+idEditorParameter+');">'+
	                                               'Ejecutar >>'+
	                                            '</button>'+*/
	                                            '<button type="submit" class="btn btn-primary" onclick="evalUserCodeAceIframe('+idEditorParameter+',\''+idDivParam+'\',\''+idIframe+'\',\''+idInputResultado+'\');">'+
	                                               'Ejecutar>>'+
	                                            '</button>'+
	                                            '<br><br>'+
	                                            '<h4>Resultado del código</h4>'+
	                                            '<input name="resultado_'+idEditor+'" class="form-control resultado_code_editor"  id="resultado_'+idEditor+'" type="text" disabled="disabled">'+
	                                            '<br><br>'+
	                                            '<button id="'+idAddGraphicButton+'" type="submit" class="btn btn-primary" onclick="alert(\'Para añadir gráfica, guarde la caja de código.\')">'+
	                                               'Añadir Gráfica'+
	                                            '</button>'+
	                                        '</div>'+
											'<div class="col-md-12" style="margin-top: 20px;">'+
	                                        	'<iframe style="width:100%;height: 0px;display:none" sandbox=\'allow-scripts\' id="'+idIframe+'" src="iframe_notebook"></iframe>'+
	                                        '</div>'+
	                                    '</div>'+

	                                '</div>'+
	                            '</div>'+
	                        '</div>'+
                        '</div>';

	$('#'+idNotebookContent).append(htmlCodeBox);

    var haveChart = false;
    if(idChart!=null && idChart!=''){
        setTimeout(
          function()
          {
            addChart(idBoxParameter,idColChartButtons,idAddGraphicButton,idBoxBD,idIframe,idChart);
          }, 1000);
        haveChart = true;
    }

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
        createUpdateCodeBox(idHiddenIdNotebook,idHiddenOrder,idHiddenIdBox,idEditor,idAddParamButton,idDivParam,idDivParamButton,idRowPrincipalParameter,idBoxParameter,idColChartButtonsParameter,idAddGraphicButton,idIframe,haveChart);
    });

    //Añadimos el id del formulario al array de formularios para guardado borrador y publicar
    addBoxFormButton(idFormBoxSubmitButton);
    addBoxForm(idFormBox);

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
	var idFormBoxSubmitButton = "form_box_submit_button_"+idBox;
	var idHiddenIdBox = "input_hidden_id_box_"+idBox;
	var idHiddenIdNotebook = "input_hidden_id_notebook_"+idBox;
	var idHiddenOrder = "input_hidden_order_"+idBox;

	if(order==null){
		maxOrder++;
		var order = maxOrder;
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
		                            	'<img class="notebook-img" id="'+idImg+'" src="'+urlImg+'" height="256px" style="max-width: 100%;" />'+
		                        	'</div>'+
		                        '</div>'+
		                        '<div class="form-group col-md-6 offset-md-3" style="padding:12px;">'+
									'<form method="POST" id="'+idFormBox+'">'+
										'<input type="hidden" id="'+idHiddenIdNotebook+'" value="'+idNotebookBD+'">'+
										'<input type="hidden" id="'+idHiddenIdBox+'" value="'+idBoxBD+'">'+
										'<input type="hidden" id="'+idHiddenOrder+'" value="'+order+'">'+
				                        '<input class="form-control col-md-5 offset-md-3" id="'+idUrlInput+'" type="text" placeholder="Establecer URL" required value="'+url+'">'+
										'<div class="col-md-12 offset-md-3" >'+
				                         		'<button id="'+idFormBoxSubmitButton+'" type="submit" class="btn btn-info pull-right" style="margin-top:10px" type="button">Guardar</button>'+
				                         		'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteImageBox(\''+idHiddenIdNotebook+'\',\''+idHiddenIdBox+'\',\''+idBox+'\',\''+idFormBoxSubmitButton+'\',\''+idFormBox+'\')" type="button">Eliminar</button>'+
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

    //Añadimos el id del formulario al array de formularios para guardado borrador y publicar
    addBoxFormButton(idFormBoxSubmitButton);
    addBoxForm(idFormBox);
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

function setParametersIframe(idDivParamsCodeBox, idIframe){
	//En primer lugar, se borran todos los parámetros anteriores del iframe

    resetParamsIframe(idIframe);

    var childrens = $("#"+idDivParamsCodeBox).children();

	for (index1 = 0; index1 < childrens.length; ++index1) {
		//Obtenemos los inputs del form de cada parámetro
    	var children = childrens[index1];
    	var idChildren = children.id;

    	//Recorremos los inputs buscando el id y el valor del parámetro
    	inputs = $("#"+idChildren+" :input");
    	if(inputs!=null){
    		var idParam = null;
	    	var paramValue = null;

	    	for (index2 = 0; index2 < inputs.length; ++index2) {
	    		input = inputs[index2];
	    		
	    		if (input.id && input.id.indexOf(ID_HIDDEN_NAME_PARAM) == 0) {
		        	//Encontrado el id del parámetro
		        	idParam = input.value;
		    	}


	    	}
	    	//Si se ha recuperado el id del parámetro, obtenemos el valor
	    	if(idParam!=null){
		    	paramValue = $('#'+idParam).val();
	    	}
	    	//Si se ha recuperado correctamente el id y valor del parámetro,
	    	//se crea en el iframe
	    	if(idParam!=null && paramValue!=null){
	    		editCreateParamIframe(idIframe, idParam, paramValue);
	    	}
	    }
	}
}

function evalUserCodeAceIframe(idEditor, idDivParamsCodeBox, idIframe, idInputResultado){
    var editor = ace.edit(idEditor);
    var code = editor.getValue();

    /*
    	Comprobamos si el código contiene operaciones no permitidas. Estas son:
    		alert(
    		ajax.
    		window.
    		location.
    		eval(
	*/

	var rexExp = new RegExp("(?:^|\W)(eval)|(alert)|(window.)|(location.)|(ajax)(?:$|\W)");
	var invalidCode = rexExp.test(code);


    /*
    	Recuperamos los valores actuales de los parámetros de la caja de código
		para mandarlos al iframe
    */
    if(!invalidCode){
	    setParametersIframe(idDivParamsCodeBox, idIframe);   

		//Una vez seteados los parámetros en el iframe, ejecutamos el código en él
		data = ['evalCode', code, idInputResultado];

		var sandboxedFrame = document.getElementById(idIframe);

	    sandboxedFrame.contentWindow.postMessage(data, '*');
	}else{
		alert("El código contiene funciones no permitidas. Estas son:\n alert, ajax, window, location y eval");
	}
}

function addNewParameter(idParameterDiv,idButtonParameter,idBox){
	addParameter(idParameterDiv,idButtonParameter,idBox,null,'',null,null);
}

function addParameter(idParameterDiv,idButtonParameter,idBox,idParam,paramValue,idNameValue,nameParam){

	var numParameter = 0;

	if(idNameValue!=null && idNameValue!='null'){
    	var numParamActualString = idNameValue.substring(5,idNameValue.length);
        //Pasar el num como String a Integer
        var numParamActual = parseInt(numParamActualString);
        numParameter = numParamActual;
	}else{
		numParameter = getNumParam();
		numParameter++;
		setNumParam(numParameter);
	}

	/* IDS FORM */
	var idFormParam = "form_param_"+numParameter;
	var idDivParam = "div_param_"+numParameter;
	var idHiddenIdBox = "input_hidden_parameter_id_box_"+numParameter;
	var idHiddenIdPkParam = "input_hidden_parameter_id_pk_param_"+numParameter;
	//El nombre del id para obtenerse por código
	//NO CAMBIAR EL VALOR DE ESTA VARIABLE
	var idHiddenIdNameParam = ID_HIDDEN_NAME_PARAM+numParameter;
	//El nombre del parámetro establecido por el usuario
	var idNameParam = "input__name_param_"+numParameter;
	var idValueParam = "input_parameter_value_"+numParameter;

	/* FIN IDS FORM */

	var idParameterDivParameter = "'"+idParameterDiv+"'";
	var idButtonParameterParameter = "'"+idButtonParameter+"'";
	var idFormBoxSubmitButton = "form_box_submit_button_parameter"+numParameter;

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
    							'<br>'+
    							'<label for="'+idNameParameter+'" class="control-label">Valor</label>'+
    							'<input value="'+paramValue+'" name="'+idNameParameter+'" class="form-control" id="'+idNameParameter+'" type="text" required>'+
    							'<br>'+
    							'<button id="'+idFormBoxSubmitButton+'" type="submit" class="btn btn-primary pull-right" style="margin-top:10px" type="button">Guardar</button>'+
    							'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteParam(\''+idDivParam+'\',\''+idHiddenIdPkParam+'\',\''+idFormBoxSubmitButton+'\',\''+idFormParam+'\')" type="button">Eliminar</button>'+
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

    //Añadimos el id del formulario al array de formularios para guardado borrador y publicar
    addBoxFormButton(idFormBoxSubmitButton);
    addBoxForm(idFormParam);

}

function addChart(idBoxParameter,idColChartButtons,idAddGraphicButton,idBox,idIframe,idChart){

    var persistirGrafica = false;
	if(idChart=='' || idChart==null){
		idChart = "myChart_"+idBoxParameter;
		persistirGrafica=true;
	}


	var idChartRow = idChart+'_row';

    if(persistirGrafica){
        $.ajax({
            url : "/web/createUpdateCodeIdGraphicAjax", // the endpoint
            type : "POST", // http method
            data : {
            'idBox': idBox,
            'idGraphic': idChart,
            }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                console.log(json); // log the returned json to the console
                //alert("Notebook editado correctamente");
                //Actualización de los campos
                console.log("success"); // another sanity check
                //$("#getCodeModal").modal('show');
                //Se comprueba si el box ha sido creado o actua
                addChartIframe(idIframe,idBoxParameter,idColChartButtons,idChart,idAddGraphicButton,idBox);
                $('#notification-text').text('Gráfica creada correctamente');

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
    }else{
        addChartIframe(idIframe,idBoxParameter,idColChartButtons,idChart,idAddGraphicButton,idBox);
    }
	//Botón eliminar gráfica

	//Quitamos previamente el botón de aceptar

	$('#'+idColChartButtons+' button:last-child').remove();


	var htmlDeleteChartButton = '<button type="submit" class="btn btn-primary" onclick="deleteChart('+idBoxParameter+',\''+idColChartButtons+'\',\''+idAddGraphicButton+'\',\''+idBox+'\',\''+idIframe+'\',\''+idChart+'\');">'+
                                   'Eliminar Gráfica'+
                                '</button>';

    $('#'+idColChartButtons).append(htmlDeleteChartButton);

}

function addChartIframe(idIframe,idBoxParameter,idColChartButtons,idChart,idAddGraphicButton,idBox){

	var idChartRow = idChart+'_row';

	//TODO LLAMAR AL IFRAME PARA CARGAR LA GRÁFICA

	var sandboxedFrame = document.getElementById(idIframe);
    data = ['addChart', idChart];

    sandboxedFrame.contentWindow.postMessage(data, '*');

	//Botón eliminar gráfica

	//Quitamos previamente el botón de aceptar

	$('#'+idColChartButtons+' button:last-child').remove();


	var htmlDeleteChartButton = '<button type="submit" class="btn btn-primary" onclick="deleteChart(\''+idBoxParameter+'\',\''+idColChartButtons+'\',\''+idAddGraphicButton+'\',\''+idBox+'\',\''+idIframe+'\');">'+
                                   'Eliminar Gráfica'+
                                '</button>';

    $('#'+idColChartButtons).append(htmlDeleteChartButton);

    //Aumentar el tamaño del iframe para mostrar la gráfica

    document.getElementById(idIframe).style.height = "365px"
    document.getElementById(idIframe).style.display = "block"
    document.getElementById(idIframe).style.marginBottom = "20px";

}

function deleteChartIframe(idIframe, idBoxParameter, idColChartButtons, idAddGraphicButton, idBox, idChart){

	var sandboxedFrame = document.getElementById(idIframe);
    data = ['deleteChart'];

    sandboxedFrame.contentWindow.postMessage(data, '*');

    document.getElementById(idIframe).style.height = "0px"

    $('#'+idColChartButtons+' button:last-child').remove();


	var htmlAddChartButton = '<button type="submit" class="btn btn-primary" onclick="addChart(\''+idBoxParameter+'\',\''+idColChartButtons+'\',\''+idAddGraphicButton+'\',\''+idBox+'\',\''+idIframe+'\',\''+idChart+'\');">'+
                                   'Añadir Gráfica'+
                                '</button>';

    $('#'+idColChartButtons).append(htmlAddChartButton);

    document.getElementById(idIframe).style.display = "none";
    document.getElementById(idIframe).style.marginBottom = "0px";

}

function editCreateParamIframe(idIframe, idParam, valueParam){
    var sandboxedFrame = document.getElementById(idIframe);
    data = ['editCreateParam', idParam, valueParam];

    sandboxedFrame.contentWindow.postMessage(data, '*');
  }


  function resetParamsIframe(idIframe){
    var sandboxedFrame = document.getElementById(idIframe);
    data = ['resetParams'];

    sandboxedFrame.contentWindow.postMessage(data, '*');
  }

  function deleteParamIframe(idIframe, idParam){
    var sandboxedFrame = document.getElementById(idIframe);
    data = ['deleteParam', idParam];

    sandboxedFrame.contentWindow.postMessage(data, '*');
  }

function deleteChart(idBoxParameter,idColChartButtons,idAddGraphicButton,idBox,idIframe,idChart){

	mensajeConfirmacion = '¿Seguro que quiere eliminar esta gráfica?';

	var confirmacion = confirm(mensajeConfirmacion);
	if (confirmacion) {
		//Si idBox no es vacío, la caja ya ha sido persistida y debe eliminarse de BD, antes de eliminar el código HTML correspondiente
		$.ajax({
	        url : "/web/deleteIdGraphicAjax", // the endpoint
	        type : "POST", // http method
	        data : {
	        'idBox': idBox
	        }, // data sent with the post request

	        // handle a successful response
	        success : function(json) {
	            console.log(json); // log the returned json to the console
	            //alert("Notebook editado correctamente");
	            //Actualización de los campos
	            console.log("success"); // another sanity check
	            //$("#getCodeModal").modal('show');
				deleteChartIframe(idIframe, idBoxParameter, idColChartButtons, idAddGraphicButton, idBox, idChart);
	            //Se comprueba si el box ha sido creado o actua
	        	$('#notification-text').text('Gráfica borrada correctamente');

	            $('#notificaciones-holder').slideDown();

	            setTimeout(
	              function()
	              {
	                $('#notificaciones-holder').slideUp();
	              }, 2000);

	            deleteElement(idAddGraphicButton);
                $('#'+idColChartButtons+' button:last-child').remove();

                var htmlAddChartButton = 	'<button id="'+idAddGraphicButton+'" type="submit" class="btn btn-primary" onclick="alert(\'Para añadir gráfica, guarde la caja de código.\')" >'+
	                                               'Añadir Gráfica'+
	                                        '</button>';

                $('#'+idColChartButtons).append(htmlAddChartButton);
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
	}

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
            document.getElementById("notificaciones-holder").className = "alert-success";
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
            document.getElementById("notificaciones-holder").className = "alert-danger";
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

function createUpdateCodeBox(idHiddenIdNotebook, idHiddenOrder, idHiddenIdBox, idEditor, idAddParamButton, idDivParam, idDivParamButton, idRowPrincipalParameter, idBoxParameter, idColChartButtonsParameter,idAddGraphicButton,idIframe,haveChart){
	console.log("Retrieving code box fields"); // sanity check
	var idNotebook = $('#'+idHiddenIdNotebook).val();
	var boxOrder = $('#'+idHiddenOrder).val();
	var idBox = $('#'+idHiddenIdBox).val();

	//Recuperando el código del editor como String
	var editor = ace.edit(idEditor);
    var contentCode = editor.getValue();

    var isSavingdraft = savingDraft;

    //Validar que el código no contiene funciones no permitidas
    var rexExp = new RegExp("(?:^|\W)(eval\\()|(alert\\()|(window.)|(location.)|(ajax)(?:$|\W)");
	var invalidCode = rexExp.test(contentCode);
	if(!invalidCode){

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

		        /*
            	Si no se está guardando el ejercicio como borrador o publicando, 
            	se muestra la notificación individual de la caja
	            */
	            if(!isSavingdraft){
					//Se comprueba si el box ha sido creado o actua
			        var updateBox = json['updateBox'];
			        if(updateBox){
			        	$('#notification-text').text('Box editada correctamente');
			        }else{
			        	$('#notification-text').text('Box creada correctamente');
			        }
			        document.getElementById("notificaciones-holder").className = "alert-success";
			        $('#notificaciones-holder').slideDown();
			        setTimeout(
			          function() 
			          {
			            $('#notificaciones-holder').slideUp();
			          }, 2000);
			    }
		        //Activar el botón de añadir parámetros para esa caja de código
		        //Recuperar id box
		        var idBox = json['savedBoxId'];
		        //Actualizar el campo idbox, por si se está creando
		        $('#'+idHiddenIdBox).val(idBox);

		        $('#'+idAddParamButton).attr("onclick","addNewParameter(\'"+idDivParam+"\',\'"+idDivParamButton+"\',\'"+idBox+"\')");
                //Si no posee gráfica cambiamos la funcionalidad del botón de añadir gráfica, de un alert a un añadir gráfica
                if(!haveChart){
                    $('#'+idAddGraphicButton).attr("onclick","addChart("+idBoxParameter+","+idColChartButtonsParameter+",\'"+idAddGraphicButton+"\',"+idBox+",\'"+idIframe+"\')");
                }

		        //onclick="addParameter('+idDivParamParameter+','+idDivParamButtonParameter+');"

		        //NECESITAMOS ID DEL BOTÓN, '+idDivParamParameter+','+idDivParamButtonParameter+'
		    },

		    // handle a non-successful response
		    error : function(xhr,errmsg,err) {
		        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
		            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
		        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console

		        $('#notification-text').text('Error al editar');
		        rexExp = new RegExp("(?:^|\W)(eval\\()|(alert\\()|(window.)|(location.)|(ajax)(?:$|\W)");
				invalidCode = rexExp.test(contentCode);
				document.getElementById("notificaciones-holder").className = "alert-danger";

				if(!isSavingdraft){
				    if(invalidCode){
				    	$('#notification-text').text('El código contiene funciones no permitidas. Estas son:\n alert, ajax, window, location y eval');
				    	$('#notificaciones-holder').show();
				        setTimeout(
				          function() 
				          {
				            $('#notificaciones-holder').hide();
				          }, 5000);

				    }else{
				    	$('#notificaciones-holder').show();
				        setTimeout(
				          function() 
				          {
				            $('#notificaciones-holder').hide();
				          }, 2000);
				    }
		        }
		        if(isSavingdraft){
		        	errorBatchSave = true;
		        }

		        
		    }
		});
	}else{
		alert("El código contiene funciones no permitidas. Estas son:\n alert, ajax, window, location y eval");
	}

}

//AJAX para crear code param

function createUpdateCodeParam(idHiddenIdBox,idValueParameter,idHiddenIdPkParam,idHiddenIdNameParam,idNameParam){
	console.log("Retrieving code param fields"); // sanity check
	var idBox = $('#'+idHiddenIdBox).val();
	var paramValue = $('#'+idValueParameter).val();
	//PK del parámetro
	var idPkParam = $('#'+idHiddenIdPkParam).val();
	//Id del input del parámetro
	var nameIdParam = $('#'+idHiddenIdNameParam).val();
	//Nombre del parámetro, establecido por el usuario
	var nameParam = $('#'+idNameParam).val();
	

	console.log("Recuperado idBox: "+idBox);
	console.log("Recuperado paramValue: "+paramValue);
	console.log("Recuperado idPkParam: "+idPkParam);
	console.log("Recuperado nameIdParam: "+nameIdParam);
	console.log("Recuperado nameParam: "+nameParam);

	var isSavingdraft = savingDraft;

	if(paramValue!=null && paramValue!='' && nameParam!=null && nameParam!=''){

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

	            /*
	            	Si no se está guardando el ejercicio como borrador o publicando, 
	            	se muestra la notificación individual de la caja
	            */
	            if(!isSavingdraft){
		            //Se comprueba si el box ha sido creado o actua
		            var updateParam = json['updateParam'];
		            if(updateParam){
		            	$('#notification-text').text('Parámetro editado correctamente');
		            }else{
		            	$('#notification-text').text('Parámetro creado correctamente');
		            }

		            document.getElementById("notificaciones-holder").className = "alert-success";

		            $('#notificaciones-holder').slideDown();
		            
		            setTimeout(
		              function() 
		              {
		                $('#notificaciones-holder').slideUp();
		              }, 2000);
		        }
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
	            /*
	            	Si no se está guardando el ejercicio como borrador o publicando, 
	            	se muestra la notificación individual de la caja
	            */
	            if(!isSavingdraft){
		            document.getElementById("notificaciones-holder").className = "alert-danger";

		            $('#notification-text').text('Error al editar');
		            $('#notificaciones-holder').show();

		            setTimeout(
		              function() 
		              {
		                $('#notificaciones-holder').hide();
		              }, 2000);
	        	}else{
	        		errorBatchSave = true;
	        	}
	        }
		});

	}
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

	var isSavingdraft = savingDraft;

	if(paramValue!=null && paramValue!=''){
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

	            /*
	            	Si no se está guardando el ejercicio como borrador o publicando, 
	            	se muestra la notificación individual de la caja
	            */
	            if(!isSavingdraft){
		            //Se comprueba si el box ha sido creado o actua
		            var updateBox = json['updateBox'];
		            if(updateBox){
		            	$('#notification-text').text('Caja de ilustración editada correctamente');
		            }else{
		            	$('#notification-text').text('Caja de ilustración creada correctamente');
		            }
		            document.getElementById("notificaciones-holder").className = "alert-success";
		            $('#notificaciones-holder').slideDown();
		            
		            setTimeout(
		              function() 
		              {
		                $('#notificaciones-holder').slideUp();
		              }, 2000);
	        	}
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
	            
	            /*
	            	Si no se está guardando el ejercicio como borrador o publicando, 
	            	se muestra la notificación individual de la caja
	            */
	            if(!isSavingdraft){
		            document.getElementById("notificaciones-holder").className = "alert-danger";
		            $('#notification-text').text('Error al editar');
		            $('#notificaciones-holder').show();

		            setTimeout(
		              function() 
		              {
		                $('#notificaciones-holder').hide();
		              }, 2000);
	        	}else{
	        		errorBatchSave = true;
	        	}
	        }
		});
	}
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

	var isSavingdraft = savingDraft;

	if(text!=null && text!=''){

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

	            /*
	            	Si no se está guardando el ejercicio como borrador o publicando, 
	            	se muestra la notificación individual de la caja
	            */
	            if(!isSavingdraft){
		            //Se comprueba si el box ha sido creado o actua
		            var updateBox = json['updateBox'];
		            if(updateBox){
		            	$('#notification-text').text('Box editada correctamente');
		            }else{
		            	$('#notification-text').text('Box creada correctamente');
		            }
		            document.getElementById("notificaciones-holder").className = "alert-success";
		            $('#notificaciones-holder').slideDown();
		            
		            setTimeout(
		              function() 
		              {
		                $('#notificaciones-holder').slideUp();
		              }, 2000);
				}
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
	            /*
	            	Si no se está guardando el ejercicio como borrador o publicando, 
	            	se muestra la notificación individual de la caja
	            */
	            if(!isSavingdraft){
		            document.getElementById("notificaciones-holder").className = "alert-danger";

		            $('#notification-text').text('Error al editar');
		            $('#notificaciones-holder').show();

		            setTimeout(
		              function() 
		              {
		                $('#notificaciones-holder').hide();
		              }, 2000);
	        	}else{
	        		errorBatchSave = true;
	        	}
	        }
		});
	}
}

//AJAX para eliminar code box
function deleteCodeBox(idHiddenIdNotebook,idHiddenIdBox,idBoxParameter,idFormBoxSubmitButton,idFormBox){
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
	            document.getElementById("notificaciones-holder").className = "alert-success";
	            //Se comprueba si el box ha sido creado o actua
	        	$('#notification-text').text('Caja de código borrada correctamente');

	            $('#notificaciones-holder').slideDown();
	            
	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').slideUp();
	              }, 2000);

	            deleteElement(idBoxParameter);

	            //Se elimina del array de formularios para guardado borrador o publicar
	            removeBoxFormButton(idFormBoxSubmitButton);
	            removeBoxForm(idFormBox);

	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {
	            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
	            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	            document.getElementById("notificaciones-holder").className = "alert-danger";
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
			//Se elimina del array de formularios para guardado borrador o publicar
	        removeBoxFormButton(idFormBoxSubmitButton);
	        removeBoxForm(idFormBox);
		}
	}
	
}


//AJAX para eliminar text box
function deleteTextBox(idHiddenIdNotebook,idHiddenIdBox,idBoxParameter,idFormBoxSubmitButton,idFormBox){
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
	            document.getElementById("notificaciones-holder").className = "alert-success";
	            //Se comprueba si el box ha sido creado o actua
	        	$('#notification-text').text('Box borrada correctamente');

	            $('#notificaciones-holder').slideDown();
	            
	            setTimeout(
	              function()
 	              {
	                $('#notificaciones-holder').slideUp();
	              }, 2000);

	            deleteElement(idBoxParameter);

	            //Se elimina del array de formularios para guardado borrador o publicar
	            removeBoxFormButton(idFormBoxSubmitButton);
	            removeBoxForm(idFormBox);
	            

	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {
	            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
	            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	            document.getElementById("notificaciones-holder").className = "alert-danger";
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
			//Se elimina del array de formularios para guardado borrador o publicar
            removeBoxFormButton(idFormBoxSubmitButton);
            removeBoxForm(idFormBox);
		}
	}
	
}

//AJAX para eliminar parametro
function deleteParam(idDivParam,idPkParam,idFormBoxSubmitButton,idFormBox){
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
	            document.getElementById("notificaciones-holder").className = "alert-success";
	            //Se comprueba si el box ha sido creado o actua
	        	$('#notification-text').text('Parámetro borrado correctamente');

	            $('#notificaciones-holder').slideDown();
	            
	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').slideUp();
	              }, 2000);

	            deleteElement(idDivParam);

	            //Se elimina del array de formularios para guardado borrador o publicar
	            removeBoxFormButton(idFormBoxSubmitButton);
	            removeBoxForm(idFormBox);

	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {
	            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
	            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	            document.getElementById("notificaciones-holder").className = "alert-danger";
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
			//Se elimina del array de formularios para guardado borrador o publicar
	        removeBoxFormButton(idFormBoxSubmitButton);
	        removeBoxForm(idFormBox);
		}
	}
	
}

//AJAX para eliminar text box
function deleteImageBox(idHiddenIdNotebook,idHiddenIdBox,idBoxParameter,idFormBoxSubmitButton,idFormBox){
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
	            document.getElementById("notificaciones-holder").className = "alert-success";
	            //Se comprueba si el box ha sido creado o actua
	        	$('#notification-text').text('Box borrada correctamente');

	            $('#notificaciones-holder').slideDown();
	            
	            setTimeout(
	              function() 
	              {
	                $('#notificaciones-holder').slideUp();
	              }, 2000);

	            deleteElement(idBoxParameter);

	            //Se elimina del array de formularios para guardado borrador o publicar
	            removeBoxFormButton(idFormBoxSubmitButton);
	            removeBoxForm(idFormBox);

	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {
	            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
	            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	            document.getElementById("notificaciones-holder").className = "alert-danger";
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
			//Se elimina del array de formularios para guardado borrador o publicar
	        removeBoxFormButton(idFormBoxSubmitButton);
	        removeBoxForm(idFormBox);
		}
	}
	
}

function getMaxOrder(){
	return maxOrder;
}

function setMaxOrder(maxOrderParam){
	maxOrder = maxOrderParam;
}

function getNumParam(){
	return numParam;
}

function setNumParam(numParameter){
	numParam = numParameter;
}

function getBoxFormsButtons(){
	return boxFormsButtons;
}

function setBoxFormsButtons(boxFormsButtonParameter){
	return boxFormsButtons = boxFormsButtonParameter;
}

function addBoxFormButton(boxFormButton){
	boxFormsButtons.push(boxFormButton);
}

function removeBoxFormButton(boxFormButton){
	var index = boxFormsButtons.indexOf(boxFormButton);
	if (index > -1) {
	  boxFormsButtons.splice(index, 1);
	}
}

function addBoxForm(boxForm){
	boxForms.push(boxForm);
}

function removeBoxForm(boxForm){
	var index = boxForms.indexOf(boxForm);
	if (index > -1) {
	  boxForms.splice(index, 1);
	}
}

function isSavingDraft(){
	return savingDraft;
}

function setSavingDraft(boolSavingDraft){
	savingDraft = boolSavingDraft;
}

function saveDraft(publishing){
	//Seteamos la bandera de guardado para borrador
	savingDraft = true;
	errorBatchSave = false;
	var formValido = true;
	try {
		//Se recorren los formularios de las cajas para guardarlas
		for (index = 0; index < boxFormsButtons.length; ++index) {
			//Si ha ocurrido un problema guardando alguna caja, se interrumpe la operación
			if(errorBatchSave){
				break;
			}
			boxForm = document.getElementById(boxForms[index]);
			formValido = $("#"+boxForm.id).valid();
			if(formValido){
				boxFormButton = document.getElementById(boxFormsButtons[index]);
				boxFormButton.click();
			}else{
				errorBatchSave = true;
				boxFormButton = document.getElementById(boxFormsButtons[index]);
				boxFormButton.click();
			}
		}

		if(errorBatchSave){
			/*
			Si ha ocurrido un error, mostrar una notificación indicando 
			que el borrador no ha podido guardarse. 
			Mensaje genérico para poder reutilizarlo en publicación
			*/
			document.getElementById("notificaciones-holder").className = "alert-danger";
			if(!publishing){
				if(!formValido){
					$('#notification-text').text('Error al guardar el borrador. Revise los campos marcados en rojo en las cajas.');
				}else{
					$('#notification-text').text('Error al guardar el borrador');
				}
			}else{
				if(!formValido){
					$('#notification-text').text('Error al publicar el ejercicio. Revise los campos marcados en rojo en las cajas.');
				}else{
					$('#notification-text').text('Error al publicar el ejercicio');
				}
			}
            $('#notificaciones-holder').show();

            setTimeout(
              function() 
              {
                $('#notificaciones-holder').hide();
              }, 2000);
		}else{
			/*
			Si todo ha ido bien, mostrar una notificación indicando 
			que el borrador se ha guardado correctamente.
			Mensaje genérico para poder reutilizarlo en publicación
			*/
			document.getElementById("notificaciones-holder").className = "alert-success";
			if(!publishing){
				$('#notification-text').text('Borrador guardado correctamente');
				$('#notificaciones-holder').slideDown();
		        setTimeout(
		          function() 
		          {
		            $('#notificaciones-holder').slideUp();
		          }, 2000);
			}
			
	    }
	} catch (e) {

     	errorBatchSave = true;
     	document.getElementById("notificaciones-holder").className = "alert-danger";
		$('#notification-text').text('Error al guardar el borrador');
        $('#notificaciones-holder').show();

        setTimeout(
          function() 
          {
            $('#notificaciones-holder').hide();
          }, 2000);
        //Reinicio de la bandera de guardado como borrador
        savingDraft = false;
    }
    //Reinicio de la bandera de guardado como borrador
    savingDraft = false;
}

function publish(){
	mensajeConfirmacion = 'Una vez publicado el ejercicio, no podrá editar su contenido. ¿Desea continuar?';

	var confirmacion = confirm(mensajeConfirmacion);
	if (confirmacion) {
		saveDraft(true);
		if(errorBatchSave){
			//Notificar que no puede publicarse porque ha habido error al persistir el borrador
			document.getElementById("notificaciones-holder").className = "alert-danger";
			$('#notification-text').text('El ejercicio no puede publicarse debido a un error guardando sus cambios');
	        $('#notificaciones-holder').show();

	        setTimeout(
	          function() 
	          {
	            $('#notificaciones-holder').hide();
	          }, 2000);
		}else{
			//Enviar el formulario de publicación de ejercicio
			document.publishExerciseForm.submit();
		}
	}
}